import os
from datetime import datetime
import gspread
import json
from logging_system import LogLevel, log_message

import constants

from saveparser import CelesteSaveData


class CelesteIndividualLevelData:
    def __init__(self, settings):
        self.previous_save_data = None
        self.reset()
        self.ready_to_upload = False
        self.first_room_deaths = 0

    # Reset all run data to empty
    def reset(self):
        self.run_date_and_time = None
        self.level_id = None
        self.run_time = 0
        self.deaths = 0
        self.dashes = 0
        self.berries = []
        self.cassette = False
        self.heart = False
        self.end_room = ""
        self.golden = False
        self.completed_run = False

    def update_from_xml(self, xml):
        save = CelesteSaveData(xml)

        self.update_data_from_save(save)
        self.run_date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # If there is no previous data this is the first time updating the file, return early
        if self.previous_save_data is None:
            self.previous_save_data = save
            self.ready_to_upload = False
            return

        self.ready_to_upload = True
        if constants.ENDS_WITH_HEART[self.level_id] == False and self.end_room == constants.FINAL_ROOM_BY_LEVEL_ID[self.level_id]:
            # If we saved while in the last room of an a-side we completed the run
            log_message(LogLevel.INFO, "Run completed with a time of {}".format(self.run_time))
            self.completed_run = True
        elif constants.ENDS_WITH_HEART[self.level_id] and self.heart:
            log_message(LogLevel.INFO, "Run completed with a time of {}".format(self.run_time))
            self.completed_run = True
        else:
            # Else the run was reset before completing
            log_message(LogLevel.INFO, "Run reset in room {} at time {}".format(self.end_room, self.run_time))
            self.completed_run = False  

        self.previous_save_data = save
        if save.current_session_in_first_room:
            self.ready_to_upload = False

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
        self.dashes = save.current_session_dashes
        self.berries = save.current_session_berries
        self.cassette = save.current_session_cassette
        self.heart = save.current_session_heart
        self.golden = save.current_session_golden
        self.end_room = save.current_session_end_room
        if self.previous_save_data is not None:
            self.first_room_deaths = (save.death_count - self.previous_save_data.death_count) - save.current_session_deaths
