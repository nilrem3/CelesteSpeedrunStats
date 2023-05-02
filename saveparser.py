import xml.etree.ElementTree as ET


LEVEL_CODE_BY_ID = {
    0: "prologue",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "epilogue",
    9: "8",
    10: "9"
}

SIDE_CODE_BY_ID = {
    0: "a",
    1: "b",
    2: "c"
}


class CelesteSaveData:
    def __init__(self, xml: str):
        save_file = ET.fromstring(xml)

        self.total_time_100_ns = int(save_file.find("Time").text)
        self.death_count = int(save_file.find("TotalDeaths").text)

        areas_data = save_file.find("Areas")

        self.total_chapter_times_100_ns = {}
        self.best_chapter_times_100_ns = {}
        self.chapter_completed = {}
        self.chapter_death_counts = {}
        self.checkpoints_completed = {}

        for area_data in areas_data.findall("AreaStats"):
            chapter_id = int(area_data.get("ID"))

            sides = area_data.find("Modes").findall("AreaModeStats")
            has_sides = chapter_id in (1, 2, 3, 4, 5, 6, 7, 9)  # ids of levels that have b- and c-sides

            if has_sides:
                for side_id in range(3):
                    level_id = LEVEL_CODE_BY_ID[chapter_id] + SIDE_CODE_BY_ID[side_id]
                    self.total_chapter_times_100_ns[level_id] = int(sides[side_id].get("TimePlayed"))
                    self.best_chapter_times_100_ns[level_id] = int(sides[side_id].get("BestTime"))
                    self.chapter_completed[level_id] = sides[side_id].get("Completed") == "true"
                    self.chapter_death_counts[level_id] = int(sides[side_id].get("Deaths"))
                    self.checkpoints_completed[level_id] = len(sides[side_id].find("Checkpoints").findall("string"))
                    if self.chapter_completed[level_id]:
                        self.checkpoints_completed += 1
            else:
                level_id = LEVEL_CODE_BY_ID[chapter_id]
                self.total_chapter_times_100_ns[level_id] = int(sides[0].get("TimePlayed"))
                self.best_chapter_times_100_ns[level_id] = int(sides[0].get("BestTime"))
                self.chapter_completed[level_id] = sides[0].get("Completed") == "true"
                self.chapter_death_counts[level_id] = int(sides[0].get("Deaths"))
                self.checkpoints_completed[level_id] = len(sides[0].find("Checkpoints").findall("string"))
                if self.chapter_completed[level_id]:
                    self.checkpoints_completed[level_id] += 1

