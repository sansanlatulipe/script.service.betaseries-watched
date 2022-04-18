# Synchronization with Betaseries

[![GitHub release](https://img.shields.io/github/v/release/sansanlatulipe/script.service.betaseries-watched.svg)](https://github.com/sansanlatulipe/script.service.betaseries-watched/releases)
[![Integration](https://github.com/sansanlatulipe/script.service.betaseries-watched/workflows/Integration/badge.svg)](https://github.com/sansanlatulipe/script.service.betaseries-watched/actions/workflows/integration.yml)
[![Codecov status](https://img.shields.io/codecov/c/github/sansanlatulipe/script.service.betaseries-watched/main)](https://codecov.io/gh/sansanlatulipe/script.service.betaseries-watched/branch/main)

This project is a service addon for Kodi media center.
It automatically updates your profile on Betaseries when you have finished watching an episode or a movie on Kodi.

## Features

* Synchronize watched movies between Betaseries and Kodi library
* Synchronize watched TV show episodes between Betaseries and Kodi library

### To do

* Mark a movie as watched on Betaseries when a video stream ends
* Mark a TV show episode as watched on Betaseries when a video stream ends

## How it works

### Business logic

#### Movie synchronization

On first scan.
For each movie stored in the Kodi library, if it is flagged as watched on either side (Kodi or Betaseries), ensure it is true on the other as well.

On complementary scans.
Firstly, for each updates registered in Kodi (watched or unwatched), duplicate it on Betaseries.
Secondly, for each updates in Betaseries timeline (watched or unwatched), duplicate it on Kodi.

### Technical logic

The add-on is launched from `service.py`.

Except for the entry points, all code can be found in the directory `resources/lib/`:
* `launcher.py`: launcher functions
* `util/`: some helper classes and functions
* `service/`: business logic
* `infra/`: technical logic, like connection to API or backward compatibily
* `appli/`: glue between `service/` and `infra/`
