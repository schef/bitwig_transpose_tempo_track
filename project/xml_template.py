from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


@dataclass
class Application:
    class Meta:
        name = "application"

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


class ContentType(Enum):
    AUDIO = "audio"
    AUTOMATION = "automation"
    NOTES = "notes"
    VIDEO = "video"
    MARKERS = "markers"
    TRACKS = "tracks"


class DeviceRole(Enum):
    INSTRUMENT = "instrument"
    NOTE_FX = "noteFX"
    AUDIO_FX = "audioFX"
    ANALYZER = "analyzer"


class EqBandType(Enum):
    HIGH_PASS = "highPass"
    LOW_PASS = "lowPass"
    BAND_PASS = "bandPass"
    HIGH_SHELF = "highShelf"
    LOW_SHELF = "lowShelf"
    BELL = "bell"
    NOTCH = "notch"


class ExpressionType(Enum):
    GAIN = "gain"
    PAN = "pan"
    TRANSPOSE = "transpose"
    TIMBRE = "timbre"
    FORMANT = "formant"
    PRESSURE = "pressure"
    CHANNEL_CONTROLLER = "channelController"
    CHANNEL_PRESSURE = "channelPressure"
    POLY_PRESSURE = "polyPressure"
    PITCH_BEND = "pitchBend"
    PROGRAM_CHANGE = "programChange"


@dataclass
class FileReference:
    class Meta:
        name = "fileReference"

    path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    external: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


class Interpolation(Enum):
    HOLD = "hold"
    LINEAR = "linear"


class MixerRole(Enum):
    REGULAR = "regular"
    MASTER = "master"
    EFFECT = "effect"
    SUBMIX = "submix"
    VCA = "vca"


@dataclass
class Nameable:
    class Meta:
        name = "nameable"

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    color: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Point1:
    class Meta:
        name = "point"

    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


class SendType(Enum):
    PRE = "pre"
    POST = "post"


class TimeUnit(Enum):
    BEATS = "beats"
    SECONDS = "seconds"


class Unit(Enum):
    LINEAR = "linear"
    NORMALIZED = "normalized"
    PERCENT = "percent"
    DECIBEL = "decibel"
    HERTZ = "hertz"
    SEMITONES = "semitones"
    SECONDS = "seconds"
    BEATS = "beats"
    BPM = "bpm"


@dataclass
class Warp1:
    class Meta:
        name = "warp"

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
class Point(Point1):
    pass


@dataclass
class Warp(Warp1):
    pass


@dataclass
class AutomationTarget:
    class Meta:
        name = "automationTarget"

    parameter: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    expression: Optional[ExpressionType] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    channel: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    key: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    controller: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class BoolPoint1(Point1):
    class Meta:
        name = "boolPoint"

    value: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class EnumPoint1(Point1):
    class Meta:
        name = "enumPoint"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class IntegerPoint1(Point1):
    class Meta:
        name = "integerPoint"

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class Marker1(Nameable):
    class Meta:
        name = "marker"

    time: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class RealPoint1(Point1):
    class Meta:
        name = "realPoint"

    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    interpolation: Optional[Interpolation] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Referenceable(Nameable):
    class Meta:
        name = "referenceable"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class TimeSignaturePoint1(Point1):
    class Meta:
        name = "timeSignaturePoint"

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


@dataclass
class BoolPoint(BoolPoint1):
    pass


@dataclass
class EnumPoint(EnumPoint1):
    pass


@dataclass
class IntegerPoint(IntegerPoint1):
    pass


@dataclass
class Marker(Marker1):
    pass


@dataclass
class RealPoint(RealPoint1):
    pass


@dataclass
class TimeSignaturePoint(TimeSignaturePoint1):
    pass


@dataclass
class Lane(Referenceable):
    class Meta:
        name = "lane"


@dataclass
class Parameter(Referenceable):
    class Meta:
        name = "parameter"

    parameter_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "parameterID",
            "type": "Attribute",
        }
    )


@dataclass
class Timeline1(Referenceable):
    class Meta:
        name = "timeline"

    time_unit: Optional[TimeUnit] = field(
        default=None,
        metadata={
            "name": "timeUnit",
            "type": "Attribute",
        }
    )
    track: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Timeline(Timeline1):
    pass


