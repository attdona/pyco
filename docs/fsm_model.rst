.. _fsm_model:

Pyco FSM Model
--------------

Pyco is a event driven system, so starting from now event has the meaning of input. 

The Pyco FSM model looks like a `FSM Mealy <http://en.wikipedia.org/wiki/Mealy_machine>`_ machine:

In the Mealy machine the FSM behavoir depends on input actions, i.e., output depends on input and state.

In Pyco FSM the output depends not only on input and (target) state but may depends on the crossed transition, i.e. depends on the begin state:
in the following figure the event ``password_request`` triggers the transition from ``GROUND`` to ``PASSWORD_SENT`` and runs the ``sendPassword`` action in the (target) state PASSWORD_SENT. 


.. figure:: images/pyco_fsm.png
	
	
The events are external events generated when a device response match a given pattern or internal events generated when some conditions are detected. 

Internal events occours instead when:

* a timeout is triggered because nothing happens when expecting a response (``timeout`` event)
* entering in state ``STATE``: a lowercase(STATE) event ``state`` is generated 	
* a command line ``cmdstr`` is sent to the device: a ``cmdstr`` is generated

In the pyco syntax an event and its associated properties is defined as follow::

	[[[password_event]]]
		pattern     = "(?i)password:[ ]*"
		beginState  = GROUND
		action      = sendPassword
		endState    = PASSWORD_SENT


The `password_event` event is generated when the pattern `(?i)password:[ ]*` is received from the device connection.
the FSM go from `GROUND` to `PASSWORD_SENT` state and the input action `sendPassword` is executed in the `PASSWORD_SENT` state.

`sendPassword` is a pyhton callable, ie. a function or a class with __call__ method.

The signature of the action function is::

 def actionFunction(target)


where target is the device object being accessed by pyco.
The function logic must be whatever but in the usual case
it is realized with few lines of code.

For example the following snippet send the password string to the requesting :py:class:`pyco.device.Device` after doing some
checking and log the action::

 def sendPassword(target):
    
    if target.password is None:
        raise MissingDeviceParameter(target, '%s password undefined' % target.name)
    
    log.debug("[%s] sending password [%s] ..." % (target.name, target.password))
    target.sendLine(target.password)

 
The event action function is searched in the following python modules, returning the first match:

 #. `$PYCO_HOME/handlers.py` python source file
 #. pyco.actions internal package module
 #. pyco.device internal package module


  