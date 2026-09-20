# OU The Builder — Foundation

This repository is the from-scratch Android foundation for OU The Builder.

## Core rule

UI state must never claim that an operation happened unless the underlying engine performed it.

## Planned modules

- app
- core:model
- core:project
- core:filesystem
- core:ai
- core:build
- core:resources
- feature:chat
- feature:import
- feature:design
- feature:imageflow
- feature:preview
- feature:build
- feature:history
- feature:settings

The first package keeps the Android app in one module so the project can be opened immediately; the modules above are the intended extraction path.

## Project format

Each project will contain:

- project.json
- screens/
- assets/
- source/
- build-config.json
- build-recipes/
- build-logs/

## Cloud

Cloud providers are abstractions. Google Drive is the first planned OAuth/authorization integration. MobiDrive, OneDrive, Dropbox and WebDAV can be added through the same provider interface.

## Storage

Android's Storage Access Framework should be used for user-selected folders and files. Android restricts direct tree access to some shared locations, including Download on modern Android, so the app must use a user-selected directory or an app-controlled storage strategy rather than promising unrestricted access to Download.

## Current status

This is a foundation package, not the completed Builder. The Build screen, AI actions, cloud connections, preview, import engine, and compiler are deliberately not represented as completed until their real implementations exist.
