import os
import gspread
from logging_system import LogLevel, log_message
from individualleveldata import CelesteIndividualLevelData
import constants


class ILDataUploader:
    def __init__(self):
        self.raw_data_sheet = None
        self.death_threshold = None
        self.time_threshold = None
        self.tags = []
        self.category = "Clear"
        self.practice_mode = "off"

    def setup_sheet(self, settings, credentials) -> bool:
        try:
            gc = gspread.service_account(filename=credentials)
        except OSError:
            log_message(LogLevel.ERROR, "Failed to find credentials.json")
            return False

        try:
            sh = gc.open_by_url(settings["SheetUrl"])
        except gspread.exceptions.APIError:
            log_message(LogLevel.ERROR, "Failed to connect to Google Sheets API")
            return False

        try:
            self.raw_data_sheet = sh.worksheet("Raw Data")
        except gspread.exceptions.WorksheetNotFound:
            log_message(LogLevel.ERROR, "Failed to find Raw Data worksheet")
            return False

        try:
            self.data_summary_sheet = sh.worksheet("IL Data Summary")
        except gspread.exceptions.WorksheetNotFound:
            log_message(LogLevel.ERROR, "Failed to find IL Data Summary worksheet")
            return False

        return True

    def upload_run_to_sheet(self, data: CelesteIndividualLevelData):
        is_practice = self.get_is_practice(data)

        if is_practice:
            log_message(LogLevel.INFO, "Run marked as practice.")

        self.check_category(data)

        level_ids = self.data_summary_sheet.col_values(1)
        categories = self.data_summary_sheet.col_values(2)
        bests = self.data_summary_sheet.col_values(
            3, value_render_option="UNFORMATTED_VALUE"
        )

        completed = data.get_run_completed(self.category)
        is_pb = False
        if completed:
            is_pb = True
            for level_id, time, category in zip(level_ids, bests, categories):
                if level_id != data.level_id or category != self.category:
                    continue
                elif time < data.run_time / 36000000000 / 24:
                    is_pb = False
                    break

        self.raw_data_sheet.insert_row(
            [
                data.run_date_and_time,
                self.category,
                data.level_id,
                data.run_time / 36000000000 / 24,
                data.deaths,
                data.dashes,
                len(data.berries),
                data.cassette,
                data.heart,
                data.golden,
                data.end_room,
                data.first_room_deaths,
                completed,
                is_pb,
                is_practice,
                ", ".join(self.tags),
            ],
            index=2,
            value_input_option="USER_ENTERED",
        )

    def add_comment(self, comment):
        self.raw_data_sheet.update("Q2", comment)

    def check_category(self, data):
        if not data.get_run_finished():
            return

        if (
            len(data.berries) < 3
            and not data.heart
            and not data.cassette
            and data.dashes > 0
        ):
            self.category = "Clear"
        if (
            len(data.berries) == len(constants.RED_BERRY_IDS_BY_LEVEL[data.level_id])
            and data.heart
            and data.cassette
        ):
            self.category = "Full Clear"
        elif (
            len(data.berries) == len(constants.RED_BERRY_IDS_BY_LEVEL[data.level_id])
            and data.heart
        ):
            self.category = "All Red Berries+Heart"
        elif data.heart and data.cassette:
            self.category = "Heart+Cassette"
        elif data.dashes == 0:
            self.category = "Dashless"

    def set_category(self, category):
        if category in constants.IL_CAT_STR_TO_CAT.keys():
            self.category = constants.IL_CATEGORIES[
                constants.IL_CAT_STR_TO_CAT[category]
            ]
            return True
        return False

    def get_is_practice(self, data):
        if self.practice_mode == "on":
            return True
        elif self.practice_mode == "off":
            return False

        if self.death_threshold is not None:
            if data.deaths > self.death_threshold:
                return True

        if self.time_threshold is not None:
            if data.run_time / 36000000000 / 24 > self.time_threshold:
                return True
