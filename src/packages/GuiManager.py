import os
try:
    import Tkinter as tk
    import ttk
    import tkFileDialog
    import tkMessageBox
except ImportError:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox


def popupInfo(title, text):
    # type: (str, str) -> None
    tkMessageBox.showinfo(title, text)


def popupWarning(title, text):
    # type: (str, str) -> None
    tkMessageBox.showwarning(title, text)


def popupError(title, text):
    # type: (str, str) -> None
    tkMessageBox.showerror(title, text)


def popupYesNo(title, text):
    # type: (str, str) -> bool
    return tkMessageBox.askyesno(title, text)


# askokcancel(text1, text2) -> bool
# askyesno(a, b) -> bool
#    ask yes or no
# askretrycancel(a, b) -> bool
#    ask "retry" or "cancel". has a warning sign
# askyesnocancel(a, b) -> bool
#    ask yes, no or cancel. returns True, False or None respectively


def addMsgToText(txtWid, msg):
    # type: (tk.Text, str) -> None
    txtWid["state"] = "normal"
    txtWid.insert(tk.END, msg + "\n")
    txtWid.see(tk.END)
    txtWid["state"] = "disabled"


def openFile(title, fileTypes, callback=None):
    # type: (str, tuple, (str, )) -> str
    archivo = tkFileDialog.askopenfilename(initialdir="/", title=title, filetypes=fileTypes)
    try:
        print(archivo)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(archivo)
    return archivo


def saveFile(title, fileTypes, callback=None):
    # type: (str, tuple, (str, )) -> str
    archivo = tkFileDialog.asksaveasfilename(initialdir="/", title=title, filetypes=fileTypes)
    try:
        print(archivo)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(archivo)
    return archivo


def selectMultiplesFiles(title, fileTypes, callback=None):
    # type: (str, tuple, (str, )) -> list[str]
    archivos = tkFileDialog.askopenfilenames(initialdir="/", title=title, filetypes=fileTypes)
    if type(archivos) != tuple:
        return list()
    try:
        print(archivos)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(archivos)
    return archivos


def selectFolder(title=None, callback=None):
    # type: (str, (str, )) -> str
    carpeta = tkFileDialog.askdirectory(title=title)
    try:
        print(carpeta)
    except UnicodeEncodeError:
        pass
    if callback:
        callback(carpeta)
    return carpeta


def generateTtkWidget(wtype, master, posT, x, y, values=None, width=None, current=None, command=None, **kwargs):
    # type: (str, ttk.Frame|ttk.LabelFrame, str, int, int, list, int, int, (), **kwargs) -> None|ttk.Label|ttk.Combobox|ttk.Entry|ttk.Button|CheckButton
    if wtype == u"Label":
        widget = ttk.Label(master, **kwargs)
    elif wtype == u"Combobox":
        widget = ttk.Combobox(master, state='disabled', values=values, **kwargs)
        if command:
            widget.bind("<<ComboboxSelected>>", command)
        if current is not None:
            widget.current(current)
    elif wtype == u"Entry":
        widget = ttk.Entry(master, state='disabled', **kwargs)
    elif wtype == u"Button":
        widget = ttk.Button(master, state="disabled", **kwargs)
        if command:
            widget["command"] = command
    elif wtype == u"CheckButton":
        widget = CheckButton(master, state="disabled", onvalue=1, offvalue=0, **kwargs)
        widget.deselect()
        if command:
            widget["command"] = command
    else:
        return
    if posT == u"pack" or posT == u"place":
        widget.pack()
        if width:
            widget.place(x=x, y=y, width=width)
        else:
            widget.place(x=x, y=y)
    elif posT == u"grid":
        if width:
            widget["width"] = width
        widget.grid(row=x, column=y)
    else:
        return
    return widget


