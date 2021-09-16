# Type aliases
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Callable

import fire

from ptools.base import Script

RecordingDict = Dict[str, Dict[int, str]]
RenameFunc = Callable[..., None]
DeleteFunc = Callable[..., None]


class YiRename(Script):
    @staticmethod
    def _get_files(path: Path) -> RecordingDict:
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
    def _get_new_filename(recording_id: str, sequence_number: int) -> str:
        """Return the new filename for the file with given ID and sequence number.
        Example output: "0727_02.mp4"

        :return: the new filename
        """
        return f"{recording_id}_{sequence_number:0>2}.mp4"

    @staticmethod
    def _rename_all(
        recordings: RecordingDict, renaming_func: RenameFunc
    ) -> int:
        """Apply the rename operation to all files in the recordings dict.

        :return: the number of renamed files
        """
        renamed_count = 0
        for recording, files in recordings.items():
            for seq, original_filename in files.items():
                new_filename = YiRename._get_new_filename(recording, seq)
                renaming_func(original_filename, new_filename)
                renamed_count += 1
        return renamed_count

    @staticmethod
    def _delete_sec_files(delete_sec_func: DeleteFunc) -> int:
        """Delete .SEC files, created as quick previews for phone viewing.

        :return: the number of deleted files
        """
        sec_files = [f for f in os.listdir() if f.lower().endswith(".sec")]
        for file in sec_files:
            delete_sec_func(file)
        return len(sec_files)

    @staticmethod
    def _rename_file_dry_run(src: str, dst: str) -> None:
        """Dry run rename - just print src and dst filenames."""
        print(f"rename: {src:>16} -> {dst}")

    @staticmethod
    def _delete_file_dry_run(file: str) -> None:
        """Dry-run delete - just print filenames."""
        print(f"delete: {file}")

    @staticmethod
    def main(
        dry_run: bool = False, delete_sec: bool = True, directory: str = "."
    ) -> None:

        dir_path = Path(directory)
        os.chdir(dir_path)

        # Set action functions depending on whether it's a dry run or not.
        # This is to make sure logic executed is identical between live and dry
        # runs, and avoid having and maintaining duplicated or very similar code.
        rename_func: RenameFunc = (
            YiRename._rename_file_dry_run if dry_run else os.rename
        )
        delete_func: DeleteFunc = (
            YiRename._delete_file_dry_run if dry_run else os.remove
        )

        rename_files = YiRename._get_files(dir_path)
        renamed_count = YiRename._rename_all(rename_files, rename_func)
        if renamed_count:
            if dry_run:
                print(f"(dry run) Renamed {renamed_count} files.")
            else:
                print(f"Renamed {renamed_count} files.")
        else:
            print(f"No files to rename in {dir_path.absolute()}.")

        if delete_sec:
            deleted_count = YiRename._delete_sec_files(delete_func)
            if deleted_count:
                if dry_run:
                    print(f"(dry run) Deleted {deleted_count} SEC files.")
                else:
                    print(f"Deleted {deleted_count} SEC files.")
            else:
                print(f"No SEC files to delete in {dir_path.absolute()}.")

    @classmethod
    def run(cls) -> None:
        fire.Fire(cls.main)


if __name__ == "__main__":
    YiRename.run()
