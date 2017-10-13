# -*- coding: UTF-8 -*-

import moviepy.editor as mp
import os


class Transformer:
    def __init__(self, videoSrc, audioOut):
        # type: (str, str) -> None
        self.src = videoSrc
        self.out = audioOut
        audioFolder = os.path.join(*(os.path.split(audioOut)[:-1]))
        if not os.path.isfile(videoSrc) or not os.path.isdir(audioFolder):
            raise OSError
        return

    def transform(self):
        # type: () -> bool
        print("\n")
        print(os.path.split(self.src)[-1] + " -> " + os.path.split(self.out)[-1])
        print("\t" + self.src + " -> " + self.out)
        print("\n")
        try:
            clip = mp.VideoFileClip(self.src)
            clip.audio.write_audiofile(self.out)
            return True
        except Exception as err:
            print(err)
            return False


def finalFolderName(src, out):
    # type: (str, str) -> str
    result = os.path.split(src)[-1]
    final = os.path.join(out, result)
    if not os.path.isdir(final):
        os.mkdir(final)
    return final


class FolderTransformer:
    def __init__(self, folderSrc, folderOut):
        # type: (str, str) -> None
        self.src = folderSrc
        self.out = finalFolderName(folderSrc, folderOut)
        if not os.path.isdir(self.src) or not os.path.isdir(self.out):
            raise OSError
        return

    def transform(self):
        # type: () -> int
        errores = 0
        for videoName in os.listdir(self.src):
            folderAndVideo = os.path.join(self.src, videoName)
            if os.path.isfile(folderAndVideo):
                # indice += 1

                subName = videoName.split(".")
                subName[-1] = "mp3"
                audioName = ".".join(subName)

                folderAndAudio = os.path.join(self.out, audioName)

                if os.path.isfile(folderAndAudio):
                    print("Ya existe el archivo:", folderAndAudio)
                    continue

                if not Transformer(folderAndVideo, folderAndAudio).transform():
                    errores += 1

                # print("\t" + str(indice) + "/" + str(total) + " ~ " + str(100 * indice / total) + "%")
        return errores
