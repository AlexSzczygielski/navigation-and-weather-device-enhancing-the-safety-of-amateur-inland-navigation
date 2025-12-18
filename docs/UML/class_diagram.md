# Updated for commit [`61f2f04`](https://github.com/AlexSzczygielski/navigation-and-weather-device-enhancing-the-safety-of-amateur-inland-navigation/tree/61f2f047f7a5d1419de4b148b8427dd4965c065f)

```mermaid
---
title: Class Diagram
---

classDiagram
    note for Backend "Backend manages connection
    (signals/slots)
    betweenen GUI and Workers logic"

    class Backend {
        # _model_path: str
        # _worker: CvWorker
        # _roi_img_base_64: str
        + img_ready: pyqtSignal
        + imageUpdated: pyqtSignal
        + << create >> Backend(model_path: str)
        + << slot >> run_cv_roi_pipe(): void
        + on_run_cv_roi_pipe_finished(img_64: str): void
        + on_run_cv_roi_pipe_error(): void
        + get_roi_img(): str
    }

    note for CvWorker "Worker classes are 
    responsible for QThread management"

    class CvWorker {
        # _model_path: str
        # _service_state: CvState
        + finished: pyqtSignal
        + error: pyqtSignal
        + << create >> CvWorker(model_path: str, service_state: CvState)
        + run(): void
    }

    note for CvService "Service classes are responsible 
    for logic implementation. This is a context class."

    class CvService {
        # _model_path: str
        # _image_path: str
        # _mask_coords: ndarray
        # _roi_processor: RoiProcessor
        # _video_processor: VideoProcessor
        # _state: CvState
        + << create >> CvService(model_path: str, state: CvState)
        + transition_to(state: CvState): void
        + fetch_image(): str
        + run_roi_creation_pipeline(): ndarray
        + fetch_frame(cap): (bool, ndarray)
        + setup_vid_stream(): VideoCapture
        + run_video_detection_pipeline(): void
    }

    class CvState {
        + context: CvService
        + << abstract >> setup_vid_stream(): VideoCapture
        + << abstract >> fetch_image(): str
        + << abstract >> fetch_frame(cap): (bool, ndarray)
    }

    class CvDemoStateService {
        + setup_vid_stream(): VideoCapture
        + fetch_image(): str
        + fetch_frame(cap): (bool, ndarray)
    }

    class RoiProcessor {
        # _model: YOLO
        + << create >> RoiProcessor(model_path: str)
        # _mask_exporter(img): ndarray
        # _mask_painter(image: str, mask_coords: ndarray): ndarray
    }

    class VideoProcessor {
        # _model: YOLO
        + << create >> VideoProcessor(model_path: str)
        + run_video_inference(cap): void
    }

    Backend *-- CvWorker
    CvWorker --|> QThread
    CvWorker *-- CvService
    CvService o-- CvState
    CvService o-- RoiProcessor
    CvService o-- VideoProcessor
    CvDemoStateService --|> CvState
