Introduction
============

This service automatically updates your profile on Betaseries when you have finished watching an episode or a movie on Kodi

Features
========

* Movie synchronization

How it works
============

Entry points
------------

There is several ways to start this add-ons:
* A service (`service.py`) that regularly checks updates from Betaseries and Kodi
* An executable (`addon.py`)
  * By default, it rescans the entire Kodi library and synchronizes with Betaseries on-demand
  * With the option "authentication", it initializes the connection with Betaseries API

Business logic
--------------

### Movie synchronization

#### First scan or full rescan

For each movie stored in the Kodi library, if it is flagged as watched on either side (Kodi or Betaseries), ensure it is true on the other as well.

#### Complementary scans

Firstly, for each updates registered in Kodi (watched or unwatched), duplicate it on Betaseries.
Secondly, for each updates in Betaseries timeline (watched or unwatched), duplicate it on Kodi.

Structure
---------

Except for the entry points, all code can be found in the directory `resources/lib/`:
* `launcher.py`: launcher functions
* `util/`: some helper classes and functions
* `service/`: business logic
* `infra/`: technical logic, like connection to API or backward compatibily
* `appli/`: glue between `service/` and `infra/`