@dataclass
class BoolParameter1(Parameter):
    class Meta:
        name = "boolParameter"

    value: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class ClipSlot1(Timeline1):
    class Meta:
        name = "clipSlot"

    clip: Optional["Clip"] = field(
        default=None,
        metadata={
            "name": "Clip",
            "type": "Element",
        }
    )
    has_stop: Optional[bool] = field(
        default=None,
        metadata={
            "name": "hasStop",
            "type": "Attribute",
        }
    )


@dataclass
class EnumParameter1(Parameter):
    class Meta:
        name = "enumParameter"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    labels: List[str] = field(
        default_factory=list,
        metadata={
            "type": "Attribute",
            "tokens": True,
        }
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class IntegerParameter1(Parameter):
    class Meta:
        name = "integerParameter"

    max: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    min: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Markers(Timeline1):
    class Meta:
        name = "markers"

    marker: List[Marker] = field(
        default_factory=list,
        metadata={
            "name": "Marker",
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class MediaFile(Timeline1):
    class Meta:
        name = "mediaFile"

    file: Optional[FileReference] = field(
        default=None,
        metadata={
            "name": "File",
            "type": "Element",
            "namespace": "",
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


@dataclass
class Points1(Timeline1):
    class Meta:
        name = "points"

    target: Optional[AutomationTarget] = field(
        default=None,
        metadata={
            "name": "Target",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    point: List[Point] = field(
        default_factory=list,
        metadata={
            "name": "Point",
            "type": "Element",
        }
    )
    real_point: List[RealPoint] = field(
        default_factory=list,
        metadata={
            "name": "RealPoint",
            "type": "Element",
        }
    )
    enum_point: List[EnumPoint] = field(
        default_factory=list,
        metadata={
            "name": "EnumPoint",
            "type": "Element",
        }
    )
    bool_point: List[BoolPoint] = field(
        default_factory=list,
        metadata={
            "name": "BoolPoint",
            "type": "Element",
        }
    )
    integer_point: List[IntegerPoint] = field(
        default_factory=list,
        metadata={
            "name": "IntegerPoint",
            "type": "Element",
        }
    )
    time_signature_point: List[TimeSignaturePoint] = field(
        default_factory=list,
        metadata={
            "name": "TimeSignaturePoint",
            "type": "Element",
        }
    )
    unit: Optional[Unit] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class RealParameter1(Parameter):
    class Meta:
        name = "realParameter"

    max: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    min: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    unit: Optional[Unit] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class TimeSignatureParameter1(Parameter):
    class Meta:
        name = "timeSignatureParameter"

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


@dataclass
class BoolParameter(BoolParameter1):
    pass


@dataclass
class ClipSlot(ClipSlot1):
    pass


@dataclass
class EnumParameter(EnumParameter1):
    pass


@dataclass
class IntegerParameter(IntegerParameter1):
    pass


@dataclass
class Points(Points1):
    pass


@dataclass
class RealParameter(RealParameter1):
    pass


@dataclass
class TimeSignatureParameter(TimeSignatureParameter1):
    pass


@dataclass
class Audio1(MediaFile):
    class Meta:
        name = "audio"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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


@dataclass
class EqBand:
    class Meta:
        name = "eqBand"

    freq: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Freq",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Gain",
            "type": "Element",
            "namespace": "",
        }
    )
    q: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Q",
            "type": "Element",
            "namespace": "",
        }
    )
    enabled: Optional[BoolParameter1] = field(
        default=None,
        metadata={
            "name": "Enabled",
            "type": "Element",
            "namespace": "",
        }
    )
    type_value: Optional[EqBandType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
            "required": True,
        }
    )
    order: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Send(Referenceable):
    class Meta:
        name = "send"

    pan: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Pan",
            "type": "Element",
            "namespace": "",
        }
    )
    volume: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    destination: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    type_value: Optional[SendType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Attribute",
        }
    )


