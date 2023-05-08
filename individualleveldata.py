import os
import time
import gspread
import json
from logging_system import LogMessage, logging_queue

import constants

from saveparser import CelesteSaveData


class CelesteIndividualLevelData:
    def __init__(self, settings):
        self.previous_save_data = None
        self.reset()
        success = self.setup_sheet(settings)
        if not success:
            logging_queue.put(LogMessage(3, "Failed to connect to google sheet."))

    # Reset all run data to empty
    def reset(self):
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

        if self.level == constants.FINAL_ROOM_BY_LEVEL_ID[self.level_id]:
            # If we saved while in the last room we completed the run
            print("Run completed with a time of {}".format(self.run_time))
            self.completed_run = True
        else:
            # Else the run was reset before completing
            print("Run reset in room {} at time {}".format(self.level, self.run_time))
            self.completed_run = False

        self.previous_save_data = save

        self.upload_data_to_sheet()
        self.reset()

    def setup_sheet(self, settings) -> bool:
        try:
            gc = gspread.service_account(filename="credentials.json")
        except OSError as e:
            print(
                "Could not find credentials.json, make sure you have the file in the same directory as the exe, and named exactly 'credentials.json'"
            )
            return False
        try:
            sh = gc.open_by_url(
                settings["SheetUrl"]
            )
        except gspread.exceptions.APIError:
            return False

        try:
            self.dataSheet = sh.worksheet("Raw Data")
        except gspread.WorksheetNotFound:
            return False
        return True

    def upload_data_to_sheet(self):
        self.dataSheet.insert_row(
            [
                self.run_date_and_time,
                self.level_id,
                self.run_time,
                self.deaths,
                len(self.berries),
                self.cassette,
                self.heart,
                self.level,
                self.completed_run,
            ],
            index=4,
            value_input_option="USER_ENTERED",
        )

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
