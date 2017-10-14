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
    xPoss = [25, 60, 160, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    gui.radios["downloaderSub"] = [GuiManager.Radiobuttons(tab, 2, ["Progresive", "Adaptative"], [xPoss[0], xPoss[0]],
                                                           yPoss)]

    check = GuiManager.generateTtkWidget(u"CheckButton", tab, u"place", xPoss[0], yPoss[2], text=u"Solo audio")
    check["state"] = "normal"
    gui.checkbuttons["downloaderSub"] = [check]

    gui.radios["downloaderSub"] = [GuiManager.Radiobuttons(tab, 3, ['mp4', 'webm', '3gpp'],
                                                           [xPoss[2], xPoss[2], xPoss[2]], yPoss)]

    return xPoss[5], yPoss[5]

