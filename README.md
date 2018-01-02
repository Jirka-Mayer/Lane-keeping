Lane keeping
============

Lane keeping assistant for the game "18 Wheels of Steel Convoy".

Under prototyping...


Notes
-----

- model output normalization defines upper limit on steering angle, check that for tight curves
- try different model architecture
- try tweaking steering offset of shifted and rotated training data frames


Disabling fullscreen
--------------------

In `%User%/Documents/18 Wos Convoy/config.cfg` set:

    uset r_fullscreen "0"


Hiding HUD
----------

Open in-game console <kbd>;</kbd> and type:

    ui t hud
