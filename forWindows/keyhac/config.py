import datetime

from keyhac import *


def configure(keymap):

    # --------------------------------------------------------------------
    # Text editer setting for editting config.py file
    if 1:
        keymap.editor = "code"
    # --------------------------------------------------------------------
    # Customizing the display
    keymap.setFont("RictyDiminishedDiscord", 12)
    keymap.setTheme("black")
    # --------------------------------------------------------------------

    # User modifier key definition
    keymap.defineModifier(29, "User0")

    # Global keymap which affects any windows
    if 1:
        keymap_global = keymap.defineWindowKeymap()

        # vim keybind
        keymap_global["O-29"] = 'F7'
        keymap_global["U0-H"] = 'Left'
        keymap_global["U0-J"] = 'Down'
        keymap_global["U0-K"] = 'Up'
        keymap_global["U0-L"] = 'Right'
        keymap_global["U0-Y"] = 'Home'
        keymap_global["U0-N"] = 'End'
        keymap_global["U0-E"] = 'Esc'
        keymap_global["U0-D"] = 'C-W'
        keymap_global["U0-W"] = 'A-F4'
        keymap_global["U0-R"] = 'Apps'
        keymap_global["U0-Enter"] = 'F7', 'Enter'
        keymap_global["U0-Back"] = 'C-A', 'Delete'
        keymap_global["S-U0-R"] = 'S-Apps'

        # USER0-Ctrl-Up/Down/Left/Right : Move active window to screen edges
        keymap_global["U0-C-Left"] = keymap.MoveWindowToMonitorEdgeCommand(0)
        keymap_global["U0-C-Right"] = keymap.MoveWindowToMonitorEdgeCommand(2)
        keymap_global["U0-C-Up"] = keymap.MoveWindowToMonitorEdgeCommand(1)
        keymap_global["U0-C-Down"] = keymap.MoveWindowToMonitorEdgeCommand(3)

        # Clipboard history related
        keymap_global["U0-C"] = keymap.command_ClipboardList     # Open the clipboard history list

        # Keyboard macro
        keymap_global["U0-1"] = keymap.command_RecordStart
        keymap_global["U0-2"] = keymap.command_RecordStop
        keymap_global["U0-3"] = keymap.command_RecordPlay

    # --------------------------------------------------------------------
    # execute or activate applications
    if 1:
        def find_window(class_name):
            def get_window(wnd, arg):
                nonlocal window
                if wnd.isVisible() and not wnd.getOwner():
                    if wnd.getClassName() == class_name:
                        window = wnd
                        return False
                return True
            window = None
            Window.enum(get_window, None)
            return window

        def activate_or_execute(path, class_name=""):
            wnd = find_window(class_name)
            if wnd:
                if wnd.isMinimized():
                    wnd.restore()
                wnd.getLastActivePopup().setForeground()
            else:
                executeFunc = keymap.ShellExecuteCommand(None, path, "", "")
                executeFunc()

        keymap_global["A-E"] = lambda: activate_or_execute('everything')
        keymap_global["A-N"] = lambda: activate_or_execute('cfiler', "CfilerWindowClass")
        keymap_global["A-C"] = lambda: activate_or_execute('qutebrowser', "Qt5QWindowIcon")
        # keymap_global["A-C"] = lambda: activate_or_execute('firefox', "MozillaWindowClass")
        keymap_global["A-S"] = lambda: activate_or_execute('code', "")

    # --------------------------------------------------------------------

    # USER0-F2 : Test of sub thread execution using JobQueue/JobItem
    if 1:
        def command_JobTest():

            def jobTest(job_item):
                shellExecute(None, "notepad.exe", "", "")

            def jobTestFinished(job_item):
                print("Done.")

            job_item = JobItem(jobTest, jobTestFinished)
            JobQueue.defaultQueue().enqueue(job_item)

        keymap_global["U0-F2"] = command_JobTest

    # Customizing clipboard history list
    if 1:
        keymap.clipboard_history.enableHook = True
        keymap.clipboard_history.maxnum = 1000
        keymap.clipboard_history.quota = 10 * 1024 * 1024


        full_width_chars = "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿‘｛｜｝～０１２３４５６７８９　"
        half_width_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}～0123456789 "

        # Convert to half-with characters
        def toHalfWidthClipboardText():
            s = getClipboardText()
            s = s.translate(str.maketrans(full_width_chars, half_width_chars))
            return s

        # Return formatted date-time string
        def dateAndTime(fmt):
            def _dateAndTime():
                return datetime.datetime.now().strftime(fmt)
            return _dateAndTime

        # Menu item list
        useful_items = [
            ("mail_address",     "null@xxx-co.jp"),
            ("YYYY/MM/DD HH:MM:SS",   dateAndTime("%Y/%m/%d %H:%M:%S")),
            ("Paste with Full-Width",              toFullWidthClipboardText),
            ("Edit config.py",             keymap.command_EditConfig),
            ("Reload config.py",           keymap.command_ReloadConfig),
        ]

        # Clipboard history list extensions
        keymap.cblisters += [
            ("useful_items", cblister_FixedPhrase(useful_items)),
        ]


def configure_ListWindow(window):
    window.keymap['J'] = window.command_CursorDown
    window.keymap['K'] = window.command_CursorUp
    window.keymap['Slash'] = window.command_IncrementalSearch
