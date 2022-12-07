# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)

sudo apt update
sudo apt upgrade
sudo apt autoremove

clear

# If not running interactively, don't do anything
case $- in
    *i*) ;;
    *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac


if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
fi

# Source alias definitions by referencing the alias file
if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't ned to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi

# remove the bash history from the previous session
if test -f "./bash_history"; then
    rm ./bash_history
fi

# The following sets the environment variable for
#	the \[\033[<attribute>;<color code>m\] prefix is used to change colors
#	this can make different sections of the prompt different colors,
#		as well as change the color of text inputs
#	The color codes are as follows:
#		- Black:  30
#		- Blue:   34
#		- Cyan:   36
#		- Green:  32
#		- Purple: 35
#		- Red:    31
#		- White:  37
#		- Yellow: 33
#	The attribute codes are as follows:
#		- Normal Text: Blank/0
#		- Bold/Light:  1
#		- Dim:         2
#		- Underlined:  4
#		- Blinking:    5
#		- Reversed:    7
#		- Hidden:      8
PS1="\[\033[1;35m\]\u@\W ->\[\033[32m\] "

sudo /etc/init.d/dbus start &> /dev/null
