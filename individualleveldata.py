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
        success = self.setup_sheet(settings)
        if not success:
            log_message(LogLevel.FATAL, "Failed to connect to google sheet.")
            quit()

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
            return
        if constants.ENDS_WITH_HEART[self.level_id] == False and self.end_room == constants.FINAL_ROOM_BY_LEVEL_ID[self.level_id]:
            # If we saved while in the last room of an a-side we completed the run
            print("Run completed with a time of {}".format(self.run_time))
            self.completed_run = True
        elif constants.ENDS_WITH_HEART[self.level_id] and self.heart:
            print("Run completed with a time of {}".format(self.run_time))
            self.completed_run = True
        else:
            # Else the run was reset before completing
            print(
                "Run reset in room {} at time {}".format(self.end_room, self.run_time)
            )
            self.completed_run = False

        self.previous_save_data = save

        if not save.current_session_in_first_room and not save.run_time == 0:
            self.upload_data_to_sheet()
        self.reset()

    def setup_sheet(self, settings) -> bool:
        try:
            gc = gspread.service_account(filename="credentials.json")
        except OSError as e:
            log_message(LogLevel.ERROR, "Failed to find credentials.json, make sure you have the file in the same directory as the exe, and named exactly 'credentials.json'")
            return False
        try:
            sh = gc.open_by_url(
                settings["SheetUrl"]
            )
        except gspread.exceptions.APIError:
            log_message(LogLevel.ERROR, "Google Sheets API Error")
            return False

        try:
            self.dataSheet = sh.worksheet("Raw Data")
        except gspread.WorksheetNotFound:
            log_message(LogLevel.ERROR, "No Worksheet 'Raw Data' Found.")
            return False
        return True


    def upload_data_to_sheet(self):
        self.dataSheet.insert_row(
            [
                self.run_date_and_time,
                self.level_id,
                self.run_time / 36000000000 / 24,
                self.deaths,
                self.dashes,
                len(self.berries),
                self.cassette,
                self.heart,
                self.golden,
                self.end_room,
                self.completed_run,
            ],
            index=2,
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
        self.dashes = save.current_session_dashes
        self.berries = save.current_session_berries
        self.cassette = save.current_session_cassette
        self.heart = save.current_session_heart
        self.golden = save.current_session_golden
        self.end_room = save.current_session_end_room
