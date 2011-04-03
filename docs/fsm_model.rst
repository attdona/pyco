.. _fsm_model:

Pyco FSM Model
--------------

The Pyco FSM model looks like a `FSM Mealy <http://en.wikipedia.org/wiki/Mealy_machine>`_ machine:

In the Mealy machine the FSM uses only input actions, i.e., output depends on input and state.

Pyco is a event driven system, so starting from now event has the meaning of input. 

In Pyco FSM the output depends not only on input and (target) state but may depends on the crossed transition, i.e. depends on the begin state:
in the following figure the event ``password_request`` triggers the transition from ``GROUND`` to ``PASSWORD_SENT`` and runs the ``sendPassword`` action in the (target) state PASSWORD_SENT. 


.. figure:: images/pyco_fsm.png
	
	
The events are external events generated when a device response match a given pattern or internal events generated when some conditions are detected. 

Examples of internal events are the ``timeout`` event or a lowercase(STATE) event ``state`` when entering in state ``STATE``. 	

The ``password_request`` event is generated when the pattern ``"Password:[ ]*"`` is received from the opened device connection.

The input action sendPassword is executed entering in the PASSWORD_SENT.

sendPassword is a pyhton callable, ie. a function or a class with __call__ method.

The signature of the action function is::

 def actionFunction(target)


where target is the device object being accessed by pyco.
The function logic must be whatever but in the usual case
it is realized with few lines of code.

For example the following snippet send the password string to the requesting device after doing some
checking and log the action::

 def sendPassword(target):
    
    if target.password is None:
        raise MissingDeviceParameter(target, '%s password undefined' % target.name)
    
    log.debug("[%s] sending password [%s] ..." % (target.name, target.password))
    target.sendLine(target.password)
 


  