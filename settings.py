


class Setting:
    def __init__(self, name, question, processing_function=None):
        self.name = name
        self.question = question
        self.processing_function = processing_function

    def get_from_user(self):
        val = input(self.question)
        if self.processing_function is None:
            return val
        else:
            return self.processing_function(val)

SETTINGS = [
    Setting("CelesteSaveFolder", "Path to your Celeste save folder: "),
    Setting("ILSaveSlot", "Save slot you do IL runs on: "),
    Setting("AnyPercentSaveSlot", "Save slot you do any% runs on: "),
    Setting("SheetUrl", "URL of the spreadsheet to track times in")
]
