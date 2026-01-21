#CvService.py
"""This module contains the CvService class, responsible for handling/coordinating operations connected with Computer Vision modules"""
#This is a class file responsible for handling/coordinating operations connected with
#Computer Vision modules
#A context class in state pattern
from multiprocessing import Process, Queue, Event
import logging

from cv.cv_pipe_status import CvPipeStatus
from cv.cv_state import CvState
from cv.roi_processor import RoiProcessor
from cv.video_processor import VideoProcessor

logger = logging.getLogger(__name__)

class CvService():
    """
    CvService is a class responsible for handling operations/tasks connected with Computer Vision modules.

    CvService also acts as a `context class` in a `state design pattern`.
    Acquisition of data required for CV logic is dependent on current CvState,
    and its' implementations can be found in respective classes.
    Depending on task class can execute tasks inside current QThread or start
    a separate process, to avoid problem with GIL and optimally use processing power.

    Parameters
    ----------
    model_path : str
        Path to the appropriate ML model weights.
    state : CvState
        State class object

    Attributes
    ----------
    _mask_coords : ndarray
        ROI mask coordinates.
    _roi_processor : RoiProcessor
        Class responsible for Region of Interest operations
    """
    _state = None
    def __init__(self, model_path, state: CvState = None, mask_coords = None):
        self._model_path = model_path
        self._image_path = None
        self._mask_coords = mask_coords
        self._roi_processor = RoiProcessor(model_path)
        self.transition_to(state)
        self._video_process = None
        self._stop_event = Event()
    
    def shutdown(self):
        self.stop_video_process()
    
    def transition_to(self, state: CvState):
        """Transit to a new state."""
        logger.info(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    ### ROI CREATION ###
    def fetch_image(self):
        """Return an input image (from camera/data/else) - depending on state."""
        return self._state.fetch_image()

    def run_roi_creation_pipeline(self):
        """
        Call RoiProcessor ROI creation logic

        Stores mask coordinates as class variable.

        Returns
        -------
        cv2
            cv2 image

        """
        img = self.fetch_image() # Important! Fetch image only once (avoids bugs with camera movement)
        self._mask_coords = self._roi_processor._mask_exporter(img) # !! MASK COORDS SHOULD BE STORED ALSO IN MEMORY! (TODO Issue #24!)
        return self._roi_processor._mask_painter(img,self._mask_coords), self._mask_coords #image
    
    ### ROI CV COUNT PIPELINE ###   
    def get_vid_source(self):
        """Setup video input source (device/memory) - depending on state."""
        return self._state.get_vid_source()

    def _start_video_process(self, vid_source, roi_mask, stop_event, status_queue: Queue, frame_queue: Queue):
        """
        THIS IS A SEPARATE process for MOB detection pipe.

        Uses run_mob_detect_pipe_process() for starting the process.
        Values from VideoProcessor.run_video_inference() are returned using yield.
        Values are returned to main process using queue.

        Parameters:
        ----------
        vid_source : str
            Video source string.
        roi_mask : ndarray
            ROI mask coordinates
        frame_queue : multiprocessing.Queue
            Queue used to send output frames to caller.
        """
        try:    
            v_processor = VideoProcessor(self._model_path, vid_source, roi_mask)
            status_queue.put((CvPipeStatus.Running, "")) # Sending status message
            
            for frame in v_processor.run_video_inference(stop_event):
                if frame is None:
                    logger.info("Frame is None")
                    break
                frame_queue.put(frame) #Sending frames
            frame_queue.put(None) #end of frames
            status_queue.put((CvPipeStatus.END, "")) # Sending end status

        except Exception as e:
            status_queue.put((CvPipeStatus.ERROR,str(e)))

    def run_mob_detect_pipe_process(self):
        """
        Starts MOB detection in separate process.

        New process calls self._start_video_process with
        appropriate arguments.

        Returns
        -------
        multiprocessing.Queue
            Queue emitting output frames.
        """
        vid_source = self.get_vid_source()
        status_queue = Queue()
        frame_queue = Queue()

        self._stop_event.clear()
        self._video_process = Process(target = self._start_video_process, args=(vid_source, self._mask_coords, self._stop_event ,status_queue, frame_queue))
        self._video_process.start()
        return status_queue, frame_queue
    
    def stop_video_process(self):
        """Terminate mob detection separate process"""
        logger.info("Trying to stop video process...")
        video_process = getattr(self, "_video_process", None)
        if video_process is None:
            # No process to stop, do NOT touch the stop_event
            logger.info("stop_video_process called, but no CV process running")
            return

        logger.info("STOPPING VIDEO PROCESS")
        self._stop_event.set()
        video_process.join(timeout=4)

        if video_process.is_alive():
            logger.warning("Video process did not exit by stop event, terminating")
            video_process.terminate()
            video_process.join(timeout=4)

        self._video_process = None
        logger.info("CV process stopped")