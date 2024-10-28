# Synchronization with Betaseries

[![GitHub release](https://img.shields.io/github/v/release/sansanlatulipe/script.service.betaseries-watched.svg)](https://github.com/sansanlatulipe/script.service.betaseries-watched/releases)
[![Integration](https://github.com/sansanlatulipe/script.service.betaseries-watched/workflows/Integration/badge.svg)](https://github.com/sansanlatulipe/script.service.betaseries-watched/actions/workflows/integration.yml)
[![Codecov status](https://img.shields.io/codecov/c/github/sansanlatulipe/script.service.betaseries-watched/main)](https://codecov.io/gh/sansanlatulipe/script.service.betaseries-watched/branch/main)

This project is a service addon for Kodi media center.
It automatically updates your profile on BetaSeries when you have finished watching an episode or a movie on Kodi.

## Features

- Synchronize watched movies between BetaSeries and Kodi library
- Synchronize watched TV show episodes between BetaSeries and Kodi library

### To do

- Mark a movie as watched on BetaSeries when a video stream ends
- Mark a TV show episode as watched on BetaSeries when a video stream ends

## How it works

### Business logic

#### Library synchronization

On first scan.
For each video stored in the Kodi library, if it is flagged as watched on either side (Kodi or BetaSeries), ensure it is true on the other as well.

On complementary scans.
Firstly, for each updates registered in Kodi (watched or unwatched), duplicate it on BetaSeries.
Secondly, for each updates in BetaSeries timeline (watched or unwatched), duplicate it on Kodi.

### Technical logic

The entry point of this add-on is `service.py`.

Except for this, all code can be found in the directory `resources/lib/`:
- `launcher.py`: launcher functions
- `util/`: some helper classes and functions
- `service/`: business logic
- `infra/`: technical logic, like connection to API or backward compatibily
- `appli/`: glue between `service/` and `infra/`

## How to contribute

In order to limit the number of thing to install directly on the workstation,
the development environment is encapsulated in Docker.

### Prerequisites

- Windows Subsystem for Linux + Debian
- Docker Desktop
- Visual Studio, with the following extensions
    - Docker
    - Dev Containers

### Start the local environment

1. Build image from Dockerfile.dev
2. Run a container from this image
    Better done from Docker Desktop to configure volumes and ports
3. Open a "Remote Window" (bottom-left icon in VS Code), then "Attach to Running Container..."
