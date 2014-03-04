tue_wit_integration
===================

Integrates wit.ai with the Amigo robot of TU Eindhoven. 
Wit.ai interprets a sentences and returns the intention and its parameters.
This project converts an Wit.ai interpretation to actions for Amigo (and possibly its successor).

Some commands it understands:

- Amigo, change your color to red
- Amigo, go to the kitchen
- Amigo, give me a beer (Holy grail of personal robotics)
- Amigo, hello --> it greets you back.

[Demonstration video](http://youtu.be/fxQsYPI6PyI?t=1m7s)

Before giving a command, you must first say the name of the robot ("Amigo"), so it starts listening for a command. 

This ROS-node is easily extensible by writing an new interpretation for your wit.ai intent.
This class must be added to a mapping which links the intent-name to its interpretation class. 
