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
    10: "9",
}


SIDE_CODE_BY_ID = {0: "a", 1: "b", 2: "c"}


SIDE_CODE_BY_MODE = {"Normal": "a", "BSide": "b", "CSide": "c"}

ENDS_WITH_HEART = {
    "prologue": False,
    "1a": False,
    "1b": True,
    "1c": True,
    "2a": False,
    "2b": True,
    "2c": True,
    "3a": False,
    "3b": True,
    "3c": True,
    "4a": False,
    "4b": True,
    "4c": True,
    "5a": False,
    "5b": True,
    "5c": True,
    "6a": False,
    "6b": True,
    "6c": True,
    "7a": False,
    "7b": True,
    "7c": True,
    "epilogue": False,
    "8a": False,
    "8b": True,
    "8c": True,
    "9": False,
}

# UNFINISHED
FINAL_ROOM_BY_LEVEL_ID = {
    "prologue": "3",
    "1a": "end",
    "1b": "",
    "1c": "",
    "2a": "end_6",
    "2b": "",
    "2c": "",
    "3a": "roof_7",
    "3b": "",
    "3c": "",
    "4a": "d-10",
    "4b": "",
    "4c": "",
    "5a": "e-11",
    "5b": "d-05",
    "5c": "",
    "6a": "after-02",
    "6b": "",
    "6c": "",
    "7a": "summit_checkpoint_1",
    "7b": "",
    "7c": "",
    "epilogue": "inside",
    "8a": "",
    "8b": "",
    "8c": "",
    "9": "",
}


CHECKPOINTS_BY_LEVEL_ID = {
    "prologue": 1,
    "1a": 3,
    "1b": 3,
    "1c": 1,
    "2a": 3,
    "2b": 3,
    "2c": 1,
    "3a": 4,
    "3b": 4,
    "3c": 1,
    "4a": 4,
    "4b": 4,
    "4c": 1,
    "5a": 5,
    "5b": 4,
    "5c": 1,
    "6a": 6,
    "6b": 4,
    "6c": 1,
    "7a": 7,
    "7b": 7,
    "7c": 1,
    "epilogue": 1,
    "8a": 4,
    "8b": 4,
    "8c": 1,
    "9": 9,
}


RED_BERRY_IDS_BY_LEVEL = {
    "prologue": [],
    "1a": [
        "2:11",
        "3:9",
        "5z:10",
        "5:21",
        "7zb:2",
        "9z:3",
        "8b:1",
        "9:14",
        "9b:9",
        "5a:2",
        "s1:9",
        "7z:3",
        "8zb:1",
        "3b:2",
        "6:12",
        "7a:12",
        "11:9",
        "10zb:1",
        "9c:2",
        "12z:8",
    ],
    "1b": [],
    "1c": [],
    "2a": [
        "d2:9",
        "d1:67",
        "d0:6",
        "d4:6",
        "d2:31",
        "1:1",
        "4:4",
        "8:18",
        "9:22",
        "10:27",
        "12d:44",
        "end_3c:13",
        "d3:10",
        "d6:2",
        "d5:12",
        "5:15",
        "9b:5",
        "12c:7",
    ],
    "2b": [],
    "2c": [],
    "3a": [
        "s2:18",
        "s2:6",
        "00-a:5",
        "00-b:42",
        "04-b:14",
        "06-a:7",
        "06-b:14",
        "06-c:3",
        "07-b:4",
        "10-y:2",
        "13-b:31",
        "11-d:52",
        "06-d:238",
        "04-c:40",
        "03-b:1",
        "03-b:25",
        "roof06:276",
        "roof06:308",
        "12-c:1",
        "12-y:1",
        "13-x:13",
        "roof03:97",
        "s3:2",
        "05-c:2",
        "08-x:4",
    ],
    "3b": [],
    "3c": [],
    "4a": [
        "a-02:8",
        "a-03:33",
        "a-04:11",
        "a-07:16",
        "b-04:1",
        "b-07:15",
        "b-03:5",
        "b-01:6",
        "b-01:13",
        "b-02:20",
        "b-08:11",
        "c-00:17",
        "c-06b:43",
        "c-06:35",
        "c-08:28",
        "d-00b:11",
        "d-01:7",
        "d-07:70",
        "a-01x:11",
        "a-06:6",
        "a-10:13",
        "a-09:12",
        "c-05:21",
        "c-10:55",
        "d-04:88",
        "d-09:18",
        "b-02:58",
        "b-secb:9",
        "c-01:26",
    ],
    "4b": [],
    "4c": [],
    "5a": [
        "a-05:22",
        "a-03:4",
        "a-02:23",
        "a-11:2",
        "a-14:12",
        "b-18:2",
        "b-01c:85",
        "b-03:24",
        "b-05:23",
        "d-15:217",
        "d-19:533",
        "b-17:10",
        "a-00x:7",
        "a-01:256",
        "a-01:164",
        "a-04:2",
        "a-07:6",
        "a-06:2",
        "a-15:182",
        "b-21:99",
        "b-20:72",
        "b-20:183",
        "b-10:4",
        "b-12:3",
        "b-17:14",
        "c-08:112",
        "d-04:122",
        "d-04:16",
        "d-15:335",
        "d-13:157",
        "e-06:56",
    ],
    "5b": [],
    "5c": [],
    "6a": [],
    "6b": [],
    "6c": [],
    "7a": [
        "a-04b:85",
        "a-04b:136",
        "a-05:54",
        "b-02:101",
        "b-04:67",
        "b-08:129",
        "d-00:43",
        "d-04:388",
        "d-07:484",
        "e-09:398",
        "e-10:515",
        "f-00:590",
        "f-07:711",
        "f-08b:856",
        "f-08c:759",
        "g-00b:127",
        "g-00b:114",
        "g-01:279",
        "g-01:342",
        "d-01c:226",
        "b-02b:102",
        "c-03b:228",
        "c-07b:291",
        "c-05:248",
        "c-06b:281",
        "c-08:331",
        "d-03:383",
        "d-08:527",
        "a-02b:61",
        "b-02e:112",
        "b-09:167",
        "c-09:354",
        "d-01d:282",
        "d-10b:682",
        "e-02:7",
        "e-05:237",
        "e-07:473",
        "e-12:504",
        "e-11:425",
        "e-13:829",
        "f-01:639",
        "f-11:1068",
        "f-11:1229",
        "f-11:1238",
        "g-00b:37",
        "g-01:66",
        "g-03:1504",
    ],
    "7b": [],
    "7c": [],
    "epilogue": [],
    "8a": ["b-06:174", "c-00b:211", "c-02:248", "c-03b:276", "d-06:130"],
    "8b": [],
    "8c": [],
    "9": [],
}

