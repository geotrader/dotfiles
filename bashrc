#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

PS1='[\u@\h \W]\$ '

JAVA_HOME=/opt/java
export _JAVA_AWT_WM_NONREPARENTING=1
export WINIT_HIDPI_FACTOR=1.0

exec fish
