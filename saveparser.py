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

RED_BERRY_IDS_BY_LEVEL = {
    "prologue": [],
    "1a": ["2:11", "3:9", "5z:10", "5:21", "7zb:2", "9z:3", "8b:1", "9:14", "9b:9", "5a:2", "s1:9", "7z:3", "8zb:1", "3b:2", "6:12", "7a:12", "11:9", "10zb:1", "9c:2", "12z:8"],
    "1b": [],
    "1c": [],
    "2a": ["d2:9", "d1:67", "d0:6", "d4:6", "d2:31", "1:1", "4:4", "8:18", "9:22", "10:27", "12d:44", "end_3c:13", "d3:10", "d6:2", "d5:12", "5:15", "9b:5", "12c:7"],
    "2b": [],
    "2c": [],
    "3a": ["s2:18", "s2:6", "00-a:5", "00-b:42", "04-b:14", "06-a:7", "06-b:14", "06-c:3", "07-b:4", "10-y:2", "13-b:31", "11-d:52", "06-d:238", "04-c:40", "03-b:1", "03-b:25", "roof06:276", "roof06:308", "12-c:1", "12-y:1", "13-x:13", "roof03:97", "s3:2", "05-c:2", "08-x:4"],
    "3b": [],
    "3c": [],
    "4a": ["a-02:8", "a-03:33", "a-04:11", "a-07:16", "b-04:1", "b-07:15", "b-03:5", "b-01:6", "b-01:13", "b-02:20", "b-08:11", "c-00:17", "c-06b:43", "c-06:35", "c-08:28", "d-00b:11", "d-01:7", "d-07:70", "a-01x:11", "a-06:6", "a-10:13", "a-09:12", "c-05:21", "c-10:55", "d-04:88", "d-09:18", "b-02:58", "b-secb:9", "c-01:26"],
    "4b": [],
    "4c": [],
    "5a": ["a-05:22", "a-03:4", "a-02:23", "a-11:2", "a-14:12", "b-18:2", "b-01c:85", "b-03:24", "b-05:23", "d-15:217", "d-19:533", "b-17:10", "a-00x:7", "a-01:256", "a-01:164", "a-04:2", "a-07:6", "a-06:2", "a-15:182", "b-21:99", "b-20:72", "b-20:183", "b-10:4", "b-12:3", "b-17:14", "c-08:112", "d-04:122", "d-04:16", "d-15:335", "d-13:157", "e-06:56"],
    "5b": [],
    "5c": [],
    "6a": [],
    "6b": [],
    "6c": [],
    "7a": ["a-04b:85", "a-04b:136", "a-05:54", "b-02:101", "b-04:67", "b-08:129", "d-00:43", "d-04:388", "d-07:484", "e-09:398", "e-10:515", "f-00:590", "f-07:711", "f-08b:856", "f-08c:759", "g-00b:127", "g-00b:114", "g-01:279", "g-01:342", "d-01c:226", "b-02b:102", "c-03b:228", "c-07b:291", "c-05:248", "c-06b:281", "c-08:331", "d-03:383", "d-08:527", "a-02b:61", "b-02e:112", "b-09:167", "c-09:354", "d-01d:282", "d-10b:682", "e-02:7", "e-05:237", "e-07:473", "e-12:504", "e-11:425", "e-13:829", "f-01:639", "f-11:1068", "f-11:1229", "f-11:1238", "g-00b:37", "g-01:66", "g-03:1504"],
    "7b": [],
    "7c": [],
    "epilogue": [],
    "8a": ["b-06:174", "c-00b:211", "c-02:248", "c-03b:276", "d-06:130"],
    "8b": [],
    "8c": [],
    "9": []
}


class CelesteSaveData:
    def __init__(self, xml: str):
        save_file = ET.fromstring(xml)

        self.file_name = save_file.find("Name").text

        self.total_time_100_ns = int(save_file.find("Time").text)
        self.death_count = int(save_file.find("TotalDeaths").text)

        areas_data = save_file.find("Areas")

        self.total_chapter_times_100_ns = {}
        self.best_chapter_times_100_ns = {}
        self.best_chapter_full_complete_times_100_ns = {}
        self.chapter_completed = {}
        self.chapter_full_completed = {}
        self.chapter_death_counts = {}
        self.checkpoints_completed = {}
        self.hearts = {}
        self.cassettes = {}
        self.num_red_berries = {}

        for area_data in areas_data.findall("AreaStats"):
            chapter_id = int(area_data.get("ID"))

            sides = area_data.find("Modes").findall("AreaModeStats")
            has_sides = chapter_id in (1, 2, 3, 4, 5, 6, 7, 9)  # ids of levels that have b- and c-sides

            self.cassettes[chapter_id] = area_data.get("Cassette") == "true"
            self.best_chapter_times_100_ns[chapter_id] = area_data.get("BestFullClearTime")
            self.chapter_full_completed[chapter_id] = area_data.get("FullClear") == "true"

            if has_sides:
                for side_id in range(3 if has_sides else 1):
                    level_id = LEVEL_CODE_BY_ID[chapter_id] + (SIDE_CODE_BY_ID[side_id] if has_sides else "")
                    self.total_chapter_times_100_ns[level_id] = int(sides[side_id].get("TimePlayed"))
                    self.best_chapter_times_100_ns[level_id] = int(sides[side_id].get("BestTime"))
                    self.chapter_completed[level_id] = sides[side_id].get("Completed") == "true"
                    self.chapter_death_counts[level_id] = int(sides[side_id].get("Deaths"))
                    self.checkpoints_completed[level_id] = len(sides[side_id].find("Checkpoints").findall("string"))
                    if self.chapter_completed[level_id]:
                        self.checkpoints_completed += 1
                    self.hearts[level_id] = sides[side_id].get("HeartGem") == "true"
                    self.num_red_berries[level_id] = 0
                    for berry in sides[side_id].find("Strawberries").findall("EntityID"):
                        if berry.get("Key") in RED_BERRY_IDS_BY_LEVEL[level_id]: # make sure it's a red berry not a golden
                            self.num_red_berries += 1

