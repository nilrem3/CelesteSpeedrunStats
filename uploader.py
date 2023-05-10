import gspread
from logging_system import LogLevel, log_message
from individualleveldata import CelesteIndividualLevelData


class ILDataUploader:
    def __init__(self):
        self.datasheet = None
        self.death_threshold = None
        self.time_threshold = None

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
            log_message(LogLevel.ERROR, "Failed to find Raw Data datasheet")
            return False

        return True

    def upload_run_to_sheet(self, data: CelesteIndividualLevelData):

        is_practice = False

        if self.death_threshold is not None:
            if data.deaths > self.death_threshold:
                is_practice = True

        if self.time_threshold is not None:
            if data.run_time / 36000000000 / 24 > self.time_threshold:
                is_practice = True

        if is_practice:
            log_message(LogLevel.INFO, "Run marked as practice.")

        self.datasheet.insert_row(
            [
                data.run_date_and_time,
                data.level_id,
                data.run_time / 36000000000 / 24,
                data.deaths,
                data.dashes,
                len(data.berries),
                data.cassette,
                data.heart,
                data.golden,
                data.end_room,
                data.completed_run,
                is_practice
            ],
            index=2,
            value_input_option="USER_ENTERED"
        )