@dataclass
class Transport:
    class Meta:
        name = "transport"

    tempo: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Tempo",
            "type": "Element",
            "namespace": "",
        }
    )
    time_signature: Optional[TimeSignatureParameter1] = field(
        default=None,
        metadata={
            "name": "TimeSignature",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Video1(MediaFile):
    class Meta:
        name = "video"

    algorithm: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
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


@dataclass
class Audio(Audio1):
    pass


@dataclass
class Video(Video1):
    pass


@dataclass
class Device1(Referenceable):
    class Meta:
        name = "device"

    parameters: Optional["Device1.Parameters"] = field(
        default=None,
        metadata={
            "name": "Parameters",
            "type": "Element",
            "namespace": "",
        }
    )
    enabled: Optional[BoolParameter1] = field(
        default=None,
        metadata={
            "name": "Enabled",
            "type": "Element",
            "namespace": "",
        }
    )
    state: Optional[FileReference] = field(
        default=None,
        metadata={
            "name": "State",
            "type": "Element",
            "namespace": "",
        }
    )
    device_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceID",
            "type": "Attribute",
        }
    )
    device_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceName",
            "type": "Attribute",
            "required": True,
        }
    )
    device_role: Optional[DeviceRole] = field(
        default=None,
        metadata={
            "name": "deviceRole",
            "type": "Attribute",
            "required": True,
        }
    )
    device_vendor: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceVendor",
            "type": "Attribute",
        }
    )
    loaded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Parameters:
        parameter: List[Parameter] = field(
            default_factory=list,
            metadata={
                "type": "Element",
            }
        )
        real_parameter: List[RealParameter] = field(
            default_factory=list,
            metadata={
                "name": "RealParameter",
                "type": "Element",
            }
        )
        bool_parameter: List[BoolParameter] = field(
            default_factory=list,
            metadata={
                "name": "BoolParameter",
                "type": "Element",
            }
        )
        integer_parameter: List[IntegerParameter] = field(
            default_factory=list,
            metadata={
                "name": "IntegerParameter",
                "type": "Element",
            }
        )
        enum_parameter: List[EnumParameter] = field(
            default_factory=list,
            metadata={
                "name": "EnumParameter",
                "type": "Element",
            }
        )
        time_signature_parameter: List[TimeSignatureParameter] = field(
            default_factory=list,
            metadata={
                "name": "TimeSignatureParameter",
                "type": "Element",
            }
        )


@dataclass
class Device(Device1):
    pass


@dataclass
class BuiltinDevice1(Device1):
    class Meta:
        name = "builtinDevice"


@dataclass
class Plugin(Device1):
    class Meta:
        name = "plugin"

    plugin_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "pluginVersion",
            "type": "Attribute",
        }
    )


@dataclass
class Warps1(Timeline1):
    class Meta:
        name = "warps"

    timeline: Optional[Timeline] = field(
        default=None,
        metadata={
            "name": "Timeline",
            "type": "Element",
        }
    )
    lanes: Optional["Lanes"] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
        }
    )
    notes: Optional["Notes"] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        }
    )
    clips: Optional["Clips"] = field(
        default=None,
        metadata={
            "name": "Clips",
            "type": "Element",
        }
    )
    clip_slot: Optional[ClipSlot] = field(
        default=None,
        metadata={
            "name": "ClipSlot",
            "type": "Element",
        }
    )
    markers: Optional[Markers] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    warps: Optional["Warps"] = field(
        default=None,
        metadata={
            "name": "Warps",
            "type": "Element",
        }
    )
    audio: Optional[Audio] = field(
        default=None,
        metadata={
            "name": "Audio",
            "type": "Element",
        }
    )
    video: Optional[Video] = field(
        default=None,
        metadata={
            "name": "Video",
            "type": "Element",
        }
    )
    points: Optional[Points] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
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
    content_time_unit: Optional[TimeUnit] = field(
        default=None,
        metadata={
            "name": "contentTimeUnit",
            "type": "Attribute",
            "required": True,
        }
    )


@dataclass
class BuiltinDevice(BuiltinDevice1):
    pass


@dataclass
class Warps(Warps1):
    pass


@dataclass
class AuPlugin1(Plugin):
    class Meta:
        name = "auPlugin"


@dataclass
class ClapPlugin1(Plugin):
    class Meta:
        name = "clapPlugin"


