PyCo test environment setup
===========================

The regression test suite of PyCo needs the following requirements:

* a sshd deamon active
* a local user with pyco/pyco as username/password

To test the discovery of a multi-line prompt configure the PS1 variable in the user environment, for example for a bash shell edit the .bashrc file with:

PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h\n\w\$ "

To test the case of a prompt that changes on every command use the following setup in the user environment:

myprompt_counter=1
export PROMPT_COMMAND='myprompt_counter=$((myprompt_counter + 1))'
PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w $myprompt_counter \$ [\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w $myprompt_counter \$ '