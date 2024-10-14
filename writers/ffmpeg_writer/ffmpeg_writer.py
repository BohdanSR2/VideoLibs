import subprocess
import numpy as np
from typing import Union
from logging import Logger
from .ffmpeg_writer_abc import FfmpegWriterABC


class FfmpegWriter(FfmpegWriterABC):
    """
    FfmpegWriter class
    """

    def __init__(self, logger: Logger, params: list, ffmpeg_binary: Union[str, None] = None):
        """
        Init FfmpegWriter class
        :param logger: logger instance
        :param params: ffmpeg params
        :param ffmpeg_binary: path to ffmpeg binary (None if installed globally)
        """
        super().__init__(ffmpeg_binary=ffmpeg_binary)
        self._params: list = params
        self._logger: Logger = logger
        self._process: subprocess.Popen[bytes] = self._process_setup()

        if not self._check_installation():
            raise Exception('Failed to run Ffmpeg for writing')

        self._logger.debug('Initialized Ffmpeg writer')

    def __str__(self):
        return (f'{type(self).__name__}(\nffmpeg_binary={self.ffmpeg_binary},\n'
                f'ffmpeg_params={self._params}\n)')

    def __repr__(self):
        return (f'{type(self).__name__}(ffmpeg_binary={self.ffmpeg_binary},'
                f'logger={self._logger},'
                f'{self._params})')

    def __del__(self) -> None:
        """
        FfmpegWriter cleanup
        :return: None
        """
        self._process.stdin.close()
        self._logger.debug('Ffmpeg writer is stopped')

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
        return subprocess.Popen(self._params, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def write(self, frame: np.ndarray) -> None:
        """
        Write frames
        :param frame: current frame
        :return: None
        """
        self._process.stdin.write(frame.tobytes())
