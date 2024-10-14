import numpy as np
from typing import Union, Self
from abc import ABC, abstractmethod


class CvWriterABC(ABC):
    """
    CvWriterABC class
    """
    def __init__(self, **kwargs):
        """
        Init CvWriterABC class
        :param kwargs: Arbitrary keyword arguments
            :output (str): output file
            :codec (str): codec value
            :fps (int): frame rate
            :size (tuple): frame size (width, height)
        """
        self.output: str = kwargs.get('output', 'output.mp4')
        self.codec: str = kwargs.get('codec', 'mp4v')
        self.fps: int = kwargs.get('fps', 30)
        self.size: tuple = kwargs.get('size', (1280, 720))

    def __enter__(self) -> Self:
        """
        Enter the runtime context related to this object.
        :return: self
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit the runtime context related to this object.
        :param exc_type: The exception type, if an exception was raised.
        :param exc_val: The exception value, if an exception was raised.
        :param exc_tb: The traceback object, if an exception was raised.
        :return: bool
        """
        return exc_type is KeyboardInterrupt

    # region getters/setters
    @property
    def output(self) -> str:
        """
        self._output getter
        :return: str
        """
        return self._output

    @output.setter
    def output(self, value: str) -> Union[None, TypeError]:
        """
        self._output setter
        :param value: output file
        :return: None or TypeError
        """
        if not isinstance(value, str):
            raise TypeError(f'Output file must be str, not {type(value)}')
        self._output = value

    @property
    def codec(self) -> str:
        """
        self._codec getter
        :return: str
        """
        return self._codec

    @codec.setter
    def codec(self, value: str) -> Union[None, TypeError]:
        """
        self._codec setter
        :param value: codec value
        :return: None or TypeError
        """
        if not isinstance(value, str):
            raise TypeError(f'Codec must be str, not {type(value)}')
        self._codec = value

    @property
    def fps(self) -> int:
        """
        self._fps getter
        :return: str
        """
        return self._fps

    @fps.setter
    def fps(self, value: int) -> Union[None, TypeError]:
        """
        self._fps setter
        :param value: fps value
        :return: None or TypeError
        """
        if not isinstance(value, int):
            raise TypeError(f'FPS value must be int, not {type(value)}')
        self._fps = value

    @property
    def size(self) -> tuple:
        """
        self._size getter
        :return: tuple
        """
        return self._size

    @size.setter
    def size(self, value: tuple) -> Union[None, TypeError]:
        """
        self._size setter
        :param value: frame size
        :return: None or TypeError
        """
        if not isinstance(value, tuple):
            raise TypeError(f'Frame size value must be tuple, not {type(value)}')
        self._size = value

    # endregion

    @abstractmethod
    def _init_writer(self) -> None:
        """
        Init CV Writer
        :return: None
        """
        pass

    @abstractmethod
    def write_frame(self, frame: np.ndarray) -> None:
        """
        Write frame
        :param frame: current frame
        :return: None
        """
        pass
