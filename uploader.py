import gspread
from logging_system import LogLevel, log_message
from individualleveldata import CelesteIndividualLevelData
import constants


class ILDataUploader:
    def __init__(self):
        self.datasheet = None
        self.death_threshold = None
        self.time_threshold = None
        self.tags = []
        self.category = "Clear"
        self.practice_mode = "off"

    def setup_sheet(self, settings) -> bool:
        try:
            gc = gspread.service_account(filename="credentials.json")
        except OSError:
            log_message(LogLevel.ERROR, "Failed to find credentials.json")
            return False

        try:
            sh = gc.open_by_url(settings["SheetUrl"])
        except gspread.exceptions.APIError:
            log_message(LogLevel.ERROR, "Failed to connect to Google Sheets API")
            return False

        try:
            self.datasheet = sh.worksheet("Raw Data")
        except gspread.exceptions.WorksheetNotFound:
            log_message(LogLevel.ERROR, "Failed to find Raw Data worksheet")
            return False

        return True

    def upload_run_to_sheet(self, data: CelesteIndividualLevelData):
        is_practice = self.get_is_practice(data)

        if is_practice:
            log_message(LogLevel.INFO, "Run marked as practice.")

        level_ids = self.datasheet.col_values(3)
        times = self.datasheet.col_values(4, value_render_option="UNFORMATTED_VALUE")
        completions = self.datasheet.col_values(13)

        is_pb = False
        best_time = None
        if data.completed_run:
            for level_id, time, completion in zip(level_ids, times, completions):
                if level_id != data.level_id or not completion:
                    continue
                else:
                    if best_time is None or float(time) < best_time:
                        best_time = float(time)
            if best_time is None or best_time > data.run_time / 36000000000 / 24:
                is_pb = True

        self.datasheet.insert_row(
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
                data.completed_run,
                is_pb,
                is_practice,
                ", ".join(self.tags),
            ],
            index=2,
            value_input_option="USER_ENTERED",
        )

    def add_comment(self, comment):
        self.datasheet.update("Q2", comment)

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
