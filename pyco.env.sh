export PYCO_HOME=/home/adona/dev/pyco

export PYTHONPATH=$PYCO_HOME/src
export PYTHONSTARTUP=$PYCO_HOME/python.shell.env

# to avoid ssh_askpass gui activation when pexpect exceed TIMEOUT
unset DISPLAY
