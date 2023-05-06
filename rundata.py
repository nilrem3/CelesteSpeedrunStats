import os
import time

from saveparser import LEVEL_CODE_BY_ID, SIDE_CODE_BY_ID


CHECKPOINTS_BY_LEVEL_ID = {
    "prologue": 1,
    "1a": 3,
    "1b": 3,
    "1c": 1,
    "2a": 3,
    "2b": 3,
    "2c": 1,
    "3a": 4,
    "3b": 4,
    "3c": 1,
    "4a": 4,
    "4b": 4,
    "4c": 1,
    "5a": 5,
    "5b": 4,
    "5c": 1,
    "6a": 6,
    "6b": 4,
    "6c": 1,
    "7a": 7,
    "7b": 7,
    "7c": 1,
    "epilogue": 1,
    "8a": 4,
    "8b": 4,
    "8c": 1,
    "9": 9,
}


class CelesteRunData:
    def __init__(self):
        self.reset()

    # Reset all run data to empty
    def reset(self):
        self.previous_save_data = None
        self.run_date_and_time = time.time()
        self.full_run_time = 0
        self.chapters = {}
        for chapter_id in LEVEL_CODE_BY_ID:
            has_sides = chapter_id in (1, 2, 3, 4, 5, 6, 7, 9)

            for side_id in range(3 if has_sides else 1):
                level_id = LEVEL_CODE_BY_ID[chapter_id] + (
                    SIDE_CODE_BY_ID[side_id] if has_sides else ""
                )
                self.chapters[level_id] = CelesteChapterData(level_id)


class CelesteChapterData:
    def __init__(self, level_id: str):
        self.level_id = level_id
        self.unlocked = False
        self.chapter_time = 0
        self.checkpoints = []

        for checkpoint_id in range(CHECKPOINTS_BY_LEVEL_ID[self.level_id]):
            self.checkpoints.append(ChapterCheckpointData())


class ChapterCheckpointData:
    def __init__(self):
        self.time = 0
        self.deaths = 0
        self.berries = []
        self.heart = False
