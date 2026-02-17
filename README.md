Using Bitwig's DAWproject and Transcribe! this script creates warped on-beat tracks from live performance.

## Install
`pip install xsdata[cli,lxml,soap]`
`pip install mido`

## What this repo can do
- Convert a Transcribe! marker file into a dawproject with tempo and time-signature automation.
- Build a dawproject directly from a MIDI file with a full track layout.
- Generate Harmony and Bass arrangement tracks from the MIDI with channel overrides.
- Package a finished `.dawproject` zip with `project.xml` and `metadata.xml`.

## Transcribe! to dawproject
`python transcribe_to_dawproject.py input.dawproject input.xsc`

## MIDI to dawproject
`python midi_to_dawproject.py input.mid output.dawproject`

If you have the setBfree harmony preset, include it:
`python midi_to_dawproject.py input.mid output.dawproject --harmony-state plugins/your_preset.fxb`

## Generate xml template
Download newest [dawproject schema](https://github.com/bitwig/dawproject/blob/main/Project.xsd)
`xsdata generate Project.xsd --package project`
