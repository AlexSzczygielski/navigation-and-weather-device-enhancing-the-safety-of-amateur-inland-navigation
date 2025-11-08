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

    note for IWorker "IWorker classes wrap the QThread - 
    they are responsible for threaded processing"

    class IWorker {
        + finished: pyqtSignal(str)
        + error: pyqtSignal(str)
        + run(): void
    }

    note "Worker classes are responsible 
    for logic implementation"

    class CvWorker {
        # _model_path: str
        + << create >> CvWorker(model_path: str)
    }

    class CvService {
        # _model_path: str
        # _image_path: str
        + << create >> CvService(model_path: str)
        # _fetch_image(): void
        # _mask_exporter(): ndarray
        # _mask_painter(): void
    }

    Backend *-- CvWorker
    CvWorker --|> QThread
    CvWorker --|> IWorker
    CvWorker *-- CvService
    CvService o-- "1" ultralytics.YOLO
    CvService o-- "1" cv2
    CvService o-- "1" numpy