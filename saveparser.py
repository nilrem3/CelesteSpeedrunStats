import xml.etree.ElementTree as ET

import constants


class CelesteSaveData:
    def __init__(self, xml: str):

        self.total_time_100_ns = {}
        self.death_count = 0
        self.current_session_id = 0
        self.current_session_mode = ""
        self.current_session_time = 0
        self.current_session_deaths = 0
        self.current_session_berries = []
        self.current_session_cassette = False
        self.current_session_heart = False
        self.total_chapter_times_100_ns = {}
        self.best_chapter_times_100_ns = {}
        self.chapter_completed = {}
        self.chapter_death_counts = {}
        self.checkpoints_completed = {}
        self.hearts = {}
        self.cassettes = {}

        if xml == "":
            pass
        else:
            return self.from_xml(xml)

    def from_xml(self, xml):

        save_file = ET.fromstring(xml)

        self.total_time_100_ns = int(save_file.find("Time").text)
        self.death_count = int(save_file.find("TotalDeaths").text)

        self.current_session_id = int(save_file.find("CurrentSession").get("ID"))
        self.current_session_mode = save_file.find("CurrentSession").get("Mode")
        self.current_session_time = int(save_file.find("CurrentSession").get("Time"))
        self.current_session_deaths = int(
            save_file.find("CurrentSession").get("Deaths")
        )
        self.current_session_berries = save_file.find("CurrentSession").findall(
            "Strawberries"
        )
        self.current_session_cassette = save_file.find("CurrentSession").get("Cassette") == "true"
        self.current_session_heart = save_file.find("CurrentSession").get("HeartGem") == "true"

        areas_data = save_file.find("Areas")

        self.total_chapter_times_100_ns = {}
        self.best_chapter_times_100_ns = {}
        self.chapter_completed = {}
        self.chapter_death_counts = {}
        self.checkpoints_completed = {}
        self.hearts = {}
        self.cassettes = {}

        for area_data in areas_data.findall("AreaStats"):
            chapter_id = int(area_data.get("ID"))

            sides = area_data.find("Modes").findall("AreaModeStats")
            has_sides = chapter_id in (
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                9,
            )  # ids of levels that have b- and c-sides

            self.cassettes[chapter_id] = area_data.get("Cassette") == "true"

            if has_sides:
                for side_id in range(3 if has_sides else 1):
                    level_id = constants.LEVEL_CODE_BY_ID[chapter_id] + (
                        constants.SIDE_CODE_BY_ID[side_id] if has_sides else ""
                    )
                    self.total_chapter_times_100_ns[level_id] = int(
                        sides[side_id].get("TimePlayed")
                    )
                    self.best_chapter_times_100_ns[level_id] = int(
                        sides[side_id].get("BestTime")
                    )
                    self.chapter_completed[level_id] = (
                        sides[side_id].get("Completed") == "true"
                    )
                    self.chapter_death_counts[level_id] = int(
                        sides[side_id].get("Deaths")
                    )
                    self.checkpoints_completed[level_id] = len(
                        sides[side_id].find("Checkpoints").findall("string")
                    )
                    if self.chapter_completed[level_id]:
                        self.checkpoints_completed[level_id] += 1
                    self.hearts[level_id] = sides[side_id].get("HeartGem") == "true"
