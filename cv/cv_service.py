#CvService.py
"""This module contains the CvService class, responsible for handling/coordinating operations connected with Computer Vision modules"""
#This is a class file responsible for handling/coordinating operations connected with
#Computer Vision modules
#A context class in state pattern
from cv.cv_state import CvState
from cv.roi_processor import RoiProcessor
from cv.video_processor import VideoProcessor
from multiprocessing import Process, Queue

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
    def __init__(self, model_path, state: CvState = None):
        self._model_path = model_path
        self._image_path = None
        self._mask_coords = None
        self._roi_processor = RoiProcessor(model_path)
        self.transition_to(state)
        self._video_process = None
    
    def __del__(self):
        self.stop_video_process()
    
    def transition_to(self, state: CvState):
        """Transit to a new state."""
        print(f"Context: Transition to {type(state).__name__}")
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
        return self._roi_processor._mask_painter(img,self._mask_coords) #image
    
    ### ROI CV COUNT PIPELINE ###   
    def get_vid_source(self):
        """Setup video input source (device/memory) - depending on state."""
        return self._state.get_vid_source()

    def _start_video_process(self, vid_source, roi_mask, queue: Queue):
        """
        Manage separate process for MOB detection pipe.

        Uses run_mob_detect_pipe_process() for starting the process.
        Values from VideoProcessor.run_video_inference() are returned using yield.

        Parameters:
        ----------
        vid_source : str
            Video source string.
        roi_mask : ndarray
            ROI mask coordinates
        queue : multiprocessing.Queue
            Queue used to send output frames to caller.
        """
        v_processor = VideoProcessor(self._model_path, vid_source, roi_mask)
        for frame in v_processor.run_video_inference():
            if frame is None:
                break
            queue.put(frame) #Sending frames
        queue.put(None) #end of frames

    def run_mob_detect_pipe_process(self):
        """
        Starts MOB detection in separete process.

        New process calls self._start_video_process with
        appropriate arguments.

        Returns
        -------
        multiprocessing.Queue
            Queue emitting output frames.
        """
        vid_source = self.get_vid_source()
        queue = Queue()
        self._video_process = Process(target = self._start_video_process, args=(vid_source, self._mask_coords, queue))
        self._video_process.start()
        return queue
    
    def stop_video_process(self):
        """Terminate mob detection separate process"""
        if self._video_process is not None:
            self._video_process.terminate()
            self._video_process.join()
            self._video_process = None