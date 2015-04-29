=============
Twitchy-Term
=============

A simple terminal browser Twitch.tv and watch streams on VLC Player using `Livestreamer <http://docs.livestreamer.io/>`_.

============
Dependencies
============

* Python 3 (tested on version 3.4)
* `Livestreamer <http://docs.livestreamer.io/>`_
* VLC (:code:`sudo apt-get install vlc`)

============
Installation
============

Clone this repository

.. code-block:: bash

   $ git clone https://github.com/Andy-Au/twitchy-term.git
   $ cd twitchy-term
   $ sudo python3 setup.py install

=====
Usage
=====

Simply run:

.. code-block:: bash

   $ twitchy-term

It also takes an optional argument for streaming quality:

.. code-block:: bash

   $ twitchy-term -q [quality]

Available qualities include:

* best
* high
* medium
* low
* worst

Twitchy-Term offers the following pages of Twitch.tv:

* Featured streams (from Twitch.tv's home page)
* Browse top games (and top streams of each)
* Search

----------------
Commands
----------------

:``▲``/``▼``: Scroll up and down the current list of items
:``f``: Featured streams
:``g``: Top Games list
:``s``: Search
:``c``: Change stream quality
:``q``: Quit

::

   In Top Games list

:``e``: View top streams of current selected game

::

   In pages where streams are listed

:``p``: Play the selected stream in VLC player with current quality

=======
License
=======

Please see `LICENSE <https://github.com/Andy-Au/twitchy-term/blob/master/LICENSE>`_.

=============
Twitchy-Term
=============

A simple terminal browser Twitch.tv and watch streams on VLC Player using `Livestreamer <http://docs.livestreamer.io/>`_.

============
Dependencies
============
* Python 3 (tested on version 3.4)
* `Livestreamer <http://docs.livestreamer.io/>`_
* VLC (:code:`sudo apt-get install vlc`)

============
Installation
============

Clone this repository

.. code-block:: bash

   $ git clone https://github.com/Andy-Au/twitchy-term.git
   $ cd twitchy-term
   $ sudo python3 setup.py install

=====
Usage
=====

Simply run:

.. code-block:: bash

   $ twitchy-term

It also takes an optional argument for streaming quality:

.. code-block:: bash

   $ twitchy-term -q [quality]

Available qualities include:

* best
* high
* medium
* low
* worst

Twitchy-Term offers the following pages of Twitch.tv:

* Featured streams (from Twitch.tv's home page)
* Browse top games (and top streams of each)
* Search

----------------
Commands
----------------

:``▲``/``▼``: Scroll up and down the current list of items
:``f``: Featured streams
:``g``: Top Games list
:``s``: Search
:``c``: Change stream quality
:``q``: Quit

::

   In Top Games list

:``e``: View top streams of current selected game

::

   In pages where streams are listed

:``p``: Play the selected stream in VLC player with current quality

=======
License
=======

Please see `LICENSE <https://github.com/Andy-Au/twitchy-term/blob/master/LICENSE>`_.