@dataclass
class Compressor1(BuiltinDevice1):
    class Meta:
        name = "compressor"

    attack: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Attack",
            "type": "Element",
            "namespace": "",
        }
    )
    auto_makeup: Optional[BoolParameter1] = field(
        default=None,
        metadata={
            "name": "AutoMakeup",
            "type": "Element",
            "namespace": "",
        }
    )
    input_gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "InputGain",
            "type": "Element",
            "namespace": "",
        }
    )
    output_gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "OutputGain",
            "type": "Element",
            "namespace": "",
        }
    )
    ratio: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Ratio",
            "type": "Element",
            "namespace": "",
        }
    )
    release: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Release",
            "type": "Element",
            "namespace": "",
        }
    )
    threshold: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Threshold",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Equalizer1(BuiltinDevice1):
    class Meta:
        name = "equalizer"

    band: List[EqBand] = field(
        default_factory=list,
        metadata={
            "name": "Band",
            "type": "Element",
            "namespace": "",
        }
    )
    input_gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "InputGain",
            "type": "Element",
            "namespace": "",
        }
    )
    output_gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "OutputGain",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Limiter1(BuiltinDevice1):
    class Meta:
        name = "limiter"

    attack: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Attack",
            "type": "Element",
            "namespace": "",
        }
    )
    input_gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "InputGain",
            "type": "Element",
            "namespace": "",
        }
    )
    output_gain: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "OutputGain",
            "type": "Element",
            "namespace": "",
        }
    )
    release: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Release",
            "type": "Element",
            "namespace": "",
        }
    )
    threshold: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Threshold",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class NoiseGate1(BuiltinDevice1):
    class Meta:
        name = "noiseGate"

    attack: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Attack",
            "type": "Element",
            "namespace": "",
        }
    )
    range: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Range",
            "type": "Element",
            "namespace": "",
        }
    )
    ratio: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Ratio",
            "type": "Element",
            "namespace": "",
        }
    )
    release: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Release",
            "type": "Element",
            "namespace": "",
        }
    )
    threshold: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Threshold",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Vst2Plugin1(Plugin):
    class Meta:
        name = "vst2Plugin"


@dataclass
class Vst3Plugin1(Plugin):
    class Meta:
        name = "vst3Plugin"


@dataclass
class AuPlugin(AuPlugin1):
    pass


@dataclass
class ClapPlugin(ClapPlugin1):
    pass


@dataclass
class Compressor(Compressor1):
    pass


@dataclass
class Equalizer(Equalizer1):
    pass


@dataclass
class Limiter(Limiter1):
    pass


@dataclass
class NoiseGate(NoiseGate1):
    pass


@dataclass
class Vst2Plugin(Vst2Plugin1):
    pass


@dataclass
class Vst3Plugin(Vst3Plugin1):
    pass


@dataclass
class Clip1(Nameable):
    class Meta:
        name = "clip"

    timeline: Optional[Timeline] = field(
        default=None,
        metadata={
            "name": "Timeline",
            "type": "Element",
        }
    )
    lanes: Optional["Lanes"] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
        }
    )
    notes: Optional["Notes"] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        }
    )
    clips: Optional["Clips"] = field(
        default=None,
        metadata={
            "name": "Clips",
            "type": "Element",
        }
    )
    clip_slot: Optional[ClipSlot] = field(
        default=None,
        metadata={
            "name": "ClipSlot",
            "type": "Element",
        }
    )
    markers: Optional[Markers] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    warps: Optional[Warps] = field(
        default=None,
        metadata={
            "name": "Warps",
            "type": "Element",
        }
    )
    audio: Optional[Audio] = field(
        default=None,
        metadata={
            "name": "Audio",
            "type": "Element",
        }
    )
    video: Optional[Video] = field(
        default=None,
        metadata={
            "name": "Video",
            "type": "Element",
        }
    )
    points: Optional[Points] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
        }
    )
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
        }
    )
    content_time_unit: Optional[TimeUnit] = field(
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
        }
    )
    play_stop: Optional[float] = field(
        default=None,
        metadata={
            "name": "playStop",
            "type": "Attribute",
        }
    )
    loop_start: Optional[float] = field(
        default=None,
        metadata={
            "name": "loopStart",
            "type": "Attribute",
        }
    )
    loop_end: Optional[float] = field(
        default=None,
        metadata={
            "name": "loopEnd",
            "type": "Attribute",
        }
    )
    fade_time_unit: Optional[TimeUnit] = field(
        default=None,
        metadata={
            "name": "fadeTimeUnit",
            "type": "Attribute",
        }
    )
    fade_in_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "fadeInTime",
            "type": "Attribute",
        }
    )
    fade_out_time: Optional[float] = field(
        default=None,
        metadata={
            "name": "fadeOutTime",
            "type": "Attribute",
        }
    )
    reference: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Clip(Clip1):
    pass


