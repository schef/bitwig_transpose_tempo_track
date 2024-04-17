from pathlib import Path
import sys
import os
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from zipfile import ZipFile

from project import Project
from project import Warp, Marker

from project.xml_template import Interpolation, RealPoint, TimeSignaturePoint
from transcribe_file import TranscribeFile

def extract_project_file(path):
    with ZipFile(path) as z:
        TMP_FILE = 'project.xml'
        filepath = z.extract(TMP_FILE)
        xml_string = Path(filepath).read_text()
        os.remove(TMP_FILE)
        parser = XmlParser()
        return parser.from_string(xml_string, Project)

def save_file(oproject, path):
    new_path = path.replace(".dawproject", "_edited.dawproject")
    TMP_FILE = 'project.xml'
    with ZipFile(path, 'r') as zr:
        with ZipFile(new_path, "w") as zw:
            for item in zr.infolist():
                if item.filename == TMP_FILE:
                    config = SerializerConfig(pretty_print=True)
                    serializer = XmlSerializer(config)
                    xml_string = serializer.render(oproject)
                    with open(TMP_FILE, "w") as f:
                        f.write(xml_string)
                    zw.write(TMP_FILE)
                    os.remove(TMP_FILE)
                else:
                    data = zr.read(item.filename)
                    zw.writestr(item, data)

if __name__ == "__main__":
    dawproject_filename = sys.argv[1]
    oproject = extract_project_file(dawproject_filename)
    #from IPython import embed; embed()
    clip = oproject.arrangement.lanes.lanes[0].clips[0].clip[0]
    warps = oproject.arrangement.lanes.lanes[0].clips[0].clip[0].clips.clip[0].warps.warp
    markers = oproject.arrangement.markers.marker
    time_signature = oproject.arrangement.time_signature_automation.time_signature_point
    tempo = oproject.arrangement.tempo_automation.real_point

    transcribe_filename = sys.argv[2]
    transcribe_file = TranscribeFile(transcribe_filename)

    # latency between transcribe audio and bitwig audio
    LATENCY = 0.04

    # clean up warps
    warps.clear()
    # clean up marks
    markers.clear()
    # clean up tempo
    tempo.clear()
    # clean up time_signature
    time_signature.clear()


    # default time signature, if no signature added on begining the measures could end in minus
    numerator = 4
    denominator = 4
    time_signature.append(TimeSignaturePoint(time='0.0', numerator=numerator, denominator=denominator))

    # default tempo if taken from the first writen
    #tempo.append(RealPoint(time='0.0', value='120.0', interpolation=Interpolation.HOLD))

    # lets start in the second bar
    start_beat = float(numerator)

    for transcribe_mark in transcribe_file.get_marks():
        if transcribe_mark.mark_type == "B":
            continue
        splited_mark = transcribe_mark.label.split(";")
        # time signature
        for part in splited_mark:
            if "TS=" in part:
                time_signature_text = part.replace("TS=", "")
                numerator, denominator = time_signature_text.split("/")
                time_signature.append(TimeSignaturePoint(time=str(start_beat), numerator=numerator, denominator=denominator))
        # tempo
        for part in splited_mark:
            if "T=" in part:
                tempo_text = part.replace("T=", "")
                tempo_float = float(tempo_text)
                tempo.append(RealPoint(time=str(start_beat), value=str(tempo_float), interpolation=Interpolation.HOLD))
        # warps
        warps.append(Warp(start_beat, transcribe_mark.timedelta.total_seconds() - LATENCY))
        # markers
        if transcribe_mark.mark_type == "S":
            mark_text = transcribe_mark.label.split(";")[0]
            markers.append(Marker(name=mark_text, color="#e5e500", time=start_beat))
        start_beat += float(4 / float(denominator) * float(numerator))

    # extend the clip to beat duration so it is visible in the project
    oproject.arrangement.lanes.lanes[0].clips[0].clip[0].duration = start_beat
    oproject.arrangement.lanes.lanes[0].clips[0].clip[0].clips.clip[0].duration = start_beat

    #from IPython import embed; embed()
    save_file(oproject, dawproject_filename)
    
