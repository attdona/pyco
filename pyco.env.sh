export PYCO_HOME=/home/tt005893/dev/pyco

export PYTHONPATH=$PYCO_HOME/src
export PYTHONSTARTUP=${PYCO_HOME}/cfg/python.shell.env

# to avoid ssh_askpass gui activation when pexpect exceed TIMEOUT
unset DISPLAY
