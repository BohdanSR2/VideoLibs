import cv2
import numpy as np
from typing import Union, Self
from abc import ABC, abstractmethod


class CvReaderABC(ABC):
    """
    CvReaderABC class
    """
    def __init__(self, path: Union[int, str], **kwargs):
        """
        Init CvReaderABC class
        :param path: path to video source
        :param kwargs: Arbitrary keyword arguments
            :fps (int): set fps value
            :width (int): set frame width
            :height (int): set frame height
        """
        self.path: Union[int, str] = path
        self._capture: Union[cv2.VideoCapture, None] = None

        self.fps: int = kwargs.get('fps', None)
        self.width: int = kwargs.get('width', None)
        self.height: int = kwargs.get('height', None)

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

    def __next__(self) -> Union[np.ndarray, None]:
        """
        Grab next frame
        :return: frame value or None
        """
        _, frame = self._capture.read()
        return frame if _ else None

    # region getters/setters
    @property
    def is_opened(self) -> bool:
        """
        Get self._capture.isOpened() state
        :return: bool
        """
        return self._capture.isOpened()

    @property
    def path(self) -> Union[int, str]:
        """
        self._path getter
        :return: self._path value
        """
        return self._path

    @path.setter
    def path(self, path: Union[int, str]) -> Union[None, TypeError]:
        """
        self._path setter
        :param path: path to video source
        :return: None or TypeError
        """
        if isinstance(path, (int, str)):
            self._path = path
            return

        raise TypeError(f'Path to video source must be int or str, not {type(path)}!')

    @property
    def fps(self) -> Union[int, None]:
        """
        self._fps getter
        :return: fps value
        """
        return self._fps

    @fps.setter
    def fps(self, value: Union[int, None]) -> Union[None, TypeError]:
        """
        self._fps setter
        :param value: fps value
        :return: None or TypeError
        """
        if not isinstance(value, (int, type(None))):
            raise TypeError(f'FPS value must be int or None, not {type(value)}')

        self._fps = value

    @property
    def width(self) -> Union[int, None]:
        """
        self._width getter
        :return: int
        """
        return self._width

    @width.setter
    def width(self, value: Union[str, None]) -> Union[None, TypeError]:
        """
        self._width setter
        :param value: frame width value
        :return: None or TypeError
        """
        if not isinstance(value, (int, type(None))):
            raise TypeError(f'Frame width value must be int or None, not {type(value)}')

        self._width = value

    @property
    def height(self) -> Union[int, None]:
        """
        self._height getter
        :return: int
        """
        return self._height

    @height.setter
    def height(self, value: Union[str, None]) -> Union[None, TypeError]:
        """
        self._height setter
        :param value: frame height value
        :return: None or TypeError
        """
        if not isinstance(value, (int, type(None))):
            raise TypeError(f'Frame height value must be int or None, not {type(value)}')

        self._height = value

    # endregion

    @abstractmethod
    def _init_capture(self) -> None:
        """
        Initialize VideoCapture object
        :return: None
        """
        pass
