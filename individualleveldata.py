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

    def update_from_xml(self, xml):
        save = CelesteSaveData(xml)

        self.update_data_from_save(save)
        self.run_date_and_time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

        # If there is no previous data this is the first time updating the file, return early
        if self.previous_save_data is None:
            self.previous_save_data = save
            self.ready_to_upload = False
            return

        self.ready_to_upload = True

        self.previous_save_data = save

    def get_run_completed(self, category):
        if not self.get_run_finished():
            log_message(
                LogLevel.INFO,
                f"{category} run reset in room {self.end_room} at time {self.run_time}",
            )
            return False

        if category == "Clear":
            log_message(
                LogLevel.INFO, f"Clear run completed with a time of {self.run_time}"
            )
            return True
        if (
            category == "Full Clear"
            and len(self.berries)
            == len(constants.RED_BERRY_IDS_BY_LEVEL[self.level_id])
            and self.heart
            and self.cassette
        ):
            log_message(
                LogLevel.INFO,
                f"Full Clear run completed with a time of {self.run_time}",
            )
            return True
        elif (
            category == "All Red Berries+Heart"
            and len(self.berries)
            == len(constants.RED_BERRY_IDS_BY_LEVEL[self.level_id])
            and self.heart
        ):
            log_message(
                LogLevel.INFO,
                f"All Red Berries+Heart run completed with a time of {self.run_time}",
            )
            return True
        elif category == "Heart+Cassette" and self.heart and self.cassette:
            log_message(
                LogLevel.INFO,
                f"Heart+Cassette run completed with a time of {self.run_time}",
            )
            return True
        elif category == "Dashless" and self.dashes == 0:
            log_message(
                LogLevel.INFO, f"Dashless run completed with a time of {self.run_time}"
            )
            return True

        log_message(
            LogLevel.INFO,
            f"{category} run reset in room {self.end_room} at time {self.run_time}",
        )
        return False

    def get_run_finished(self):
        if (
            constants.ENDS_WITH_HEART[self.level_id] is False
            and self.end_room == constants.FINAL_ROOM_BY_LEVEL_ID[self.level_id]
        ):
            # If we saved while in the last room of an a-side we completed the run
            return True
        elif constants.ENDS_WITH_HEART[self.level_id] and self.heart:
            return True
        else:
            # Else the run was reset before completing
            return False

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
            self.first_room_deaths = (
                (save.death_count - self.previous_save_data.death_count)
                - save.current_session_deaths
                if (save.death_count - self.previous_save_data.death_count)
                - save.current_session_deaths
                < 0
                else 0
            )
