#!/usr/bin/python3

from re import split
import sys
from datetime import datetime, timedelta

class Mark:
    #M,-1,1,1,0,0:00:00.933250
    def __init__(self, line):
        splited = line.strip().split(",")
        self.mark_type = splited[0]
        self.label = splited[3]
        self.timedelta = Mark.get_timedelta_from_timestamp_string(splited[5])

    def __repr__(self):
        return f"[{self.label}] {self.timedelta}"

    @staticmethod
    def get_timedelta_from_timestamp_string(timestamp_string):
        t = datetime.strptime(timestamp_string, '%H:%M:%S.%f')
        return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

class TranscribeFile:
    START_LINE = "SectionStart,Markers"
    SKIP_LINES = ["Howmany"]
    END_LINE = "SectionEnd,Markers"

    def __init__(self, path):
        self.path = path

    def get_file_lines(self):
        with open(self.path, "r") as file:
            return file.readlines()

    def get_marks(self):
        marks = []
        lines = self.get_file_lines()
        inside = False
        for l in lines:
            l = l.strip()
            if not inside:
                if l == self.START_LINE:
                    inside = True
                    continue
            if inside:
                if l == self.END_LINE:
                    inside = False
                    continue
                skip_line_found = False
                for skip_line in self.SKIP_LINES:
                    if skip_line in l:
                        skip_line_found = True
                        continue
                if skip_line_found:
                    continue
                marks.append(Mark(l))
        return marks

if __name__ == "__main__":
    tf = TranscribeFile(sys.argv[1])
    marks = tf.get_marks()
    print(len(marks))
    mark = marks[0]
