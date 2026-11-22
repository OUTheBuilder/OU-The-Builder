# OU DJ Studio

Python/Kivy Android DJ mixer project.

## First build

The GitHub Actions workflow builds a debug APK when files under this folder change or when manually started from the Actions tab.

## Current working controls

- Two independent audio decks using Kivy's Android audio backend.
- Load supported local audio files (MP3, WAV, OGG, M4A, FLAC where the device backend supports them).
- Play/pause, stop, cue point, seek, per-deck volume.
- Four user-set hot cue positions per deck.
- Approximate 4-beat loop (fixed 2-second loop at an assumed 120 BPM).
- Equal-power crossfader and master level.

## Important limitations of v1.0

The waveform is a visual rhythm placeholder, not decoded track waveform data. Beat detection, BPM analysis, beat matching, true pitch/time-stretch, EQ, filters, effects, recording, headphone cue routing, stems, and MIDI/USB controller support are not implemented in this first build. Android audio backends and device audio routing vary, so test playback with your device and headphones.

This is an original application and does not include VirtualDJ code, branding, or assets.
