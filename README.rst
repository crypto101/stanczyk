==========
 stanczyk
==========

This is a client for the game-shaped exercises which are part of
Crypto 101, the introductory book on cryptography by lvh_.

.. image:: https://travis-ci.org/crypto101/stanczyk.png
   :target: https://travis-ci.org/crypto101/stanczyk
.. image:: https://coveralls.io/repos/crypto101/stanczyk/badge.png?branch=master
   :target: https://coveralls.io/r/crypto101/stanczyk?branch=master

.. image:: https://dl.dropboxusercontent.com/u/38476311/Logos/stanczyk.jpg

Testing and documentation
=========================

The short version: use tox_.

The long version: see the extra notes for merlyn_.

Changelog
=========

0.0.2
-----

A much nicer version you can actually play around with.

- stanczyk is now continuously tested, thanks to Travis CI. Coverage
  is measured thanks to Coveralls.
- Solution notification: when an exercise is solved, stanczyk will say
  something.
- Exercise listing and exercise details listing commands.
- Proxy commands. You can now connect to remote virtual servers.
- Nicer terminal line overwriting routines, which makes it less
  obvious that stuff is happening asynchronously (sometimes).
- When starting, a nice table is displayed with all of the available
  commands, plus a short description of what they do.

I've made a `short video <http://youtu.be/W_jEIvugwes>`_ that roughly
coincides with this version.

0.0.1
-----

Initial version. Contains a nice basic manhole with no extra commands.

Name and spelling
=================

``stanczyk`` is named after `Stańczyk`_, a historical Polish jester.
Other Crypto 101 projects (such as merlyn_, arthur_ and clarent_) were
already named after things from the court of Arthurian legend; I
picked Stańczyk because:

1. Poland is awesome.
2. This project looks simple, but it's actually pretty clever; perhaps
   more than its peers.
3. Poland is awesome.

The banner is an excerpt from the famous painting of Stańczyk by `Jan
Matejko`_.

.. _lvh: https://twitter.com/lvh/
.. _tox: https://testrun.org/tox/
.. _`Stańczyk`: https://en.wikipedia.org/wiki/Sta%C5%84czyk
.. _merlyn: https://github.com/crypto101/merlyn
.. _arthur: https://github.com/crypto101/arthur
.. _clarent: https://github.com/crypto101/clarent
.. _`Jan Matejko`: https://en.wikipedia.org/wiki/Jan_Matejko