LEVEL_IDS = [
    "prologue",
    "1a",
    "1b",
    "1c",
    "2a",
    "2b",
    "2c",
    "3a",
    "3b",
    "3c",
    "4a",
    "4b",
    "4c",
    "5a",
    "5b",
    "5c",
    "6a",
    "6b",
    "6c",
    "7a",
    "7b",
    "7c",
    "epilogue",
    "8a",
    "8b",
    "8c",
    "9",
]

HELP_MESSAGE = """
help: displays this message
help advanced: display help message for advanced commands.
quit: closes the program
practice help: learn more about practice marking
tag help: learn more about tags
category help: learn more about setting your run category
comment <words>: add words as a comment on the most recent uploaded run.
"""

ADVANCED_HELP_MESSAGE = """
===ADVANCED MODE===
these commands shouldn't be necessary to use this program, but advanced users may find them helpful in certain cases.
setloglevel <n>: sets the verbosity of the logging system.  0 is the most verbose, 4 is the least.
"""

PRACTICE_HELP_MESSAGE = """
Practice options are used to automatically mark certain runs or sessions as practice for stat sorting. Thresholds do not save if you close the tracker, you will have to re-set them.
practice [on|off|auto]
    on: always mark runs as practice
    off: never mark runs as practice
    auto: runs will be marked as practice if they meet auto thresholds
practice auto [clear|deaths|time] [deaths|time|<n>]
    clear:
        deaths: clear deaths threshold
        time: clear time threshold
    deaths <n>: set practice deaths threshold to n.  Runs with more than n deaths will be marked as practice.
    time <n>: set practice time threshold to n.  Runs longer than n seconds will be marked as practice.
"""

TAG_HELP_MESSAGE = """
Tags are used to add custom sortable tags to your runs and sessions for stat sorting. Tags do not save if you close the tracker, you will have to re-set them.
tag add <tags>: add tags (a comma separated list) to the current set of tags.  
    list: show the current set of tags
    clear: remove all current tags.
"""

CATEGORY_HELP_MESSAGE = """
Category is used to keep track of what you are running and used for sorting data, your category will be automatically changed if the program detects a new run.
category set <category>: set the current category to category.
         current: prints the current set category
         list: lists all category options
"""

VANILLA_SAVE_SLOTS = ["0", "1", "2", "debug"]

IL_CAT_STR_TO_CAT = {
    "Clear": 0,
    "clear": 0,
    "Full Clear": 1,
    "full clear": 1,
    "FC": 1,
    "fc": 1,
    "All Red Berries+Heart": 2,
    "all red berries+heart": 2,
    "ARB+Heart": 2,
    "ARB+heart": 2,
    "arb+heart": 2,
    "Heart+Cassette": 3,
    "heart+cassette": 3,
    "Dashless": 4,
    "dashless": 4,
}

IL_CATEGORIES = [
    "Clear",
    "Full Clear",
    "All Red Berries+Heart",
    "Heart+Cassette",
    "Dashless",
]
