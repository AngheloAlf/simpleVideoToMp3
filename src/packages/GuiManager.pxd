cpdef void popupInfo(unicode title, unicode text)
    # type: (unicode, unicode) -> None

cpdef void popupWarning(unicode title, unicode text)
    # type: (unicode, unicode) -> None

cpdef void popupError(unicode title, unicode text)
    # type: (unicode, unicode) -> None

cpdef bint popupYesNo(unicode title, unicode text)
    # type: (unicode, unicode) -> bool

cpdef void addMsgToText(txtWid, str msg)
    # type: (Tkinter.Text, str) -> None

cpdef unicode openFile(unicode title, tuple fileTypes, callback=*)
    # type: (unicode, tuple, (unicode, )) -> unicode

cpdef unicode saveFile(unicode title, tuple fileTypes, callback=*)
    # type: (unicode, tuple, (unicode, )) -> unicode

cpdef list selectMultiplesFiles(unicode title, tuple fileTypes, callback=*)
    # type: (unicode, tuple, (unicode, )) -> list[unicode]

cpdef unicode selectFolder(unicode title=*, callback=*)
    # type: (unicode, (unicode, )) -> unicode

# cpdef generateTtkWidget(unicode wtype, master, unicode posT, int x, int y, list values=*, int width=*, int current=*, command=*, **kwargs)
    # type: (unicode, ttk.Frame|ttk.LabelFrame, unicode, int, int, list, int, int, function, **kwargs) -> None|ttk.Label|ttk.Combobox|ttk.Entry|ttk.Button|CheckButton

cdef void __cleanData(list listData)
    # type: (list) -> None

cdef void cleanData(dict dictData)
    # type: (dict) -> None

cpdef void __disableData(list listData)
    # type: (list) -> None

cpdef void disableData(dict dictData)
    # type: (dict) -> None

cpdef void __enableData(list listData)
    # type: (list) -> None

cpdef void enableData(dict dictData)
    # type: (dict) -> None

cdef class GuiManager:
    cdef gui
    # gui = Tkinter.Tk()
    cdef int tabsWidth
    cdef int tabsHeight
    cdef bint running
    cdef unicode title
    cdef tabs
    # tabs = ttk.Notebook(self.gui)
    cdef dict tabsData
    cpdef public dict entries
    cpdef public dict comboboxs
    cpdef public dict checkbuttons
    cpdef public dict buttons
    # cdef list progressBar
    cdef bint restart
    cdef unicode icon
    cdef bint closeOverrided

    cpdef void addTab(self, unicode tabName, tabCallback)
        # type: (unicode, (ttk.Frame, dict, dict, dict, dict)) -> None

    cpdef void addMenu(self, list cascadeNames, list cascadeData)
        # type: (list, list) -> None

    cpdef void start(self, unicode title=*, unicode icon=*)
        # type: (unicode, unicode) -> None

    cpdef void stop(self)
        # type: () -> None

    cpdef bint isRunning(self)
        # type: () -> bool

    cpdef void clean(self)
        # type: () -> None

    cpdef void disableAll(self)
        # type: () -> None

    cpdef void enableAll(self)
        # type: () -> None

    cpdef void overrideClose(self, callback)
        # type: (()) -> None

    # cpdef void putProgressBar(self, int maxi)
    #     # type: (int) -> None
    #
    # cpdef void restartProgressBar(self)
    #     # type: () -> None
    #
    # cpdef void updateProgressBar(self)
    #     # type: () -> None

    cpdef bint isRestart(self)
        # type: () -> bool

    cpdef void quit(self)
        # type: () -> None


# cdef class CheckButton:
#     cdef var
#
#     cpdef int is_checked(self)
#         # type: () -> int
