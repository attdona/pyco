export PYCO_HOME=/opt/pyco

export PYTHONPATH=$PYCO_HOME/src
export PYTHONSTARTUP=/opt/pyco/cfg/python.shell.env

# to avoid ssh_askpass gui activation when pexpect exceed TIMEOUT
unset DISPLAY
