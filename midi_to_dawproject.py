#!/usr/bin/env python3

from __future__ import annotations

import typer
import contextlib
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from zipfile import ZipFile

import mido
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from project import (
    Application,
    Arrangement,
    AutomationTarget,
    Audio,
    BoolParameter,
    BuiltinDevice,
    Channel,
    Clip,
    Clips,
    ClipSlot,
    ContentType,
    DeviceRole,
    FileReference,
    Interpolation,
    Lanes,
    Markers,
    MixerRole,
    Note,
    Notes,
    Points,
    Project,
    RealParameter,
    RealPoint,
    Scene,
    Send,
    SendType,
    TimeSignatureParameter,
    TimeSignaturePoint,
    TimeUnit,
    Track,
    Transport,
    Unit,
    Vst2Plugin,
)


@dataclass
class NoteEvent:
    start_beats: float
    duration_beats: float
    channel: int
    key: int
    velocity: int


class IdGenerator:
    def __init__(self) -> None:
        self._counter = 0

    def next(self) -> str:
        value = f"id{self._counter}"
        self._counter += 1
        return value


METADATA_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<MetaData>
    <Title></Title>
    <Artist></Artist>
    <Album></Album>
    <OriginalArtist></OriginalArtist>
    <Songwriter></Songwriter>
    <Producer></Producer>
    <Year></Year>
    <Genre></Genre>
    <Copyright></Copyright>
    <Comment></Comment>
