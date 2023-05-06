import os
import time

import constants


class CelesteRunData:
    def __init__(self):
        self.reset()

    # Reset all run data to empty
    def reset(self):
        self.previous_save_data = None
        self.run_date_and_time = time.time()
        self.full_run_time = 0
        self.chapters = {}
        for chapter_id in constants.LEVEL_CODE_BY_ID:
            has_sides = chapter_id in (1, 2, 3, 4, 5, 6, 7, 9)

            for side_id in range(3 if has_sides else 1):
                level_id = constants.LEVEL_CODE_BY_ID[chapter_id] + (
                    constants.SIDE_CODE_BY_ID[side_id] if has_sides else ""
                )
                self.chapters[level_id] = CelesteChapterData(level_id)

    def update_from_xml(xml):
        pass


class CelesteChapterData:
    def __init__(self, level_id: str):
        self.level_id = level_id
        self.unlocked = False
        self.chapter_time = 0
        self.checkpoints = []

        for checkpoint_id in range(constants.CHECKPOINTS_BY_LEVEL_ID[self.level_id]):
            self.checkpoints.append(ChapterCheckpointData())


class ChapterCheckpointData:
    def __init__(self):
        self.time = 0
        self.deaths = 0
        self.berries = []
        self.heart = False
