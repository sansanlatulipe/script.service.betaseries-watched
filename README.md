# Synchronization with BetaSeries

[![GitHub release](https://img.shields.io/github/v/release/sansanlatulipe/script.service.betaseries-watched.svg)](https://github.com/sansanlatulipe/script.service.betaseries-watched/releases)
[![Integration](https://github.com/sansanlatulipe/script.service.betaseries-watched/workflows/Integration/badge.svg)](https://github.com/sansanlatulipe/script.service.betaseries-watched/actions/workflows/integration.yml)
[![Codecov status](https://img.shields.io/codecov/c/github/sansanlatulipe/script.service.betaseries-watched/main)](https://codecov.io/gh/sansanlatulipe/script.service.betaseries-watched/branch/main)

This project is a service addon for Kodi media center.
It automatically updates your profile on BetaSeries when you watched an episode or a movie on Kodi.

## Features

- Synchronize watched movies between BetaSeries and Kodi library
- Synchronize watched TV show episodes between BetaSeries and Kodi library

### To do

- Mark a movie as watched on BetaSeries when a video stream ends
- Mark a TV show episode as watched on BetaSeries when a video stream ends

## How it works

### Quick start

You need a BetaSeries account.

1. Authenicate
    1. Click the "Initialize the connection" action from the addon settings
        This will open a pop-in displaying an authentication code
    2. Go to https://www.betaseries.com/device and follow the authentication steps
    3. Close the pop-in
2. Synchronize
    1. Choose the libraries you want to synchronize (movies and/or TV shows)
        By default, none is selected
    2. Choose if you want BetaSeries to notify your social networks when you watched a media
    3. Save the changes to initialize the synchronization
        - The media marked as watched on BetaSeries are synchronized with your Kodi libraries (if they exist)
        - The media marked as watched on Kodi are synchronized with BetaSeries
    5. From now
        - Every hour, Kodi will check the status of your media in BetaSeries and update your libraries if necessary
        - When the status a media from your libraries changes, Kodi will update it on BetaSeries

### Data protection

Your authentication token is store locally (in Kodi's addon data).

There is no third-party component (like a server) between your Kodi and BetaSeries.

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
3. Open a "Remote Window" (bottom-left icon in VS Code), then "Attach to Running Container..."

### Technical logic

The entry point of this add-on is `service.py`.

Except for this, all code can be found in the directory `resources/lib/`:
- `launcher.py`: launcher functions
- `util/`: some helper classes and functions
- `service/`: business logic
- `infra/`: technical logic, like connection to API or backward compatibily
- `appli/`: glue between `service/` and `infra/`