@dataclass
class Channel1(Lane):
    class Meta:
        name = "channel"

    devices: Optional["Channel1.Devices"] = field(
        default=None,
        metadata={
            "name": "Devices",
            "type": "Element",
            "namespace": "",
        }
    )
    mute: Optional[BoolParameter1] = field(
        default=None,
        metadata={
            "name": "Mute",
            "type": "Element",
            "namespace": "",
        }
    )
    pan: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Pan",
            "type": "Element",
            "namespace": "",
        }
    )
    sends: Optional["Channel1.Sends"] = field(
        default=None,
        metadata={
            "name": "Sends",
            "type": "Element",
            "namespace": "",
        }
    )
    volume: Optional[RealParameter1] = field(
        default=None,
        metadata={
            "name": "Volume",
            "type": "Element",
            "namespace": "",
        }
    )
    audio_channels: Optional[int] = field(
        default=None,
        metadata={
            "name": "audioChannels",
            "type": "Attribute",
        }
    )
    destination: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    role: Optional[MixerRole] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    solo: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Devices:
        device: List[Device] = field(
            default_factory=list,
            metadata={
                "name": "Device",
                "type": "Element",
            }
        )
        vst2_plugin: List[Vst2Plugin] = field(
            default_factory=list,
            metadata={
                "name": "Vst2Plugin",
                "type": "Element",
            }
        )
        vst3_plugin: List[Vst3Plugin] = field(
            default_factory=list,
            metadata={
                "name": "Vst3Plugin",
                "type": "Element",
            }
        )
        clap_plugin: List[ClapPlugin] = field(
            default_factory=list,
            metadata={
                "name": "ClapPlugin",
                "type": "Element",
            }
        )
        builtin_device: List[BuiltinDevice] = field(
            default_factory=list,
            metadata={
                "name": "BuiltinDevice",
                "type": "Element",
            }
        )
        equalizer: List[Equalizer] = field(
            default_factory=list,
            metadata={
                "name": "Equalizer",
                "type": "Element",
            }
        )
        compressor: List[Compressor] = field(
            default_factory=list,
            metadata={
                "name": "Compressor",
                "type": "Element",
            }
        )
        noise_gate: List[NoiseGate] = field(
            default_factory=list,
            metadata={
                "name": "NoiseGate",
                "type": "Element",
            }
        )
        limiter: List[Limiter] = field(
            default_factory=list,
            metadata={
                "name": "Limiter",
                "type": "Element",
            }
        )
        au_plugin: List[AuPlugin] = field(
            default_factory=list,
            metadata={
                "name": "AuPlugin",
                "type": "Element",
            }
        )

    @dataclass
    class Sends:
        send: List[Send] = field(
            default_factory=list,
            metadata={
                "name": "Send",
                "type": "Element",
                "namespace": "",
            }
        )


@dataclass
class Channel(Channel1):
    pass


@dataclass
class Clips1(Timeline1):
    class Meta:
        name = "clips"

    clip: List[Clip] = field(
        default_factory=list,
        metadata={
            "name": "Clip",
            "type": "Element",
        }
    )


@dataclass
class Clips(Clips1):
    pass


@dataclass
class Track1(Lane):
    class Meta:
        name = "track"

    channel: Optional[Channel] = field(
        default=None,
        metadata={
            "name": "Channel",
            "type": "Element",
        }
    )
    track: List["Track"] = field(
        default_factory=list,
        metadata={
            "name": "Track",
            "type": "Element",
        }
    )
    content_type: List[ContentType] = field(
        default_factory=list,
        metadata={
            "name": "contentType",
            "type": "Attribute",
            "tokens": True,
        }
    )
    loaded: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Track(Track1):
    pass


@dataclass
class Note1:
    class Meta:
        name = "note"

    timeline: Optional[Timeline] = field(
        default=None,
        metadata={
            "name": "Timeline",
            "type": "Element",
        }
    )
    lanes: Optional["Lanes"] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
        }
    )
    notes: Optional["Notes"] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        }
    )
    clips: Optional[Clips] = field(
        default=None,
        metadata={
            "name": "Clips",
            "type": "Element",
        }
    )
    clip_slot: Optional[ClipSlot] = field(
        default=None,
        metadata={
            "name": "ClipSlot",
            "type": "Element",
        }
    )
    markers: Optional[Markers] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    warps: Optional[Warps] = field(
        default=None,
        metadata={
            "name": "Warps",
            "type": "Element",
        }
    )
    audio: Optional[Audio] = field(
        default=None,
        metadata={
            "name": "Audio",
            "type": "Element",
        }
    )
    video: Optional[Video] = field(
        default=None,
        metadata={
            "name": "Video",
            "type": "Element",
        }
    )
    points: Optional[Points] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
        }
    )
    time: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    channel: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    key: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    vel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    rel: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Note(Note1):
    pass


@dataclass
class Notes1(Timeline1):
    class Meta:
        name = "notes"

    note: List[Note] = field(
        default_factory=list,
        metadata={
            "name": "Note",
            "type": "Element",
        }
    )


