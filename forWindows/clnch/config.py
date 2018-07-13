from clnch import *
from pathlib import Path


# common function
def command_Help(info):
    help_path = Path(getAppExePath()).joinpath('doc\\index.html')
    shellExecute(None, str(help_path), "", "")


def configure(window):
    # keymap
    # Ctrl-E で、入力中のファイルパスを編集する
    window.cmd_keymap["C-E"] = window.command.Edit
    # --------------------------------------------------------------------
    window.cmd_keymap["F1"] = command_Help
    window.keymap["A-Space"] = window.command.AutoCompleteToggle
    # --------------------------------------------------------------------
    window.editor = "subl"
    # --------------------------------------------------------------------
    # コマンドを登録する
    window.launcher.command_list += [
        ("", window.command_ConsoleClose),
        ("Cfiler",    window.ShellExecuteCommand(None, "cfiler", "", "")),
        ("FireFox",   window.ShellExecuteCommand(None, "firefox.exe", "", "C:/Program Files/Mozilla Firefox")),
    ]


def configure_ListWindow(window):
    window.keymap["F1"] = command_Help
    window.keymap["J"] = window.command_CusorUp
    window.keymap["S-J"] = window.command_CusorPageUp
    window.keymap["K"] = window.command_CusorDown
    window.keymap["S-K"] = window.command_CusorPageDown
    window.keymap["Slash"] = window.command_IncrementalSearch
