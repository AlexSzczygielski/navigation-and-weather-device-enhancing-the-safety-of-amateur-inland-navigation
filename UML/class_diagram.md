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
        + img_ready: pyqtSignal(str)
        + imageUpdated: pyqtSignal(str)
        + << create >> Backend(model_path: str)
        + << slot >> run_cv(): void
        + on_run_cv_finished(img_path: str): void
        + on_run_cv_error(): void
    }

    note for CvWorker "Worker classes are 
    responsible for QThread management"

    class CvWorker {
        # _model_path: str
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
        # _state: CvState
        + << create >> CvService(model_path: str, state: CvState)
        + transition_to(state: CvState): void
        # _fetch_image(): void
        # _mask_exporter(): ndarray
        # _mask_painter(): void
    }

    class CvState {
        + context: CvService
        + << abstract >> fetch_image(): void
    }

    class CvDemoStateService {
        + fetch_image(): void
    }

    Backend *-- CvWorker
    CvWorker --|> QThread
    CvWorker *-- CvService
    CvService o-- CvState
    CvService o-- "1" ultralytics.YOLO
    CvService o-- "1" cv2
    CvService o-- "1" numpy
    CvDemoStateService --|> CvState
