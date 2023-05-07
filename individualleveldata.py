import os
import time

import constants

from saveparser import CelesteSaveData


class CelesteIndividualLevelData:
    def __init__(self):
        self.reset()

    # Reset all run data to empty
    def reset(self):
        self.previous_save_data = None
        self.run_date_and_time = time.time()
        self.level_id = None
        self.run_time = 0
        self.deaths = 0
        self.berries = []
        self.cassette = False
        self.heart = False
        self.level = ""
        self.completed_run = False

    def update_from_xml(self, xml):
        save = CelesteSaveData(xml)

        self.update_data_from_save(save)

        # If there is no previous data this is the first time updating the file, return early
        if self.previous_save_data is None:
            self.previous_save_data = save
            return

        # If we saved while in the last room we completed the run
        if self.level == constants.FINAL_ROOM_BY_LEVEL_ID[self.level_id]:
            print("Run completed with a time of {}".format(self.run_time))
        # Else the run was reset before completing
        else:
            print("Run reset in room {} at time {}".format(self.level, self.run_time))

        self.previous_save_data = save

    def update_data_from_save(self, save):
        has_sides = save.current_session_id in (
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            9,
        )
        self.level_id = constants.LEVEL_CODE_BY_ID[save.current_session_id] + (
            constants.SIDE_CODE_BY_MODE[save.current_session_mode] if has_sides else ""
        )
        self.run_time = save.current_session_time
        self.deaths = save.current_session_deaths
        self.berries = save.current_session_berries
        self.cassette = save.current_session_cassette
        self.heart = save.current_session_heart
        self.level = save.current_session_level