def __cleanData(listData):
    # type: (list) -> None
    for data in listData:
        if type(data) == list:
            __cleanData(data)
        else:
            if data.winfo_class() in ("Button", "TButton"):
                data.command = None
            elif data.winfo_class() in ("Checkbutton", ):
                data.deselect()
            elif data.winfo_class() in ("Entry", "TEntry"):
                data.delete(0, "end")
            elif data.winfo_class() in ("Combobox", "TCombobox"):
                data.set('')
            else:
                print(u"Error data")
                print(data)
                print(data.winfo_class())
                print("")
                return
            data["state"] = "disabled"
    return


def cleanData(dictData):
    # type: (dict) -> None
    for key, value in dictData.items():
        # print key, value
        __cleanData(value)
    return


def __disableData(listData):
    # type: (list) -> None
    for data in listData:
        if type(data) == list:
            __cleanData(data)
        else:
            if data.winfo_class() in ("Button", "TButton"):
                data["state"] = "normal"
            elif data.winfo_class() in ("Checkbutton", ):
                data["state"] = "normal"
            elif data.winfo_class() in ("Entry", "TEntry"):
                data["state"] = "normal"
            elif data.winfo_class() in ("Combobox", "TCombobox"):
                data["state"] = "readonly"
            else:
                print(u"Error data")
                print(data)
                print(data.winfo_class())
                print("")
                return
    return


def disableData(dictData):
    # type: (dict) -> None
    for key, value in dictData.items():
        # print key, value
        __disableData(value)
    return


def __enableData(listData):
    # type: (list) -> None
    for data in listData:
        if type(data) == list:
            __cleanData(data)
        else:
            data["state"] = "disabled"
    return


def enableData(dictData):
    # type: (dict) -> None
    for key, value in dictData.items():
        # print key, value
        __enableData(value)
    return


