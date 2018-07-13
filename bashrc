#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'
PS1='[\u@\h \W]\$ '

# eval $(thefuck --alias)
JAVA_HOME=/opt/java
export _JAVA_AWT_WM_NONREPARENTING=1

exec fish
