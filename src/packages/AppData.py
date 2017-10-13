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
        if "." not in folderOut:
            folderOut += ".mp3"

        self.gui.disableAll()
        errors = Transformer.FolderTransformer(folderSrc, folderOut).transform()
        self.gui.enableAll()
        if errors == 0:
            GuiManager.popupInfo(u"Exito.", u"Se han transformado todos sus videos.")
        else:
            GuiManager.popupWarning(u"Problemas.", str(errors) + u" archivos no han podido ser transformados.")

    def transformVideo(self):
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

# total = len([name for name in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, name))])
