.. _fsm_model:

Pyco FSM Model
--------------

Pyco is an event driven system, so in the following explanation the term `event` has the same meaning of `input`. 

The Pyco FSM model looks like a `FSM Mealy <http://en.wikipedia.org/wiki/Mealy_machine>`_ machine:

* in the Mealy machine, the FSM behavoir depends on input actions, i.e. output depends on state and input;

* in the Pyco FSM the output depends on input and (target) state,  but it may also depend on the transition being crossed, i.e. it may depend also on the beginning state.

In the picture below the event ``password_request`` triggers the transition from the ``GROUND`` state to the ``PASSWORD_SENT`` state and runs the ``sendPassword`` action in the (target) state ``PASSWORD_SENT``. 


.. figure:: images/pyco_fsm.png
	
	
Events in Pyco are either external events (generated when a device response matches a given pattern) or internal events (generated when some conditions are detected). 

Internal events occur in the following cases:

* when a timeout is triggered because nothing happens for too much time while expecting a response (``timeout`` event);
* when entering a new state: in that case Pyco generates an event named as the lowercase version of state's name (i.e. state ``NEWSTATE`` results in event ``newstate``); 
* when a command string is sent to the device: Pyco generates an event named as the command string.

Using the Pyco syntax, an event and its related properties are defined as follows::

	[[[password_event]]]
		pattern     = "(?i)password:[ ]*"
		beginState  = GROUND
		action      = sendPassword
		endState    = PASSWORD_SENT


With this definition, event `password_event` is then generated when the pattern `(?i)password:[ ]*` is matched in the output from the device.
The FSM performs a transition from the ``GROUND`` state to the ``PASSWORD_SENT`` state, and then executes the action `sendPassword`.

Actions are Pyhton callables, i.e. a function or a class having a ``__call__`` method.

The signature of the action is the following::

 def actionFunction(target)

where ``target`` is the instance of the object representing the device being accessed by Pyco.
There are no constraints on what an action may perform, but it's customary to
keep them short.

For example, the following snippet performs some checking, logs the action and then sends the password string to the requesting :py:class:`pyco.device.Device`::

 def sendPassword(target):
    
    if target.password is None:
        raise MissingDeviceParameter(target, 
				     '%s password undefined' % target.name)
    
    log.debug("[%s] sending password [%s] ..." % (target.name, target.password))
    target.sendLine(target.password)

 
The action definition is searched in the following Python modules, stopping at the first match:

 #. ``$PYCO_HOME/handlers.py`` python source file
 #. pyco.actions internal package module
 #. pyco.device internal package module


  
