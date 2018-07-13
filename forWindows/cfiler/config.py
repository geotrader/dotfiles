from cfiler import *
from pathlib import Path


# common function
def command_Help(info):
    help_path = Path(getAppExePath()).joinpath('doc\\index.html')
    shellExecute(None, str(help_path), "", "")


def configure(window):

    # I hate that deletion does not work if items are unselected.
    # --------------------------------------------------------------------
    def command_CustomDelete(info):
        if not window.activeSelectedItems():
            window.command_Select(info)

        window.command_Delete(info)

# --------------------------------------------------------------------
    window.keymap["F1"] = command_Help
    window.keymap["J"] = window.command_CursorDown
    window.keymap["K"] = window.command_CursorUp
    window.keymap["H"] = window.command_GotoParentDir
    window.keymap["L"] = window.command_Enter
    window.keymap["G"] = window.command_CursorTop
    window.keymap["O"] = window.command_ChdirInactivePaneToOther
    window.keymap["X"] = command_CustomDelete
    window.keymap["V"] = window.command_SelectDown
    window.keymap["Apps"] = window.command_ContextMenu
    window.keymap["Slash"] = window.command_IncrementalSearch
    window.keymap["Space"] = window.command_FocusOther
    window.keymap["Colon"] = window.command_CommandLine
    window.keymap["S-V"] = window.command_SelectUp
    window.keymap["S-G"] = window.command_CursorBottom
    window.keymap["S-J"] = window.command_JumpList
    window.keymap["S-Apps"] = window.command_ContextMenuDir
    window.keymap["S-Slash"] = window.command_Search
    window.keymap["C-R"] = window.command_Reload
    window.keymap["C-S-J"] = window.command_JumpInput

    # --------------------------------------------------------------------
    # テキストエディタを設定する

    if 1:  # プログラムのファイルパスを設定 (単純な使用方法)
        window.editor = "subl"

    # --------------------------------------------------------------------
    # テキスト差分エディタを設定する

    if 0:  # プログラムのファイルパスを設定 (単純な使用方法)
        window.diff_editor = "WinMergeU.exe"

    # --------------------------------------------------------------------

    window.jump_list += [
        ("Desktop",       Path.home().joinpath('/Desktop')),
        ("PortableTools", "C:/PortableTools"),
        ("NAS",           "Z:/"),
    ]

    # --------------------------------------------------------------------
    # アーカイブファイルのファイル名パターンとアーカイバの関連付け

    window.archiver_list = [
        ("*.zip *.jar *.apk",  ZipArchiver),
        ("*.7z",               SevenZipArchiver),
        ("*.tgz *.tar.gz",     TgzArchiver),
        ("*.tbz2 *.tar.bz2",   Bz2Archiver),
        ("*.lzh",              LhaArchiver),
        ("*.rar",              RarArchiver),
    ]

    # --------------------------------------------------------------------
    # ファイルアイテムの表示形式

    # 昨日以前については日時、今日については時間、を表示するアイテムの表示形式
    #
    #   引数:
    #       window   : メインウインドウ
    #       item     : アイテムオブジェクト
    #       width    : 表示領域の幅
    #       userdata : ファイルリストの描画中に一貫して使われるユーザデータオブジェクト
    #
    def itemformat_Name_Ext_Size_YYYYMMDDorHHMMSS(window, item, width, userdata):

        if item.isdir():
            str_size = "<DIR>"
        else:
            str_size = "%6s" % getFileSizeString(item.size())

        if not hasattr(userdata, "now"):
            userdata.now = time.localtime()

        t = item.time()
        if t[0] == userdata.now[0] and t[1] == userdata.now[1] and t[2] == userdata.now[2]:
            str_time = "  %02d:%02d:%02d" % (t[3], t[4], t[5])
        else:
            str_time = "%04d/%02d/%02d" % (t[0] % 10000, t[1], t[2])

        str_size_time = "%s %s" % (str_size, str_time)

        width = max(40, width)
        filename_width = width - len(str_size_time)

        if item.isdir():
            body, ext = item.name, None
        else:
            body, ext = splitExt(item.name)

        if ext:
            body_width = min(width, filename_width - 6)
            return (adjustStringWidth(window, body, body_width, ALIGN_LEFT, ELLIPSIS_RIGHT) +
                    adjustStringWidth(window, ext, 6, ALIGN_LEFT, ELLIPSIS_NONE) +
                    str_size_time)
        else:
            return (adjustStringWidth(window, body, filename_width, ALIGN_LEFT, ELLIPSIS_RIGHT) +
                    str_size_time)

    # Z キーで表示されるファイル表示形式リスト
    window.itemformat_list = [
        ("1 : 全て表示 : filename  .ext  99.9K YY/MM/DD HH:MM:SS", itemformat_Name_Ext_Size_YYMMDD_HHMMSS),
        ("2 : 秒を省略 : filename  .ext  99.9K YY/MM/DD HH:MM",    itemformat_Name_Ext_Size_YYMMDD_HHMM),
        ("3 : 日 or 時 : filename  .ext  99.9K YYYY/MM/DD",        itemformat_Name_Ext_Size_YYYYMMDDorHHMMSS),
        ("0 : 名前のみ : filename.ext",                            itemformat_NameExt),
    ]

    # 表示形式の初期設定
    window.itemformat = itemformat_Name_Ext_Size_YYYYMMDDorHHMMSS

    # --------------------------------------------------------------------
    # "CheckEmpty" コマンド
    #   ファイルが入っていない空のディレクトリを検索します。
    #   ディレクトリが入っていても、ファイルが入っていない場合は空とみなします。

    def command_CheckEmpty(info):

        pane = window.activePane()
        location = window.activeFileList().getLocation()
        items = window.activeItems()

        result_items = []
        message = [""]

        def jobCheckEmpty(job_item):

            def printBoth(s):
                print(s)
                message[0] += s + "\n"

            def appendResult(item):
                result_items.append(item)
                printBoth('   %s' % item.getName())

            printBoth('空のディレクトリを検索 :')

            # ビジーインジケータ On
            window.setProgressValue(None)

            for item in items:

                if not item.isdir():
                    continue

                if job_item.isCanceled():
                    break
                if job_item.waitPaused():
                    window.setProgressValue(None)

                empty = True

                for root, dirs, files in item.walk(False):

                    if job_item.isCanceled():
                        break
                    if job_item.waitPaused():
                        window.setProgressValue(None)

                    if not empty:
                        break
                    for file in files:
                        empty = False
                        break

                if empty:
                    appendResult(item)

            message[0] += '\n'
            message[0] += '検索結果をファイルリストに反映しますか？(Enter/Esc):\n'

        def jobCheckEmptyFinished(job_item):

            # ビジーインジケータ Off
            window.clearProgress()

            if job_item.isCanceled():
                print('中断しました.\n')
            else:
                print('Done.\n')

            if job_item.isCanceled():
                return

            result = popResultWindow(window, "検索完了", message[0])
            if not result:
                return

            window.jumpLister(pane, lister_Custom(window, "[empty] ", location, result_items))

        job_item = ckit.JobItem(jobCheckEmpty, jobCheckEmptyFinished)
        window.taskEnqueue(job_item, "CheckEmpty")

    # --------------------------------------------------------------------
    # "CheckDuplicate" コマンド
    #   左右のペイン両方のアイテムを通して、内容が重複するファイルを検索します。
    #   ファイルのサイズが一致するものについて、より詳細に比較を行います。

    def command_CheckDuplicate(info):

        left_location = window.leftFileList().getLocation()
        right_location = window.rightFileList().getLocation()

        left_items = window.leftItems()
        right_items = window.rightItems()

        items = []
        for item in left_items:
            if not item.isdir() and hasattr(item, "getFullpath"):
                items.append([item, None, False])
        for item in right_items:
            if not item.isdir() and hasattr(item, "getFullpath"):
                items.append([item, None, False])

        if len(items) <= 1:
            return

        result_left_items = set()
        result_right_items = set()
        message = [""]

        def jobCheckDuplicate(job_item):

            def printBoth(s):
                print(s)
                message[0] += s + "\n"

            def appendResult(item):
                if item in left_items:
                    result_left_items.add(item)
                    printBoth('   Left: %s' % item.getName())
                else:
                    result_right_items.add(item)
                    printBoth('  Right: %s' % item.getName())

            def leftOrRight(item):
                if item in left_items:
                    return 'Left'
                else:
                    return 'Right'

            printBoth('重複するファイルを検索 :')

            # ビジーインジケータ On
            window.setProgressValue(None)

            # ファイルのMD5値を調べる
            import hashlib
            for i, item in enumerate(items):

                if job_item.isCanceled():
                    break
                if job_item.waitPaused():
                    window.setProgressValue(None)

                digest = hashlib.md5(item[0].open().read(64 * 1024)).hexdigest()
                print('MD5 : %s : %s' % (item[0].getName(), digest))
                items[i][1] = digest

            # ファイルサイズとハッシュでソート
            if not job_item.isCanceled():
                items.sort(key=lambda item: (item[0].size(), item[1]))

            for i in range(len(items)):

                if job_item.isCanceled():
                    break
                if job_item.waitPaused():
                    window.setProgressValue(None)

                item1 = items[i]
                if item1[2]:
                    continue

                dumplicate_items = []
                dumplicate_filenames = [item1[0].getFullpath()]

                for k in range(i + 1, len(items)):

                    if job_item.isCanceled():
                        break
                    if job_item.waitPaused():
                        window.setProgressValue(None)

                    item2 = items[k]
                    if item1[1] != item2[1]:
                        break
                    if item2[2]:
                        continue
                    if item2[0].getFullpath() in dumplicate_filenames:
                        item2[2] = True
                        continue

                    print('比較 : %5s : %s' % (leftOrRight(item1[0]), item1[0].getName()))
                    print('     : %5s : %s …' % (leftOrRight(item2[0]), item2[0].getName()), )

                    try:
                        result = compareFile(item1[0].getFullpath(), item2[0].getFullpath(), shallow=1, schedule_handler=job_item.isCanceled)
                    except CanceledError:
                        print('中断')
                        break

                    if result:
                        print('一致')
                        dumplicate_items.append(item2)
                        dumplicate_filenames.append(item2[0].getFullpath())
                        item2[2] = True
                    else:
                        print('不一致')

                    print('')

                if dumplicate_items:
                    appendResult(item1[0])
                    for item2 in dumplicate_items:
                        appendResult(item2[0])
                    printBoth("")

            message[0] += '\n'
            message[0] += '検索結果をファイルリストに反映しますか？(Enter/Esc):\n'

        def jobCheckDuplicateFinished(job_item):

            # ビジーインジケータ Off
            window.clearProgress()

            if job_item.isCanceled():
                print('中断しました.\n')
            else:
                print('Done.\n')

            if job_item.isCanceled():
                return

            result = popResultWindow(window, "検索完了", message[0])
            if not result:
                return

            window.leftJumpLister(lister_Custom(window, "[duplicate] ", left_location, list(result_left_items)))
            window.rightJumpLister(lister_Custom(window, "[duplicate] ", right_location, list(result_right_items)))

        job_item = ckit.JobItem(jobCheckDuplicate, jobCheckDuplicateFinished)
        window.taskEnqueue(job_item, "CheckDuplicate")

    # --------------------------------------------------------------------
    # "CheckSimilar" コマンド
    #   左右のペイン両方のアイテムを通して、名前が似ているファイルを検索します。

    def command_CheckSimilar(info):

        left_location = window.leftFileList().getLocation()
        right_location = window.rightFileList().getLocation()
        left_items = window.leftItems()
        right_items = window.rightItems()
        items = left_items + right_items

        result_left_items = set()
        result_right_items = set()
        message = [""]

        def jobCheckSimilar(job_item):

            def printBoth(s):
                print(s)
                message[0] += s + "\n"

            def appendResult(item):
                if item in left_items:
                    result_left_items.add(item)
                    printBoth('   Left: %s' % item.getName())
                else:
                    result_right_items.add(item)
                    printBoth('  Right: %s' % item.getName())

            printBoth('名前が似ているファイルを検索 :')

            # ビジーインジケータ On
            window.setProgressValue(None)

            def to_charset(item):
                return (item, set(item.getName().lower()))
            item_charset_list = map(to_charset, items)

            for i in range(len(item_charset_list) - 1):

                if job_item.isCanceled():
                    break
                if job_item.waitPaused():
                    window.setProgressValue(None)

                item_charset1 = item_charset_list[i]
                for k in range(i + 1, len(item_charset_list)):

                    if job_item.isCanceled():
                        break
                    if job_item.waitPaused():
                        window.setProgressValue(None)

                    item_charset2 = item_charset_list[k]
                    or_set = item_charset1[1].union(item_charset2[1])
                    and_set = item_charset1[1].intersection(item_charset2[1])
                    score = float(len(and_set)) / float(len(or_set))

                    if score >= 0.90:
                        appendResult(item_charset1[0])
                        appendResult(item_charset2[0])
                        printBoth('')

            message[0] += '\n'
            message[0] += '検索結果をファイルリストに反映しますか？(Enter/Esc):\n'

        def jobCheckSimilarFinished(job_item):

            # ビジーインジケータ Off
            window.clearProgress()

            if job_item.isCanceled():
                print('中断しました.\n')
            else:
                print('Done.\n')

            if job_item.isCanceled():
                return

            result = popResultWindow(window, "検索完了", message[0])
            if not result:
                return

            window.leftJumpLister(lister_Custom(window, "[similar] ", left_location, list(result_left_items)))
            window.rightJumpLister(lister_Custom(window, "[similar] ", right_location, list(result_right_items)))

        job_item = ckit.JobItem(jobCheckSimilar, jobCheckSimilarFinished)
        window.taskEnqueue(job_item, "CheckSimilar")

    # Alternertive touch
    # I hate delimiter semicolon.Because I replaced semicolon to enter.
    # --------------------------------------------------------------------
    def command_Touch(info):
        directory = Path(str(window.activeCursorItem())).parent
        file_name = Path('newfile_named_by_Cfiler')
        new_file_path = Path.joinpath(directory, file_name)

        Path.touch(new_file_path)
        window.activeJump(str(new_file_path.as_posix()))
        window.command_Rename(info)

    # --------------------------------------------------------------------
    # コマンドランチャにコマンドを登録する

    window.launcher.command_list += [
        ("Help",              command_Help),
        ("CheckEmpty",        command_CheckEmpty),
        ("CheckDuplicate",    command_CheckDuplicate),
        ("CheckSimilar",      command_CheckSimilar),
        ("touch",             command_Touch),
    ]


def configure_TextViewer(window):
    window.keymap["F1"] = command_Help
    window.keymap["Q"] = window.command_Closeh


def configure_DiffViewer(window):
    window.keymap["F1"] = command_Help
    window.keymap["Q"] = window.command_Cancel


def configure_ImageViewer(window):
    window.keymap["F1"] = command_Help
    window.keymap["Q"] = window.command_Cancel


def configure_ListWindow(window):
    window.keymap["F1"] = command_Help
    window.keymap["Q"] = window.command_Cancel
    window.keymap["J"] = window.command_CursorDown
    window.keymap["K"] = window.command_CursorUp
    window.keymap["G"] = window.command_CursorBottom
    window.keymap["Slash"] = window.command_IncrementalSearch
    window.keymap["S-G"] = window.command_CursorTop
