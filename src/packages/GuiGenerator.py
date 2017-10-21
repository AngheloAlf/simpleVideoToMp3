# -*- coding: UTF-8 -*-
from . import GuiManager
from tkinter import ttk


def downloadTab(gui, tab):
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)
    xPoss = [25, 60, 260, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    entry = GuiManager.generateTtkWidget(u"Entry", tab, u"place", xPoss[0], yPoss[0], width=500)
    gui.entries["downloadSimple"] = [entry]

    dlButton = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[1], text=u"Descargar video")
    gui.buttons["downloadSimple"] = [dlButton]

    return xPoss[2], yPoss[2]


def transformTab(gui, tab):
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)
    xPoss = [25, 60, 260, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    transButton = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[0], text=u"Transformar video")
    gui.buttons["transformSimple"] = [transButton]
    transButton2 = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[1],
                                                text=u"Transformar videos en una carpeta")
    gui.buttons["transformFolder"] = [transButton2]

    return xPoss[4], yPoss[4]


def downloaderSubTab(gui, tab):
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)
    xPoss = [25, 200, 300, 700, 900]
    yPoss = [30, 60, 90, 120, 150, 210]

    radio1 = GuiManager.Radiobuttons(tab, ["Todos", "Progresive (Junto)", "Adaptative (Por separado)"], [xPoss[0]]*3, yPoss)

    check = GuiManager.generateTtkWidget(u"CheckButton", tab, u"place", xPoss[0], yPoss[3], text=u"Solo audio")
    # check["state"] = "normal"
    gui.checkbuttons["downloaderSub"] = [check]

    radio2 = GuiManager.Radiobuttons(tab, ["Todos", 'mp4', 'webm', '3gpp'], [xPoss[1]]*4, yPoss)
    gui.radios["downloaderSub"] = [radio1, radio2]

    gui.comboboxs["downloadOptions"] = [GuiManager.generateTtkWidget("Combobox", tab, "place", xPoss[2], yPoss[0],
                                        width=500)]

    gui.buttons["downloadOptionsDown"] = [GuiManager.generateTtkWidget("Button", tab, "place", xPoss[2], yPoss[3],
                                                                       text="Descargar")]

    return xPoss[4], yPoss[5]

