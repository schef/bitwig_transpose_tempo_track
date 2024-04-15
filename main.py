from pathlib import Path
import sys
import os
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig
from zipfile import ZipFile

from project import Project
from project import Warp, Marker

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
    warps = oproject.arrangement.lanes.lanes[0].clips[0].clip[0].clips.clip[0].warps.warp
    markers = oproject.arrangement.markers.marker

    from IPython import embed; embed()

    transcribe_filename = sys.argv[2]
    tf = TranscribeFile(transcribe_filename) 

    last_warp = warps.pop()
    START_BEAT = warps.pop().time
    beat_in_measure = 4.0

    start_beat = START_BEAT
    for mark in tf.get_marks():
        warps.append(Warp(start_beat, mark.timedelta.total_seconds()))
        start_beat += beat_in_measure
    warps.append(last_warp)

    start_beat = START_BEAT
    for mark in tf.get_marks():
        if not any(char.isdigit() for char in mark.label):
            markers.append(Marker(name=mark.label, color="#e5e500", time=start_beat))
        start_beat += beat_in_measure
    warps.append(last_warp)

    #from IPython import embed; embed()
    save_file(oproject, dawproject_filename)
    
