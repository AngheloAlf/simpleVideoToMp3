# -*- coding: UTF-8 -*-
from . import GuiManager
from . import GuiGenerator
from . import Transformer
from . import Downloader


# TODO: Añadir progress bar y threads para que no explote mientras transforma.
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
        self.gui.entries["downloadSimple"][0]["state"] = "normal"
        self.gui.buttons["downloadSimple"][0]["state"] = "normal"
        self.gui.buttons["downloadSimple"][0]["command"] = self.downloadVideo

        self.gui.addTab("Transformar", GuiGenerator.transformTab)
        self.gui.buttons["transformSimple"][0]["command"] = self.transformVideo
        self.gui.buttons["transformSimple"][0]["state"] = "normal"
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
            self.closeSubGui()
            print(u"\nCerrando...\n")
            self.gui.quit()
        return

    def closeSubGui(self):
        # type: () -> bool
        if self.subGui and self.subGui.isRunning():
            self.subGui.close()
            return True
        return False

    def transformFolder(self):
        # type: () -> None
        folderSrc = GuiManager.selectFolder(u"Seleccione su carpeta de videos")
        if not folderSrc:
            return
        folderOut = GuiManager.selectFolder(u"Seleccione su carpeta de destino")
        if not folderOut:
            return
        if "." not in folderOut:
            folderOut += ".mp3"

        self.gui.disableAll()
        errors = Transformer.FolderTransformer(folderSrc, folderOut).transform()
        self.gui.enableAll()
        if errors == 0:
            GuiManager.popupInfo(u"Exito.", u"Se han transformado todos sus videos.")
        else:
            GuiManager.popupWarning(u"Problemas.", str(errors) + u" archivos no han podido ser transformados.")
        return

    def transformVideo(self):
        # type: () -> None
        videoSrc = GuiManager.openFile(u"Seleccione su video.", (("MP4", "*.mp4"), ("Todo", "*.*")))
        if not videoSrc:
            return
        audioOut = GuiManager.saveFile(u"Indique el nombre del archivo final.", (("MP3", "*.mp3"), ("Todo", "*.*")))
        if not audioOut:
            return

        self.gui.disableAll()
        success = Transformer.Transformer(videoSrc, audioOut).transform()
        self.gui.enableAll()
        if success:
            GuiManager.popupInfo(u"Exito.", u"Se ha transformado su video exitosamente..")
        else:
            GuiManager.popupWarning(u"Problemas.", u"Su archivo no han podido ser transformado.")
        return

    def downloadVideo(self):
        # type: () -> None
        ytUrl = self.gui.entries["downloadSimple"][0].get()
        self.closeSubGui()
        self.subGui = DownloadManager(ytUrl)
        self.subGui.start()
        return

# total = len([name for name in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, name))])


class DownloadManager:
    def __init__(self, ytUrl):
        # type: (str) -> None
        self.gui = GuiManager.GuiManager("Descargar")
        self.ytUrl = ytUrl
        self.downloader = Downloader.Downloader(self.ytUrl)
        return

    def start(self):
        # type: () -> None
        self.gui.addTab("Descargar", GuiGenerator.downloaderSubTab)
        # self.gui.entries["downloadSimple"][0]["state"] = "normal"
        # self.gui.buttons["downloadSimple"][0]["state"] = "normal"
        # self.gui.buttons["downloadSimple"][0]["command"] = self.downloadVideo

        self.gui.overrideClose(self.close)
        self.gui.start()
        return

    def isRunning(self):
        # type: () -> bool
        return self.gui.isRunning()

    def close(self):
        # type: () -> None
        self.gui.quit()
        return
