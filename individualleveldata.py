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

    def update_from_xml(self, xml):
        save = CelesteSaveData(xml)

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