class GuiManager:
    def __init__(self, title=u"Tk", icon=None):
        # type: (str, str) -> None
        self.gui = tk.Tk()
        self.tabsWidth = 0
        self.tabsHeight = 0
        self.running = False
        self.title = title
        self.tabs = ttk.Notebook(self.gui)
        self.tabsData = dict()
        self.comboboxs = dict()
        self.entries = dict()
        self.checkbuttons = dict()
        self.buttons = dict()
        self.radios = dict()
        # self.progressBar = list()
        self.restart = False
        self.icon = icon
        self.closeOverrided = False

    def addTab(self, tabName, tabCallback):
        # type: (str, (GuiManager, ttk.Frame)) -> None
        tab = ttk.Frame(self.tabs)  # , width = self.tabsWidth, height = self.tabsHeight)
        self.tabs.add(tab, text=tabName)
        self.tabsData[tabName] = tab
        newX, newY = tabCallback(self, tab)

        tab["width"] = newX
        tab["height"] = newY

        if newX > self.tabsWidth:
            self.tabsWidth = newX
        if newY > self.tabsHeight:
            self.tabsHeight = newY
        return

    def addMenu(self, cascadeNames, cascadeData):
        # type: (list, list) -> None
        if len(cascadeNames) != len(cascadeData):
            return
        
        menuVar = tk.Menu(self.gui)

        for i in range(len(cascadeNames)):
            subMenu = tk.Menu(menuVar, tearoff=0)
            for optionName, callback in cascadeData[i]:
                if optionName is None:
                    subMenu.add_separator()
                else:
                    if callback:
                        subMenu.add_command(label=optionName, command=callback)
                    else:
                        subMenu.add_command(label=optionName)
            menuVar.add_cascade(label=cascadeNames[i], menu=subMenu)

        self.gui.config(menu=menuVar)

    def start(self, title=None, icon=None):
        # type: (str, str) -> None
        if icon:
            self.icon = icon
        if self.icon:
            # TODO: test on linux
            if os.name == 'nt':
                try:
                    self.gui.wm_iconbitmap(bitmap=self.icon)
                    # img = tk.PhotoImage(file=self.icon)
                except Exception:
                    self.gui.wm_iconbitmap(bitmap=os.path.join("..", self.icon))
                    # img = tk.PhotoImage(file=os.path.join("..", self.icon))
                # self.gui.tk.call('wm', 'iconphoto', self.gui._w, img)

        if title:
            self.title = title
        self.gui.title(self.title)

        self.gui.minsize(self.tabsWidth, self.tabsHeight+25)
        self.running = True
        self.tabs.grid(column=0, row=0)
        if not self.closeOverrided:
            self.overrideClose(self.quit)
        self.gui.mainloop()

    def stop(self):
        # type: () -> None
        if self.running:
            self.clean()
            self.gui.destroy()
        self.closeOverrided = False
        self.tabsData = dict()
        self.gui = tk.Tk()
        self.tabs = ttk.Notebook(self.gui)
        self.running = False
        self.restart = False

    def isRunning(self):
        # type: () -> bool
        return self.running

    def clean(self):
        # type: () -> None
        cleanData(self.comboboxs)
        cleanData(self.checkbuttons)
        cleanData(self.entries)
        cleanData(self.buttons)
        return

    def disableAll(self):
        # type: () -> None
        disableData(self.comboboxs)
        disableData(self.checkbuttons)
        disableData(self.entries)
        disableData(self.buttons)
        return

    def enableAll(self):
        # type: () -> None
        enableData(self.comboboxs)
        enableData(self.checkbuttons)
        enableData(self.entries)
        enableData(self.buttons)
        return

    def overrideClose(self, callback):
        # type: (()) -> None
        self.gui.eval('::ttk::CancelRepeat')
        self.gui.protocol("WM_DELETE_WINDOW", callback)
        self.closeOverrided = True
        return

    # def putProgressBar(self, maxi):
    #     # type: (int) -> None
    #     pb = ttk.Progressbar(self.gui, orient="horizontal", length=self.tabsWidth, mode="determinate", maximum=maxi)
    #     pb.grid(column=0, row=1)
    #     self.progressBar = [pb, maxi]
    #
    # def restartProgressBar(self):
    #     # type: () -> None
    #     if self.progressBar:
    #         self.progressBar[0]["value"] = 0
    #
    # def updateProgressBar(self):
    #     # type: () -> None
    #     if self.progressBar is None:
    #         return
    #     if self.progressBar[0]["value"] > self.progressBar[1]:
    #         self.progressBar[0]["value"] = 0
    #     self.progressBar[0]["value"] += 1

    def isRestart(self):
        # type: () -> bool
        return self.restart

    def setRestart(self, restart):
        # type: (bool) -> None
        self.restart = restart
        return

    def quit(self):
        # type: () -> None
        if self.running:
            self.gui.destroy()
        self.running = False
        return


class CheckButton(tk.Checkbutton):
    def __init__(self, master, *args, **kwargs):
        self.var = kwargs.get('variable', tk.IntVar(master))
        kwargs['variable'] = self.var
        tk.Checkbutton.__init__(self, master, *args, **kwargs)

    def is_checked(self):
        # type: () -> int
        return self.var.get()


class Radiobuttons:
    def __init__(self, master, texts, x, y, **kwargs):
        # type: (ttk.Frame|ttk.LabelFrame, list, list, list, **kwargs) -> None
        length = len(texts)
        if length > len(x) or length > len(y):
            raise ValueError("Len of 'x' or y' is less than 'texts' arg.")

        self.var = kwargs.get('variable', tk.IntVar(master))
        kwargs['variable'] = self.var
        self.radios = list()
        for i in range(len(texts)):
            widget = tk.Radiobutton(master, text=texts[i], value=i, state="disabled",  **kwargs)
            self.radios.append(widget)
            widget.pack()
            widget.place(x=x[i], y=y[i])
        self.radios[0].select()
        return

    def getSelected(self):
        # type: () -> int
        return self.var.get()

    def __setitem__(self, key, value):
        if type(key) != str:
            raise TypeError("Expected 'str', got " + str(type(key)).strip("<class ").strip(">"))
        for i in self.radios:
            i[key] = value
        return
