# -*- coding: UTF-8 -*-

from pytube import YouTube
import os


class Downloader:
    def __init__(self, ytUrl):
        # type: (str) -> None
        self.url = ytUrl
        self.data = YouTube(self.url)
        return
