import cv2
import numpy as np
from logging import Logger
from .cv_writer_abc import CvWriterABC


class CvWriter(CvWriterABC):
    """
    CvWriter class
    """

    def __init__(self, logger: Logger, **kwargs):
        """
        Init CvWriter class
        :param logger: logger instance
        :param kwargs: Arbitrary keyword arguments
            :output (str): output file
            :codec (str): codec value
            :fps (int): frame rate
            :size (tuple): frame size (width, height)
        """
        super().__init__(**kwargs)
        self._logger: Logger = logger
        self._out: cv2.VideoWriter = self._init_writer()
        self._logger.debug('Initialized CV Writer')

    def __del__(self) -> None:
        self._out.release()
        self._logger.debug('CV writer is stopped')

    def _init_writer(self) -> cv2.VideoWriter:
        """
        Init CV Writer
        :return: None
        """
        return cv2.VideoWriter(self.output, cv2.VideoWriter_fourcc(*self.codec), self.fps, self.size)

    def write_frame(self, frame: np.ndarray) -> None:
        """
        Write frame
        :param frame: current frame
        :return: None
        """
        self._out.write(frame)
