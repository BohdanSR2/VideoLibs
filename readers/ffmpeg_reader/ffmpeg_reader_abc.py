import os.path
import subprocess
from abc import ABC, abstractmethod
from typing import Union, Self, Generator


class FfmpegReaderABC(ABC):
    """
    FfmpegReaderABC class
    """

    def __init__(self, ffmpeg_binary: Union[str, None] = None):
        """
        Init FfmpegReaderABC class
        :param ffmpeg_binary: path to ffmpeg binary (None if installed globally)
        """
        self.ffmpeg_binary: Union[str, None] = ffmpeg_binary

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

    @property
    def ffmpeg_binary(self) -> Union[str, None]:
        """
        self._ffmpeg_binary path getter
        :return: path to ffmpeg binary or None if set to global installation
        """
        return self._ffmpeg_binary

    @ffmpeg_binary.setter
    def ffmpeg_binary(self, path: Union[str, None]) -> Union[None, TypeError, FileNotFoundError]:
        """
        self._ffmpeg_binary setter
        :param path: path to ffmpeg binary
        :return: None, TypeError or FileNotFoundError
        """
        if not isinstance(path, (str, type(None))):
            raise TypeError(f'ffmpeg binary path must be str or None, not {type(path)}!')
        elif type(path) is str and not os.path.exists(path):
            raise FileNotFoundError(f'ffmpeg executable not found!')

        self._ffmpeg_binary = path if type(path) is str else 'ffmpeg'

    @abstractmethod
    def _check_installation(self) -> bool:
        """
        Verify ffmpeg installation
        :return: bool
        """
        pass

    @abstractmethod
    def _process_setup(self) -> subprocess.Popen[bytes]:
        """
        Generate FFmpeg command
        :return: process (Popen[bytes])
        """
        pass

    @abstractmethod
    def read(self) -> Generator:
        """
        Frames generator
        :return: Generator
        """
        pass
