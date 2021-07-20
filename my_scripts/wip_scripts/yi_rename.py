# Type aliases
import os
import re
from collections import Callable, defaultdict
from pathlib import Path

from my_scripts.base import Script

RecordingDict = dict[str, dict[int, str]]
RenameFunc = Callable[..., None]
DeleteFunc = Callable[..., None]


class YiRename(Script):
    @staticmethod
    def get_files(path: Path) -> RecordingDict:
        """Return a dict containing recording IDs and pertaining files in the
        correct order.

        Example output:
        {
         "0732": {
          "0": "YDXJ0732.MP4",
          "1": "YN010732.MP4",
          "2": "YN020732.MP4"
         },
         "0733": {
          "0": "YDXJ0733.MP4",
          "1": "YN010734.MP4"
         }
        }

        :return: dict containing recording IDs and files in their correct order
        """
        recordings: RecordingDict = defaultdict(dict)
        dir_files = (f for f in path.iterdir() if f.is_file())
        for file in dir_files:

            if match := re.match(r"YDXJ(\d{4})\.MP4", file.name):
                # First file of the recording
                recording_number = match.group(1)
                recordings[recording_number][0] = file

            elif match := re.match(r"YN(\d{2})(\d{4})\.MP4", file.name):
                # Second+ file of the recording
                _, file_no, recording_no = match[0], match[1], match[2]
                recordings[recording_no][int(file_no)] = file.name

        return recordings

    @staticmethod
    def get_new_filename(recording_id: str, sequence_number: int) -> str:
        """Return the new filename for the file with given ID and sequence number.
        Example output: "0727_02.mp4"

        :return: the new filename
        """
        return f"{recording_id}_{sequence_number:0>2}.mp4"
