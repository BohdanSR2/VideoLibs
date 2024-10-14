import cv2
import time
from typing import Union
from logging import Logger
from .cv_reader_abc import CvReaderABC


class CvStreamReader(CvReaderABC):
    """
    CvStreamReader class
    """

    def __init__(self, path: Union[int, str], logger: Logger, **kwargs):
        """
        Init OpenCV stream readers
        :param path: path to video source
        :param logger: logger instance
        :param kwargs: Arbitrary keyword arguments
            :fps (int): set fps value
            :width (int): set frame width
            :height (int): set frame height
        """
        super().__init__(path=path, **kwargs)
        self._logger: Logger = logger
        self._init_capture()

    def __del__(self):
        self._capture.release()
        self._logger.debug('CV stream reader is stopped')

    def __str__(self):
        return f'{type(self).__name__}(path={self.path})'

    def __repr__(self):
        return f'{type(self).__name__}(path={self.path}, logger={self._logger})'

    def _init_capture(self) -> None:
        """
        Initialize VideoCapture object
        :return: None
        """
        self._capture = cv2.VideoCapture(self.path)
        while not self._capture.isOpened():
            self._logger.debug('Capture is not opened, reopening..')
            time.sleep(5)
            self._capture = cv2.VideoCapture(self.path)
        else:
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH,
                              self.width if self.width else int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)))
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT,
                              self.height if self.height else int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self._capture.set(cv2.CAP_PROP_FPS, self.fps if self.fps else self._capture.get(cv2.CAP_PROP_FPS))
            self._logger.debug('Capture is opened')
