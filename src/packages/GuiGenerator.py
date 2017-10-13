# -*- coding: UTF-8 -*-
from . import GuiManager
from tkinter import ttk


def downloadTab(gui, tab):
    # type: (GuiManager.GuiManager, ttk.Frame) -> (int, int)
    xPoss = [25, 60, 260, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    dlButton = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[0], text=u"Descargar video")
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
