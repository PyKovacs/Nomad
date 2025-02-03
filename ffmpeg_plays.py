import ffmpeg

from settings import get_rtsp_settings

settings = get_rtsp_settings()
stream = ffmpeg.input(settings.url, ss=0)
frame_count = 0

while True:
    file = stream.output(f"test{frame_count}.png", vframes=1)
    testfile = file.run(capture_stdout=True, capture_stderr=True)
    frame_count += 1
