# git-distribution

Self-updatable zero-install Pythonic software distribution for Windows.

## Objective

Write a Python app that can run on Windows out-of-box, without the need to install anything else.

Specifically:

- A Windows user isn't required to install any stuff like Python/git
- The app can update itself from its stable git repository
- Devs aren't required to make a Windows build on every commit
- No continuous integration required too
- The regular development process isn't affected in any way
- The way you run the app having Python/git pre-installed isn't affected too

## Windows Install

- Download and unpack https://github.com/zencd/git-distribution/archive/simple.zip
    which is always up-to-date

## Usage

- `app.bat` for the app's main functionality
- `update.bat` to update the app to the most recent version

v3
