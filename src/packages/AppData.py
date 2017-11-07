# -*- coding: UTF-8 -*-
from . import GuiManager
from . import GuiGenerator
from . import Transformer
from . import Downloader
import re
import threading
import functools


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
        if "." not in audioOut:
            audioOut += ".mp3"

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
        if not ytUrl or not re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*").search(ytUrl):
            GuiManager.popupWarning("Warning", "Debe ingresar un enlace valido.")
        else:
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
        self.downloaderReady = False
        self.filters = dict()
        hilo = threading.Thread(target=self.downloader.parseYT)
        hilo.start()
        threading.Thread(target=self.parseYTdata, args=[hilo]).start()
        # self.gui.putProgressBar(100)
        return

    def start(self):
        # type: () -> None
        self.gui.addTab("Descargar", GuiGenerator.downloaderSubTab)

        self.gui.comboboxs["downloadOptions"][0]["values"] = ["Cargando..."]
        self.gui.comboboxs["downloadOptions"][0].current(0)

        self.gui.checkbuttons["downloaderSub"][0]["command"] = self.onlyAudioCallback
        self.gui.radios["downloaderSub"][0]["command"] = self.fileTypeCallback
        self.gui.radios["downloaderSub"][1]["command"] = self.videoTypeCallback

        self.gui.overrideClose(self.close)
        self.gui.start()
        return

    def parseYTdata(self, hilo):
        # type: (threading.Thread) -> None
        try:
            c = 0
            while hilo.isAlive():
                c += 1
                continue
            self.downloaderReady = True
            print("ready", c)
            self.applyFilters()
            self.gui.checkbuttons["downloaderSub"][0]["state"] = "normal"
            self.gui.radios["downloaderSub"][0]["state"] = "normal"
            self.gui.radios["downloaderSub"][1]["state"] = "normal"
            self.gui.buttons["downloadOptionsDown"][0]["state"] = "normal"
            self.gui.buttons["downloadOptionsDown"][0]["command"] = self.downloadVideo
            self.downloader.on_download(functools.partial(on_download, gui=self.gui))
        except Exception as err:
            print(err)
            GuiManager.popupError("Error", str(err))
            raise
        return

    def onlyAudioCallback(self):
        # type: () -> None
        while not self.downloaderReady:
            continue
        self.filters["only_audio"] = bool(self.gui.checkbuttons["downloaderSub"][0].is_checked())
        self.applyFilters()
        return

    def fileTypeCallback(self):
        # type: () -> None
        while not self.downloaderReady:
            continue

        selected = self.gui.radios["downloaderSub"][0].getSelected()
        self.filters["progressive"] = False
        self.filters["adaptive"] = False
        if selected == 1:
            self.filters["progressive"] = True
        elif selected == 2:
            self.filters["adaptive"] = True

        self.applyFilters()

    def videoTypeCallback(self):
        # type: () -> None
        while not self.downloaderReady:
            continue

        selected = self.gui.radios["downloaderSub"][1].getSelected()
        if selected == 0:
            if "subtype" in self.filters:
                del self.filters["subtype"]
        elif selected == 1:
            self.filters["subtype"] = "mp4"
        elif selected == 2:
            self.filters["subtype"] = "webm"
        elif selected == 3:
            self.filters["subtype"] = "3gpp"

        self.applyFilters()

        return

    def applyFilters(self):
        # type: () -> None
        values = self.downloader.getValues(**self.filters)
        self.gui.comboboxs["downloadOptions"][0]["values"] = values
        if len(values) > 0:
            self.gui.comboboxs["downloadOptions"][0].current(0)
            self.gui.comboboxs["downloadOptions"][0]["state"] = "readonly"
        else:
            self.gui.comboboxs["downloadOptions"][0]["state"] = "disabled"
        return

    def downloadVideo(self):
        # type: () -> None
        self.gui.buttons["downloadOptionsDown"][0]["state"] = "disabled"
        video = self.gui.comboboxs["downloadOptions"][0].get()
        print(video)
        itag = int(video.split(",")[0])
        outputName = GuiManager.selectFolder("Seleccionar carpeta")
        if outputName:
            kwargs = dict(self.filters)
            kwargs["outputName"] = outputName
            hilo = threading.Thread(target=self.downloader.download, args=[itag], kwargs=kwargs)
            hilo.start()
            # self.downloader.download(itag, outputName=outputName, **self.filters)
        else:
            self.gui.buttons["downloadOptionsDown"][0]["state"] = "normal"
        return

    def isRunning(self):
        # type: () -> bool
        return self.gui.isRunning()

    def close(self):
        # type: () -> None
        self.gui.quit()
        return


def on_download(stream, chunk, file_handle, bytes_remaining, gui):
    # type: (None, bytes, None, int, GuiManager.GuiManager) -> None
    # print("")
    # TODO: Poner Progressbar
    print(bytes_remaining)
    if bytes_remaining == 0:
        GuiManager.popupInfo("Listo", "Descarga satisfactoria")
        gui.quit()
    # if not gui.isProgressNew():
    #     print("if gui.getProgressBarMax() != 0:")
    #     print("max", gui.getProgressBarMax())
    #     print("remaining", bytes_remaining)
    #     newData = gui.getProgressBarMax()-bytes_remaining
    #     newData = int(100.0*newData/gui.getProgressBarMax())
    #     print("newData", newData)
    #     gui.setProgressAmount(newData)
    # else:
    #     print("else:")
    #     gui.setProgressBarMax(bytes_remaining)
    return
