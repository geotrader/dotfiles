import datetime

from keyhac import *


def configure(keymap):

    # --------------------------------------------------------------------
    # Text editer setting for editting config.py file
    if 1:
        keymap.editor = "code"
    # --------------------------------------------------------------------
    # Customizing the display
    keymap.setFont("RictyDiminishedDiscord", 18)
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
        def activate_or_execute(exec_command, exe_name=None, class_name=None, window_text=None, check_func=None, force=False):
            active_window = keymap.ActivateWindowCommand(exe_name, class_name, window_text, check_func, force)
            if active_window() is None:
                return keymap.ShellExecuteCommand(None, exec_command, "", "")()
            else:
                return active_window


        keymap_global["A-E"] = lambda: activate_or_execute('everything',exe_name='Everything.exe')
        keymap_global["A-N"] = lambda: activate_or_execute('cfiler', exe_name='cfiler.exe')
        keymap_global["A-C"] = lambda: activate_or_execute('qutebrowser', exe_name='qutebrowser.exe')
        keymap_global["A-S"] = lambda: activate_or_execute('code', exe_name='Code.exe')

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