@dataclass
class Notes(Notes1):
    pass


@dataclass
class Lanes1(Timeline1):
    class Meta:
        name = "lanes"

    timeline: List[Timeline] = field(
        default_factory=list,
        metadata={
            "name": "Timeline",
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
    notes: List[Notes] = field(
        default_factory=list,
        metadata={
            "name": "Notes",
            "type": "Element",
        }
    )
    clips: List[Clips] = field(
        default_factory=list,
        metadata={
            "name": "Clips",
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
    markers: List[Markers] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    warps: List[Warps] = field(
        default_factory=list,
        metadata={
            "name": "Warps",
            "type": "Element",
        }
    )
    audio: List[Audio] = field(
        default_factory=list,
        metadata={
            "name": "Audio",
            "type": "Element",
        }
    )
    video: List[Video] = field(
        default_factory=list,
        metadata={
            "name": "Video",
            "type": "Element",
        }
    )
    points: List[Points] = field(
        default_factory=list,
        metadata={
            "name": "Points",
            "type": "Element",
        }
    )


@dataclass
class Lanes(Lanes1):
    pass


@dataclass
class Arrangement1(Referenceable):
    class Meta:
        name = "arrangement"

    lanes: Optional[Lanes] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
        }
    )
    markers: Optional[Markers] = field(
        default=None,
        metadata={
            "name": "Markers",
            "type": "Element",
            "namespace": "",
        }
    )
    tempo_automation: Optional[Points1] = field(
        default=None,
        metadata={
            "name": "TempoAutomation",
            "type": "Element",
            "namespace": "",
        }
    )
    time_signature_automation: Optional[Points1] = field(
        default=None,
        metadata={
            "name": "TimeSignatureAutomation",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Scene1(Referenceable):
    class Meta:
        name = "scene"

    timeline: Optional[Timeline] = field(
        default=None,
        metadata={
            "name": "Timeline",
            "type": "Element",
        }
    )
    lanes: Optional[Lanes] = field(
        default=None,
        metadata={
            "name": "Lanes",
            "type": "Element",
        }
    )
    notes: Optional[Notes] = field(
        default=None,
        metadata={
            "name": "Notes",
            "type": "Element",
        }
    )
    clips: Optional[Clips] = field(
        default=None,
        metadata={
            "name": "Clips",
            "type": "Element",
        }
    )
    clip_slot: Optional[ClipSlot] = field(
        default=None,
        metadata={
            "name": "ClipSlot",
            "type": "Element",
        }
    )
    markers: Optional[Markers] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    warps: Optional[Warps] = field(
        default=None,
        metadata={
            "name": "Warps",
            "type": "Element",
        }
    )
    audio: Optional[Audio] = field(
        default=None,
        metadata={
            "name": "Audio",
            "type": "Element",
        }
    )
    video: Optional[Video] = field(
        default=None,
        metadata={
            "name": "Video",
            "type": "Element",
        }
    )
    points: Optional[Points] = field(
        default=None,
        metadata={
            "name": "Points",
            "type": "Element",
        }
    )


@dataclass
class Arrangement(Arrangement1):
    pass


@dataclass
class Scene(Scene1):
    pass


@dataclass
class Project1:
    class Meta:
        name = "project"

    application: Optional[Application] = field(
        default=None,
        metadata={
            "name": "Application",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    transport: Optional[Transport] = field(
        default=None,
        metadata={
            "name": "Transport",
            "type": "Element",
            "namespace": "",
        }
    )
    structure: Optional["Project1.Structure"] = field(
        default=None,
        metadata={
            "name": "Structure",
            "type": "Element",
            "namespace": "",
        }
    )
    arrangement: Optional[Arrangement] = field(
        default=None,
        metadata={
            "name": "Arrangement",
            "type": "Element",
        }
    )
    scenes: Optional["Project1.Scenes"] = field(
        default=None,
        metadata={
            "name": "Scenes",
            "type": "Element",
            "namespace": "",
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
    class Structure:
        track: List[Track] = field(
            default_factory=list,
            metadata={
                "name": "Track",
                "type": "Element",
            }
        )
        channel: List[Channel] = field(
            default_factory=list,
            metadata={
                "name": "Channel",
                "type": "Element",
            }
        )

    @dataclass
    class Scenes:
        scene: List[Scene] = field(
            default_factory=list,
            metadata={
                "name": "Scene",
                "type": "Element",
            }
        )


@dataclass
class Project(Project1):
    pass
