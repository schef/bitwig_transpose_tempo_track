from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional, Union


@dataclass
class Application:
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class ClipSlot:
    has_stop: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasStop",
            "type": "Attribute",
            "required": True,
        }
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class File:
    path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Marker:
    time: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Mute:
    value: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Pan:
    max: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    min: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class RealPoint:
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    interpolation: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    time: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Target:
    parameter: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Tempo:
    max: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    min: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class TimeSignature:
    denominator: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    numerator: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class TimeSignaturePoint:
    numerator: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    denominator: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    time: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Volume:
    max: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    min: Optional[Decimal] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[Union[Decimal, float]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Warp:
    time: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    content_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "contentTime",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Audio:
    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    channels: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    sample_rate: Optional[int] = field(
        default=None,
        metadata={
            "name": "sampleRate",
            "type": "Attribute",
            "required": True,
        }
    )
    duration: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    file: Optional[File] = field(
        default=None,
        metadata={
            "name": "File",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Markers:
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    marker: Optional[Marker] = field(
        default=None,
        metadata={
            "name": "Marker",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Send:
    destination: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    volume: Optional[Volume] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class TempoAutomation:
    unit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    target: Optional[Target] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "required": True,
        }
    )
    real_point: List[RealPoint] = field(
        default_factory=list,
        metadata={
            "name": "RealPoint",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class TimeSignatureAutomation:
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    target: Optional[Target] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "required": True,
        }
    )
    time_signature_point: List[TimeSignaturePoint] = field(
        default_factory=list,
        metadata={
            "name": "TimeSignaturePoint",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Transport:
    tempo: Optional[Tempo] = field(
        default=None,
        metadata={
            "name": "Tempo",
            "type": "Element",
            "required": True,
        }
    )
    time_signature: Optional[TimeSignature] = field(
        default=None,
        metadata={
            "name": "TimeSignature",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Sends:
    send: Optional[Send] = field(
        default=None,
        metadata={
            "name": "Send",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Warps:
    content_time_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentTimeUnit",
            "type": "Attribute",
            "required": True,
        }
    )
    time_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "timeUnit",
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    audio: Optional[Audio] = field(
        default=None,
        metadata={
            "name": "Audio",
            "type": "Element",
            "required": True,
        }
    )
    warp: List[Warp] = field(
        default_factory=list,
        metadata={
            "name": "Warp",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Channel:
    audio_channels: Optional[int] = field(
        default=None,
        metadata={
            "name": "audioChannels",
            "type": "Attribute",
            "required": True,
        }
    )
    destination: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    role: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    solo: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    mute: Optional[Mute] = field(
        default=None,
        metadata={
            "name": "Mute",
            "type": "Element",
            "required": True,
        }
    )
    pan: Optional[Pan] = field(
        default=None,
        metadata={
            "name": "Pan",
            "type": "Element",
            "required": True,
        }
    )
    sends: Optional[Sends] = field(
        default=None,
        metadata={
            "name": "Sends",
            "type": "Element",
        }
    )
    volume: Optional[Volume] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Clip:
    time: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    duration: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    content_time_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentTimeUnit",
            "type": "Attribute",
        }
    )
    play_start: Optional[float] = field(
        default=None,
        metadata={
            "name": "playStart",
            "type": "Attribute",
            "required": True,
        }
    )
    fade_time_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "fadeTimeUnit",
            "type": "Attribute",
            "required": True,
        }
    )
    fade_in_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "fadeInTime",
            "type": "Attribute",
            "required": True,
        }
    )
    fade_out_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "fadeOutTime",
            "type": "Attribute",
            "required": True,
        }
    )
    warps: Optional[Warps] = field(
        default=None,
        metadata={
            "name": "Warps",
            "type": "Element",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    clips: Optional["Clips"] = field(
        default=None,
        metadata={
            "name": "Clips",
            "type": "Element",
        }
    )


@dataclass
class Clips:
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    clip: Optional[Clip] = field(
        default=None,
        metadata={
            "name": "Clip",
            "type": "Element",
        }
    )


@dataclass
class Track:
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Attribute",
            "required": True,
        }
    )
    loaded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    channel: Optional[Channel] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Lanes:
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    time_unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "timeUnit",
            "type": "Attribute",
        }
    )
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    clips: Optional[Clips] = field(
        default=None,
        metadata={
            "name": "Clips",
            "type": "Element",
        }
    )
    lanes: List["Lanes"] = field(
        default_factory=list,
        metadata={
            "name": "Lanes",
            "type": "Element",
        }
    )
    clip_slot: List[ClipSlot] = field(
        default_factory=list,
        metadata={
            "name": "ClipSlot",
            "type": "Element",
        }
    )


@dataclass
class Structure:
    track: List[Track] = field(
        default_factory=list,
        metadata={
            "name": "Track",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Arrangement:
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    lanes: Optional[Lanes] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
            "required": True,
        }
    )
    markers: Optional[Markers] = field(
        default=None,
        metadata={
            "name": "Markers",
            "type": "Element",
            "required": True,
        }
    )
    tempo_automation: Optional[TempoAutomation] = field(
        default=None,
        metadata={
            "name": "TempoAutomation",
            "type": "Element",
            "required": True,
        }
    )
    time_signature_automation: Optional[TimeSignatureAutomation] = field(
        default=None,
        metadata={
            "name": "TimeSignatureAutomation",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Scene:
    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    lanes: Optional[Lanes] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
            "required": True,
        }
    )


@dataclass
class Scenes:
    scene: List[Scene] = field(
        default_factory=list,
        metadata={
            "name": "Scene",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Project:
    version: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    application: Optional[Application] = field(
        default=None,
        metadata={
            "name": "Application",
            "type": "Element",
            "required": True,
        }
    )
    transport: Optional[Transport] = field(
        default=None,
        metadata={
            "name": "Transport",
            "type": "Element",
            "required": True,
        }
    )
    structure: Optional[Structure] = field(
        default=None,
        metadata={
            "name": "Structure",
            "type": "Element",
            "required": True,
        }
    )
    arrangement: Optional[Arrangement] = field(
        default=None,
        metadata={
            "name": "Arrangement",
            "type": "Element",
            "required": True,
        }
    )
    scenes: Optional[Scenes] = field(
        default=None,
        metadata={
            "name": "Scenes",
            "type": "Element",
            "required": True,
        }
    )
