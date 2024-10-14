import subprocess
import numpy as np
from logging import Logger
from typing import Union, Generator
from .ffmpeg_reader_abc import FfmpegReaderABC


class FfmpegReader(FfmpegReaderABC):
    """
    FfmpegReader class
    """

    def __init__(self, logger: Logger, params: list, ffmpeg_binary: Union[str, None] = None):
        """
        Init FfmpegReader class
        :param logger: logger instance
        :param params: ffmpeg params
        :param ffmpeg_binary: path to ffmpeg binary (None if installed globally)
        """
        super().__init__(ffmpeg_binary=ffmpeg_binary)
        self._logger: Logger = logger
        self._params: list = params
        self._process: subprocess.Popen[bytes] = self._process_setup()

        if not self._check_installation():
            raise Exception('Failed to run Ffmpeg for reading')

        self._logger.debug('Initialized Ffmpeg reader')

    def __str__(self):
        return (f'{type(self).__name__}(\nffmpeg_binary={self.ffmpeg_binary},\n'
                f'ffmpeg_params={self._params}\n)')

    def __repr__(self):
        return (f'{type(self).__name__}(ffmpeg_binary={self.ffmpeg_binary},'
                f'logger={self._logger},'
                f'{self._params})')

    def __del__(self) -> None:
        """
        Cleanup method
        :return: None
        """
        self._logger.debug('Stopping FFmpeg reader..')
        self._process.stdout.close()
        self._logger.debug('FFmpeg reader is stopped')

    def _check_installation(self) -> bool:
        """
        Verify ffmpeg installation
        :return: bool
        """
        try:
            result: subprocess.CompletedProcess = subprocess.run(
                [self.ffmpeg_binary, '-version'],
                capture_output=True, text=True, check=True)
            self._logger.debug(f'FFMPEG installation info: {result.stdout.splitlines()[0]}')
            return True
        except subprocess.CalledProcessError as e:
            self._logger.error(f'FFMPEG command failed: {e.stderr}')
            return False
        except FileNotFoundError:
            self._logger.error(f'FFMPEG is not installed or not found in PATH')
            return False

    def _process_setup(self) -> subprocess.Popen[bytes]:
        """
        Generate FFmpeg command
        :return: process (Popen[bytes])
        """
        self._params.insert(0, self.ffmpeg_binary)
        return subprocess.Popen(self._params, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def read(self) -> Generator:
        """
        Frames generator
        :return: Generator
        """
        try:
            width, height = self._params[self._params.index('-s') + 1].split('x')
            width, height = int(width), int(height)
        except Exception as e:
            raise Exception(f'Failed to set width and height, {e}')

        while True:
            in_bytes = self._process.stdout.read(width * height * 3)
            if not in_bytes:
                self._logger.debug('No frame received!')
                break
            yield np.frombuffer(in_bytes, np.uint8).reshape((height, width, 3))
