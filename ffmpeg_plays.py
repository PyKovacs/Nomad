import ffmpeg

from settings import get_rtsp_settings

settings = get_rtsp_settings()


stream = ffmpeg.input(settings.url, ss=0)
file = stream.output("test.png", vframes=1)
testfile = file.run(capture_stdout=True, capture_stderr=True)
