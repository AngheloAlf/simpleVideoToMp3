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
        return self.data.streams.filter(**kwargs).all()
