# Python Modules Lib

# 1. Video Readers

## 1.1. OpenCV readers

### OpenCV file reader
Grab frames from a single video file.

***Create CvFileReader instance***

```python
from readers import CvFileReader

cv_file_reader = CvFileReader(path='<path-to-video-file>',
                              logger='<logger-instance>',
                              **{'width': '<value>', 'height': '<value>', 'fps': '<value>'})
while cv_file_reader.is_opened:
    frame = next(cv_file_reader)
    if frame is None:
        break
    ...
```

***CvFileReader with ContextManager:***

```python
from readers import CvFileReader

with CvFileReader(path='<path-to-video-file>',
                  logger='<logger-instance>',
                  **{'width': '<value>', 'height': '<value>', 'fps': '<value>'}) as cv_file_reader:
    while cv_file_reader.is_opened:
        frame = next(cv_file_reader)
        if frame is None:
            break
        ...
```

### OpenCV stream reader
Grab frames from a video stream

```python
from readers import CvStreamReader

cv_stream_reader = CvStreamReader(path='<path-to-video-file>',
                                  logger='<logger-instance>',
                                  **{'width': '<value>', 'height': '<value>', 'fps': '<value>'})
while cv_stream_reader.is_opened:
    frame = next(cv_stream_reader)
    if frame is None:
        break
    ...
```

***CvStreamReader with ContextManager:***
```python
from readers import CvStreamReader

with CvStreamReader(path='<path-to-video-file>',
                    logger='<logger-instance>',
                    **{'width': '<value>', 'height': '<value>', 'fps': '<value>'}) as cv_stream_reader:
    while cv_stream_reader.is_opened:
        frame = next(cv_stream_reader)
        if frame is None:
            break
        ...
```

## 1.2. FFMPEG reader

***Create FfmpegReader reader instance:***

```python
from readers import FfmpegReader

reader = FfmpegReader(ffmpeg_binary='<path_to_ffmpeg_exe_or_None_if_global>',
                      logger='<logger_instance>',
                      params=['-i', '<path_to_source>',
                              'specify_other_ffmpeg_params'])

for frame in reader.read():
    if frame is None:
        break
    ...
```

***FfmpegReader with ContextManager:***

```python
from readers import FfmpegReader

with FfmpegReader(ffmpeg_binary='<path_to_ffmpeg_exe_or_None_if_global>', 
                  logger='<logger_instance>', 
                  params=['-i', '<path_to_source>', 'specify_other_ffmpeg_params']) as reader:

    for frame in reader.read():
        if frame is None:
            break
        ...
```

# 2. Video Writers

## 2.1. OpenCV writer

Write frames using OpenCV-Python

```python
from writers import CvWriter
from readers import CvFileReader

cv_file_reader = CvFileReader(path='<path_to_source>', logger='<logger_instance>')
cv_writer = CvWriter(logger='<logger_instance>')

while cv_file_reader.is_opened:
    frame = next(cv_file_reader)
    if frame is None:
        break
    cv_writer.write_frame(frame=frame)
```

***CvWriter with ContextManager:***

```python
from writers import CvWriter
from readers import CvFileReader

cv_file_reader = CvFileReader(path='<path_to_source>', logger='<logger_instance>')

with CvWriter(logger='<logger_instance>', **{'additional': 'params'}) as cv_writer:
    while cv_file_reader.is_opened:
        frame = next(cv_file_reader)
        if frame is None:
            break
        cv_writer.write_frame(frame=frame)
```

## 2.2. FFMPEG writer

Init FFMPEG Writer (also available using Context Manager)

```python
from readers import CvFileReader
from writers import FfmpegWriter

cv_file_reader = CvFileReader(path=..., logger=...)
writer = FfmpegWriter(logger=..., 
                      ffmpeg_binary=...,
                      params=['-y',
                              '-f', 'rawvideo',
                              '-pixel_format', 'bgr24',
                              '-video_size', f'{1920}x{1080}',
                              '-framerate', str(30),
                              '-i', 'pipe:',
                              '-pix_fmt', 'yuv420p',
                              'test.mp4'])

while cv_file_reader.is_opened:
    frame = next(cv_file_reader)
    if frame is None:
        break
    writer.write(frame)
```


# 3. Logging Configurator

Set up logger for further usage

```python
import logging
from logging_config import LoggerSetup

logger = LoggerSetup(level=logging.DEBUG,
                         datefmt='%Y-%m-%d %H:%M:%S',
                         msg_format='%(asctime)s|%(name)s|%(levelname)s - %(message)s',
                         output_file='app.log').create_logger(name='TEST_LOGGER')
logger.debug('Debug log')
```
***NOTE:*** in case if debug in cmd is needed set output_file to None

