import XMonad
import XMonad.Util.EZConfig (additionalKeysP)
import qualified XMonad.StackSet as W (view,shift) --for edit client to screen keybind
import XMonad.Actions.WindowGo(runOrRaise)
import XMonad.Actions.SpawnOn(spawnOn)


-- for bar
import XMonad.Hooks.ManageDocks(docks,avoidStruts)
import XMonad.Hooks.EwmhDesktops        (ewmh)

import XMonad.Hooks.DynamicLog
import qualified DBus as D
import qualified DBus.Client as D
import qualified Codec.Binary.UTF8.String as UTF8

-- for taffybar
-- import System.Taffybar.Support.PagerHints (pagerHints)

main :: IO ()
main = do
    dbus <- D.connectSession
    -- Request access to the DBus name
    D.requestName dbus (D.busName_ "org.xmonad.Log")
        [D.nameAllowReplacement, D.nameReplaceExisting, D.nameDoNotQueue]
    -- xmonad $ docks $ ewmh $ pagerHints $ def
    xmonad $ docks $ ewmh $ def
      { terminal = myTerminal
      , modMask = myModMask
      , borderWidth = myBorderWidth
      , startupHook = myStartupHook
      , layoutHook =  myLayoutHook
      , workspaces = myWorkspaces
      , logHook = dynamicLogWithPP (myLogHook dbus)
      } `additionalKeysP` myKeys

myKeys =
    [ ("M-b",spawn "qutebrowser")
    , ("M-c",spawn "rofi -modi \"clipboard:greenclip print\" -show clipboard -run-command '{cmd}'")
    , ("M-s",spawn "steam")
    , ("M-d",spawn "discord-canary")
    , ("M-<Space>",spawn "rofi -show run")
    , ("M-<Return>",spawn myTerminal)
    , ("M-r" ,spawn "xmonad --recompile; xmonad --restart")
    , ("M-q" ,kill)
    , ("M-<Tab>" ,sendMessage NextLayout)
    , ("M-<F8>" ,spawn "pactl set-sink-volume 0 +2%")
    , ("M-<F9>" ,spawn "pactl set-sink-volume 0 -2%")
    , ("M-<F10>" ,spawn "pactl set-sink-volume 0 0%")
    ]
    ++
    [ (otherModMasks ++ "M-" ++ [key], action tag)
      | (tag, key)  <- zip myWorkspaces "312"
      , (otherModMasks, action) <- [ ("", windows . W.view) , ("S-", windows . W.shift)]
    ]

myStartupHook = do
        spawn "pkill pasystray;pasystray"
        spawn "sudo updatedb"
        spawn "pkill greenclip;greenclip daemon"
        spawn "nitrogen --restore"
        spawn "fcitx-autostart"
        spawn "bash ~/.config/myStartup/configOnlyForMyEnv.sh"
        spawn "bash ~/.config/myStartup/myXkbConfig.sh"
        spawn "bash ~/.config/myStartup/SyncDrive.sh"
        spawn "pkill polybar;polybar example"
        -- spawn "pkill taffybar;taffybar"

-- myLayoutHook = tiled ||| Full
myLayoutHook = avoidStruts (tiled ||| Full)
  where
    tiled = Tall nmaster delta ratio
    nmaster = 1
    ratio = 3/5
    delta = 1/100


myTerminal = "termite"
myModMask = mod4Mask -- Win key or SuperL
myBorderWidth = 3 -- active window outline
myWorkspaces = ["1","2","3"]

-- Override the PP values as you would otherwise, adding colors etc depending
-- on  the statusbar used
myLogHook :: D.Client -> PP
myLogHook dbus = def { ppOutput = dbusOutput dbus }

-- Emit a DBus signal on log updates
dbusOutput :: D.Client -> String -> IO ()
dbusOutput dbus str = do
    let signal = (D.signal objectPath interfaceName memberName) {
            D.signalBody = [D.toVariant $ UTF8.decodeString str]
        }
    D.emit dbus signal
  where
    objectPath = D.objectPath_ "/org/xmonad/Log"
    interfaceName = D.interfaceName_ "org.xmonad.Log"
    memberName = D.memberName_ "Update"