</MetaData>
"""


def format_float(value: float) -> str:
    return f"{value:.6f}"


def clamp_midi_key(value: int) -> int:
    return max(0, min(127, value))


@dataclass
class AudioInfo:
    channels: int
    sample_rate: int
    duration_seconds: float


def read_audio_info(path: Path) -> AudioInfo:
    with contextlib.closing(wave.open(str(path), "rb")) as wav_file:
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        frames = wav_file.getnframes()
        duration_seconds = frames / float(sample_rate) if sample_rate else 0.0
    return AudioInfo(
        channels=channels,
        sample_rate=sample_rate,
        duration_seconds=duration_seconds,
    )


def collect_midi_events(
    mid: mido.MidiFile,
) -> Tuple[List[Tuple[int, float]], List[Tuple[int, int, int]]]:
    tempo_events: List[Tuple[int, float]] = []
    ts_events: List[Tuple[int, int, int]] = []
    for track in mid.tracks:
        abs_tick = 0
        for msg in track:
            abs_tick += msg.time
            if msg.type == "set_tempo":
                tempo_events.append((abs_tick, mido.tempo2bpm(msg.tempo)))
            elif msg.type == "time_signature":
                ts_events.append((abs_tick, msg.numerator, msg.denominator))
    return tempo_events, ts_events


def collect_notes(mid: mido.MidiFile) -> Tuple[Dict[int, List[NoteEvent]], float]:
    ticks_per_beat = mid.ticks_per_beat
    notes_by_channel: Dict[int, List[NoteEvent]] = {0: [], 1: [], 2: [], 3: []}
    open_notes: Dict[int, Dict[int, List[Tuple[int, int]]]] = {
        0: {},
        1: {},
        2: {},
        3: {},
    }
    max_tick = 0

    for track in mid.tracks:
        abs_tick = 0
        for msg in track:
            abs_tick += msg.time
            max_tick = max(max_tick, abs_tick)
            if msg.type not in {"note_on", "note_off"}:
                continue
            if msg.channel not in notes_by_channel:
                continue
            if msg.type == "note_on" and msg.velocity > 0:
                open_notes[msg.channel].setdefault(msg.note, []).append(
                    (abs_tick, msg.velocity)
                )
                continue
            if msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                pending = open_notes[msg.channel].get(msg.note, [])
                if not pending:
                    continue
                start_tick, velocity = pending.pop(0)
                duration_ticks = max(0, abs_tick - start_tick)
                notes_by_channel[msg.channel].append(
                    NoteEvent(
                        start_beats=start_tick / ticks_per_beat,
                        duration_beats=duration_ticks / ticks_per_beat,
                        channel=msg.channel,
                        key=msg.note,
                        velocity=velocity,
                    )
                )

    max_beats = max_tick / ticks_per_beat if ticks_per_beat else 0.0
    for channel, by_key in open_notes.items():
        for key, pending in by_key.items():
            for start_tick, velocity in pending:
                duration_ticks = max(0, max_tick - start_tick)
                notes_by_channel[channel].append(
                    NoteEvent(
                        start_beats=start_tick / ticks_per_beat,
                        duration_beats=duration_ticks / ticks_per_beat,
                        channel=channel,
                        key=key,
                        velocity=velocity,
                    )
                )

    for channel in notes_by_channel:
        notes_by_channel[channel].sort(key=lambda note: note.start_beats)

    return notes_by_channel, max_beats


def make_real_parameter(
    param_id: str,
    name: str,
    value: float,
    unit: Unit,
    min_value: float,
    max_value: float,
) -> RealParameter:
    return RealParameter(
        id=param_id,
        name=name,
        value=format_float(value),
        unit=unit,
        min=format_float(min_value),
        max=format_float(max_value),
    )


def make_bool_parameter(param_id: str, name: str, value: bool) -> BoolParameter:
    return BoolParameter(id=param_id, name=name, value=value)


def make_send(send_id: str, enable_id: str, volume_id: str, destination: str) -> Send:
    return Send(
        id=send_id,
        destination=destination,
        type_value=SendType.POST,
        enable=make_bool_parameter(enable_id, "Enable", False),
        volume=make_real_parameter(volume_id, "Send", 0.0, Unit.LINEAR, 0.0, 1.0),
    )


def make_channel(
    channel_id: str,
    destination: Optional[str],
    role: MixerRole,
    volume_value: float,
    id_gen: IdGenerator,
    send_destination: Optional[str] = None,
    device: Optional[BuiltinDevice] = None,
) -> Channel:
    sends = None
    if send_destination:
        sends = Channel.Sends(
            send=[
                make_send(
                    id_gen.next(),
                    id_gen.next(),
                    id_gen.next(),
                    send_destination,
                )
            ]
        )

    devices = None
    if device:
        devices = Channel.Devices(builtin_device=[device])

    return Channel(
        id=channel_id,
        audio_channels=2,
        destination=destination,
        role=role,
        solo=False,
        devices=devices,
        mute=make_bool_parameter(id_gen.next(), "Mute", False),
        pan=make_real_parameter(id_gen.next(), "Pan", 0.5, Unit.NORMALIZED, 0.0, 1.0),
        sends=sends,
        volume=make_real_parameter(
            id_gen.next(), "Volume", volume_value, Unit.LINEAR, 0.0, 2.0
        ),
    )


def make_builtin_device(
    device_id: str,
    name: str,
    device_name: str,
    id_gen: IdGenerator,
) -> BuiltinDevice:
    return BuiltinDevice(
        id=id_gen.next(),
        device_id=device_id,
        device_name=device_name,
        device_role=DeviceRole.INSTRUMENT,
        loaded=True,
        name=name,
        parameters=BuiltinDevice.Parameters(),
        enabled=make_bool_parameter(id_gen.next(), "On/Off", True),
    )


def make_vst2_device(
    device_id: str,
    name: str,
    device_name: str,
    id_gen: IdGenerator,
    state_path: Optional[str] = None,
) -> Vst2Plugin:
    return Vst2Plugin(
        id=id_gen.next(),
        device_id=device_id,
        device_name=device_name,
        device_role=DeviceRole.INSTRUMENT,
        loaded=True,
        name=name,
        parameters=Vst2Plugin.Parameters(),
        enabled=make_bool_parameter(id_gen.next(), "On/Off", True),
        state=FileReference(path=state_path) if state_path else None,
    )


def build_notes(
    events: Iterable[NoteEvent],
    channel_override: Optional[int] = None,
    key_offset: int = 0,
) -> List[Note]:
    notes: List[Note] = []
    for event in sorted(events, key=lambda item: item.start_beats):
        channel = channel_override if channel_override is not None else event.channel
        key = clamp_midi_key(event.key + key_offset)
        velocity = event.velocity / 127.0
        notes.append(
            Note(
                time=format_float(event.start_beats),
                duration=format_float(event.duration_beats),
                channel=channel,
                key=key,
                vel=format_float(velocity),
                rel=format_float(velocity),
            )
        )
    return notes


def make_clip(
    track_name: str, notes: List[Note], duration: float, id_gen: IdGenerator
) -> Clip:
    return Clip(
        time=0.0,
        duration=duration,
        play_start=0.0,
        loop_start=0.0,
        loop_end=duration,
        enable=True,
        name=track_name,
        notes=Notes(id=id_gen.next(), note=notes),
    )


def make_lanes(track_id: str, clips: Optional[Clips], id_gen: IdGenerator) -> Lanes:
    return Lanes(id=id_gen.next(), track=track_id, clips=[clips] if clips else [])


def make_clips(clip: Optional[Clip], id_gen: IdGenerator) -> Clips:
    return Clips(id=id_gen.next(), clip=[clip] if clip else [])


def make_audio_clip(
    audio_path: Path,
    tempo_bpm: float,
    id_gen: IdGenerator,
) -> Tuple[Clip, float]:
    audio_info = read_audio_info(audio_path)
    duration_beats = audio_info.duration_seconds * tempo_bpm / 60.0
    clip_name = audio_path.stem
    audio_file = Audio(
        id=id_gen.next(),
        algorithm="raw",
        channels=audio_info.channels,
        sample_rate=audio_info.sample_rate,
        duration=audio_info.duration_seconds,
        file=FileReference(path=f"audio/{audio_path.name}"),
    )
    inner_clip = Clip(
        time=0.0,
        duration=duration_beats,
        content_time_unit=TimeUnit.SECONDS,
        play_start=0.0,
        play_stop=audio_info.duration_seconds,
        fade_time_unit=TimeUnit.BEATS,
        fade_in_time=0.0,
        fade_out_time=0.0,
        audio=audio_file,
    )
    outer_clip = Clip(
        time=0.0,
        duration=duration_beats,
        play_start=0.0,
        fade_time_unit=TimeUnit.BEATS,
        fade_in_time=0.0,
        fade_out_time=0.0,
        enable=True,
        name=clip_name,
        clips=Clips(id=id_gen.next(), clip=[inner_clip]),
    )
    return outer_clip, duration_beats


def build_tempo_points(
    tempo_events: List[Tuple[int, float]],
    ticks_per_beat: int,
    tempo_param_id: str,
    id_gen: IdGenerator,
) -> Points:
    points: List[RealPoint] = []
    events = sorted(tempo_events, key=lambda item: item[0])
    if not events:
        events = [(0, 120.0)]
    if events[0][0] != 0:
        events.insert(0, (0, events[0][1]))
    for tick, bpm in events:
        time_beats = tick / ticks_per_beat if ticks_per_beat else 0.0
        points.append(
            RealPoint(
                time=format_float(time_beats),
                value=format_float(bpm),
                interpolation=Interpolation.HOLD,
            )
        )
    return Points(
        id=id_gen.next(),
        unit=Unit.BPM,
        target=AutomationTarget(parameter=tempo_param_id),
        real_point=points,
    )


def build_time_signature_points(
    ts_events: List[Tuple[int, int, int]],
    ticks_per_beat: int,
    ts_param_id: str,
    id_gen: IdGenerator,
) -> Points:
    events = sorted(ts_events, key=lambda item: item[0])
    if not events:
        events = [(0, 4, 4)]
    if events[0][0] != 0:
        events.insert(0, (0, events[0][1], events[0][2]))
    points = [
        TimeSignaturePoint(
            time=format_float(tick / ticks_per_beat if ticks_per_beat else 0.0),
            numerator=numerator,
            denominator=denominator,
        )
        for tick, numerator, denominator in events
    ]
    return Points(
        id=id_gen.next(),
        target=AutomationTarget(parameter=ts_param_id),
        time_signature_point=points,
    )


def build_project(
    midi_path: Path,
    harmony_state: Optional[Path] = None,
    vocal_audio: Optional[Path] = None,
) -> Project:
    mid = mido.MidiFile(midi_path)
    tempo_events, ts_events = collect_midi_events(mid)
    notes_by_channel, max_beats = collect_notes(mid)

    ticks_per_beat = mid.ticks_per_beat

    id_gen = IdGenerator()
    tempo_param_id = id_gen.next()
    ts_param_id = id_gen.next()

    if tempo_events:
        tempo_events_sorted = sorted(tempo_events, key=lambda item: item[0])
        tempo_value = tempo_events_sorted[0][1]
    else:
        tempo_value = 120.0

    if ts_events:
        ts_events_sorted = sorted(ts_events, key=lambda item: item[0])
        ts_numerator = ts_events_sorted[0][1]
        ts_denominator = ts_events_sorted[0][2]
    else:
        ts_numerator = 4
        ts_denominator = 4

    vocal_clip: Optional[Clip] = None
    vocal_duration_beats: Optional[float] = None
    if vocal_audio:
        vocal_clip, vocal_duration_beats = make_audio_clip(
            vocal_audio,
            tempo_value,
            id_gen,
        )
        if vocal_duration_beats is not None:
            max_beats = max(max_beats, vocal_duration_beats)

    transport = Transport(
        tempo=make_real_parameter(
            tempo_param_id,
            "Tempo",
            tempo_value,
            Unit.BPM,
            20.0,
            666.0,
        ),
        time_signature=TimeSignatureParameter(
            id=ts_param_id,
            numerator=ts_numerator,
            denominator=ts_denominator,
        ),
    )

    master_channel_id = id_gen.next()
    fx_channel_id = id_gen.next()
    group_channel_id = id_gen.next()

    melody_device = make_builtin_device(
        "7a0a94df-3aa4-4bb5-8e24-2511999871ad",
        "Flute vs Trumpet",
        "FM-4",
        id_gen,
    )
    harmony_device = make_vst2_device(
        "493825326",
        "setBfree DSP Tonewheel Organ",
        "setBfree DSP Tonewheel Organ",
        id_gen,
        state_path=(f"plugins/{harmony_state.name}" if harmony_state else None),
    )
    bass_device = make_builtin_device(
        "468bc14b-b2e7-45a1-9666-e83117fe404e",
        "Electric Bass - Fingered",
        "Sampler",
        id_gen,
    )
    rhythm_device = make_builtin_device(
        "8ea97e45-0255-40fd-bc7e-94419741e9d1",
        "Acoustic Drums Kit Brushed Clean",
        "Drum Machine",
        id_gen,
    )

    group_track_id = id_gen.next()
    soprano_track_id = id_gen.next()
    alto_track_id = id_gen.next()
    tenor_track_id = id_gen.next()
    bass_track_id = id_gen.next()
    melody_track_id = id_gen.next()
    harmony_track_id = id_gen.next()
    bass_inst_track_id = id_gen.next()
    rhythm_track_id = id_gen.next()
    vocal_track_id = id_gen.next() if vocal_audio else None
    fx_track_id = id_gen.next()
    master_track_id = id_gen.next()

    group_track = Track(
        id=group_track_id,
        name="Group 1",
        color="#5761c6",
        comment="",
        content_type=[ContentType.TRACKS],
        loaded=True,
        channel=make_channel(
            group_channel_id,
            master_channel_id,
            MixerRole.MASTER,
            1.0,
            id_gen,
            send_destination=fx_channel_id,
        ),
    )

    soprano_track = Track(
        id=soprano_track_id,
        name="Soprano",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            group_channel_id,
            MixerRole.REGULAR,
            0.316228,
            id_gen,
            send_destination=fx_channel_id,
            device=make_builtin_device(
                "f2dcfe9a-7b66-4c84-984a-b25685a1c21a",
                "Organ",
                "Organ",
                id_gen,
            ),
        ),
    )
    alto_track = Track(
        id=alto_track_id,
        name="Alto",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            group_channel_id,
            MixerRole.REGULAR,
            0.316228,
            id_gen,
            send_destination=fx_channel_id,
            device=make_builtin_device(
                "f2dcfe9a-7b66-4c84-984a-b25685a1c21a",
                "Organ",
                "Organ",
                id_gen,
            ),
        ),
    )
    tenor_track = Track(
        id=tenor_track_id,
        name="Tenor",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            group_channel_id,
            MixerRole.REGULAR,
            0.316228,
            id_gen,
            send_destination=fx_channel_id,
            device=make_builtin_device(
                "f2dcfe9a-7b66-4c84-984a-b25685a1c21a",
                "Organ",
                "Organ",
                id_gen,
            ),
        ),
    )
    bass_track = Track(
        id=bass_track_id,
        name="Bass",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            group_channel_id,
            MixerRole.REGULAR,
            0.316228,
            id_gen,
            send_destination=fx_channel_id,
            device=make_builtin_device(
                "f2dcfe9a-7b66-4c84-984a-b25685a1c21a",
                "Organ",
                "Organ",
                id_gen,
            ),
        ),
    )

    group_track.track = [soprano_track, alto_track, tenor_track, bass_track]

    melody_track = Track(
        id=melody_track_id,
        name="Melody",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            master_channel_id,
            MixerRole.REGULAR,
            0.16405,
            id_gen,
            send_destination=fx_channel_id,
            device=melody_device,
        ),
    )
    harmony_channel = make_channel(
        id_gen.next(),
        master_channel_id,
        MixerRole.REGULAR,
        0.59013,
        id_gen,
        send_destination=fx_channel_id,
    )
    harmony_channel.devices = Channel.Devices(vst2_plugin=[harmony_device])
    harmony_track = Track(
        id=harmony_track_id,
        name="Harmony",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=harmony_channel,
    )
    bass_inst_track = Track(
        id=bass_inst_track_id,
        name="Bass",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            master_channel_id,
            MixerRole.REGULAR,
            0.466902,
            id_gen,
            send_destination=fx_channel_id,
            device=bass_device,
        ),
    )
    rhythm_track = Track(
        id=rhythm_track_id,
        name="Rhythm",
        comment="",
        content_type=[ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            id_gen.next(),
            master_channel_id,
            MixerRole.REGULAR,
            0.316228,
            id_gen,
            send_destination=fx_channel_id,
            device=rhythm_device,
        ),
    )
    vocal_track = None
    if vocal_track_id:
        vocal_track = Track(
            id=vocal_track_id,
            name="Vocal",
            color="#a37943",
            comment="",
            content_type=[ContentType.AUDIO],
            loaded=True,
            channel=make_channel(
                id_gen.next(),
                master_channel_id,
                MixerRole.REGULAR,
                0.316228,
                id_gen,
                send_destination=fx_channel_id,
            ),
        )
    fx_track = Track(
        id=fx_track_id,
        name="FX 1",
        comment="",
        content_type=[ContentType.AUDIO],
        loaded=True,
        channel=make_channel(
            fx_channel_id,
            master_channel_id,
            MixerRole.EFFECT,
            1.0,
            id_gen,
            send_destination=fx_channel_id,
        ),
    )
    master_track = Track(
        id=master_track_id,
        name="Master",
        comment="",
        content_type=[ContentType.AUDIO, ContentType.NOTES],
        loaded=True,
        channel=make_channel(
            master_channel_id,
            None,
            MixerRole.MASTER,
            1.0,
            id_gen,
        ),
    )

    project_tracks = [
        group_track,
        melody_track,
        harmony_track,
        bass_inst_track,
        rhythm_track,
    ]
    if vocal_track:
        project_tracks.append(vocal_track)
    project_tracks.extend([fx_track, master_track])

    def clip_duration(notes: List[Note]) -> float:
        if not notes:
            return max_beats
        last_end = max(
            float(note.time or 0.0) + float(note.duration or 0.0) for note in notes
        )
        return max(last_end, max_beats)

    soprano_notes = build_notes(notes_by_channel[0])
    alto_notes = build_notes(notes_by_channel[1])
    tenor_notes = build_notes(notes_by_channel[2])
    bass_notes = build_notes(notes_by_channel[3])

    melody_notes = build_notes(notes_by_channel[0], key_offset=12)
    harmony_notes = build_notes(
        notes_by_channel[0]
        + notes_by_channel[1]
        + notes_by_channel[2]
        + notes_by_channel[3],
        channel_override=1,
        key_offset=12,
    )
    bass_inst_notes = build_notes(
        notes_by_channel[3], channel_override=1, key_offset=-12
    )

    arrangement_lanes = Lanes(id=id_gen.next(), time_unit=TimeUnit.BEATS)
    lanes_list: List[Lanes] = [
        make_lanes(group_track_id, make_clips(None, id_gen), id_gen),
        make_lanes(
            soprano_track_id,
            make_clips(
                make_clip(
                    "Soprano",
                    soprano_notes,
                    clip_duration(soprano_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(
            alto_track_id,
            make_clips(
                make_clip(
                    "Alto",
                    alto_notes,
                    clip_duration(alto_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(
            tenor_track_id,
            make_clips(
                make_clip(
                    "Tenor",
                    tenor_notes,
                    clip_duration(tenor_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(
            bass_track_id,
            make_clips(
                make_clip(
                    "Bass",
                    bass_notes,
                    clip_duration(bass_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(
            melody_track_id,
            make_clips(
                make_clip(
                    "Melody",
                    melody_notes,
                    clip_duration(melody_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(
            harmony_track_id,
            make_clips(
                make_clip(
                    "Harmony",
                    harmony_notes,
                    clip_duration(harmony_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(
            bass_inst_track_id,
            make_clips(
                make_clip(
                    "Bass",
                    bass_inst_notes,
                    clip_duration(bass_inst_notes),
                    id_gen,
                ),
                id_gen,
            ),
            id_gen,
        ),
        make_lanes(rhythm_track_id, make_clips(None, id_gen), id_gen),
    ]
    if vocal_track_id:
        lanes_list.append(
            make_lanes(vocal_track_id, make_clips(vocal_clip, id_gen), id_gen)
        )
    lanes_list.extend(
        [
            make_lanes(fx_track_id, make_clips(None, id_gen), id_gen),
            make_lanes(master_track_id, make_clips(None, id_gen), id_gen),
        ]
    )
    arrangement_lanes.lanes = lanes_list

    arrangement = Arrangement(
        id=id_gen.next(),
        lanes=arrangement_lanes,
        tempo_automation=build_tempo_points(
            tempo_events,
            ticks_per_beat,
            tempo_param_id,
            id_gen,
        ),
        time_signature_automation=build_time_signature_points(
            ts_events,
            ticks_per_beat,
            ts_param_id,
            id_gen,
        ),
    )

    scene_lanes = Lanes(id=id_gen.next())
    scene_track_ids = [
        group_track_id,
        soprano_track_id,
        alto_track_id,
        tenor_track_id,
        bass_track_id,
        melody_track_id,
        harmony_track_id,
        bass_inst_track_id,
        rhythm_track_id,
    ]
    if vocal_track_id:
        scene_track_ids.append(vocal_track_id)
    scene_track_ids.extend([fx_track_id, master_track_id])
    scene_lanes.clip_slot = [
        ClipSlot(id=id_gen.next(), track=track_id, has_stop=True)
        for track_id in scene_track_ids
    ]

    scenes = Project.Scenes(
        scene=[Scene(id=id_gen.next(), name="Scene 1", comment="", lanes=scene_lanes)]
    )

    project = Project(
        version="1.0",
        application=Application(name="Bitwig Studio", version="5.3.13"),
        transport=transport,
        structure=Project.Structure(track=project_tracks),
        arrangement=arrangement,
        scenes=scenes,
    )

    return project


def write_dawproject(
    project: Project,
    output_path: Path,
    harmony_state: Optional[Path] = None,
    vocal_audio: Optional[Path] = None,
) -> None:
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    project_xml = serializer.render(project)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with ZipFile(output_path, "w") as zip_file:
        zip_file.writestr("project.xml", project_xml)
        zip_file.writestr("metadata.xml", METADATA_XML)
        if harmony_state:
            zip_file.write(
                harmony_state,
                f"plugins/{harmony_state.name}",
            )
        if vocal_audio:
            zip_file.write(vocal_audio, f"audio/{vocal_audio.name}")


app = typer.Typer(help="Convert MIDI to a Bitwig dawproject.")


@app.command()
def main(
    midi: Path = typer.Argument(..., help="Input MIDI file"),
    output: Path = typer.Argument(..., help="Output .dawproject file"),
    harmony_state: Optional[Path] = typer.Option(
        None,
        "--harmony-state",
        help="Optional setBfree .fxb file for Harmony track",
    ),
    vocal_audio: Optional[Path] = typer.Option(
        None,
        "--vocal-audio",
        help="Optional vocal audio file to include",
    ),
) -> None:
    if harmony_state and not harmony_state.exists():
        raise FileNotFoundError(f"Harmony state file not found: {harmony_state}")
    if vocal_audio and not vocal_audio.exists():
        raise FileNotFoundError(f"Vocal audio file not found: {vocal_audio}")
    project = build_project(
        midi,
        harmony_state=harmony_state,
        vocal_audio=vocal_audio,
    )
    write_dawproject(
        project,
        output,
        harmony_state=harmony_state,
        vocal_audio=vocal_audio,
    )


if __name__ == "__main__":
    app()
