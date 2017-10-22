# -*- coding: UTF-8 -*-

from pytube import YouTube


class Downloader:
    def __init__(self, ytUrl):
        # type: (str) -> None
        self.url = ytUrl
        self.data = None
        return

    def parseYT(self):
        self.data = YouTube(self.url)
        return

    def getValues(self, **kwargs):
        return [Streams(x) for x in self.data.streams.filter(**kwargs).all()]

    def download(self, itag, outputName=None, **kwargs):
        filtered = self.data.streams.filter(**kwargs)
        video = filtered.get_by_itag(itag)
        video.download(outputName)
        return

    def on_download(self, callback):
        self.data.register_on_progress_callback(callback)
        return


class Streams:
    def __init__(self, stream):
        self.stream = stream

    def __repr__(self):
        parts = '{s.itag}, {s.mime_type}, '
        if self.stream.includes_video_track:
            parts += '{s.resolution}@{s.fps}, video_codec: {s.video_codec}'
            if not self.stream.is_adaptive:
                parts += ', audio_codec: {s.audio_codec}'
        else:
            parts += '{s.abr}, audio_codec: {s.audio_codec}'
        return parts.format(s=self.stream)
