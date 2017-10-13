# -*- coding: UTF-8 -*-
from . import GuiManager
from . import GuiGenerator
from . import Transformer


class AppData:
    def __init__(self):
        # type: () -> None
        self.gui = GuiManager.GuiManager("Simple downloader")
        self.subGui = None
        return

    def start(self):
        # type: () -> None

        print(u"Preparando menú superior...")
        cascadeNames = [u"Archivo"]
        cascadeData = [
            [
                (u"Salir", self.onMainClose)
            ]
        ]
        self.gui.addMenu(cascadeNames, cascadeData)

        print(u"Preparando pestañas...")
        self.gui.addTab("Descargar", GuiGenerator.downloadTab)

        self.gui.addTab("Transformar", GuiGenerator.transformTab)
        self.gui.buttons["transformFolder"][0]["command"] = self.transformFolder
        self.gui.buttons["transformFolder"][0]["state"] = "normal"

        print(u"Pestañas listas!")

        self.gui.overrideClose(self.onMainClose)

        print(u"Iniciando interfaz.\n")
        self.gui.start()
        return

    def onMainClose(self):
        # type: () -> None
        wantToExit = GuiManager.popupYesNo(u"¿Cerrar?", "¿Seguro que quieres salir de la aplicación?")
        if wantToExit:
            print(u"\nCerrando...\n")
            self.gui.quit()
        return

    def transformFolder(self):
        folderSrc = GuiManager.selectFolder(u"Seleccione su carpeta de videos")
        if not folderSrc:
            return
        folderOut = GuiManager.selectFolder(u"Seleccione su carpeta de destino")
        if not folderOut:
            return

        self.gui.disableAll()
        errors = Transformer.FolderTransformer(folderSrc, folderOut).transform()
        self.gui.enableAll()
        if errors == 0:
            GuiManager.popupInfo(u"Exito.", u"Se han transformado todos sus videos.")
        else:
            GuiManager.popupWarning(u"Problemas.", str(errors) + u" archivos no han podido ser transformados.")


#
# folder1 = filedialog.askdirectory(title="Select videos folder")
# if folder1 == "":
#     exit(0)
# folder2 = filedialog.askdirectory(title="Select output folder")
# if folder2 == "":
#     exit(0)
#
# indice = 0
# total = len([name for name in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, name))])
# print(total)
#
# subResultFolder = os.path.split(folder1)[-1]
# audioFolder = os.path.join(folder2, subResultFolder)
# if not os.path.isdir(audioFolder):
#     os.mkdir(audioFolder)
#
# for videoName in os.listdir(folder1):
#     folderAndVideo = os.path.join(folder1, videoName)
#     if os.path.isfile(folderAndVideo):
#         indice += 1
#
#         subName = videoName.split(".")
#         subName[-1] = "mp3"
#         audioName = ".".join(subName)
#
#         folderAndAudio = os.path.join(audioFolder, audioName)
#
#         if os.path.isfile(folderAndAudio):
#             continue
#
#         print("\n")
#         print(videoName + " -> " + audioName)
#         print("\t" + folderAndVideo + " -> " + folderAndAudio)
#         print("\n")
#
#         clip = mp.VideoFileClip(folderAndVideo)
#         clip.audio.write_audiofile(folderAndAudio)
#
#         print("\t" + str(indice) + "/" + str(total) + " ~ " + str(100 * indice / total) + "%")
