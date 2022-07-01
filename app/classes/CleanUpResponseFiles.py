import os


class CleanupFiles:
    def __init__(self, lstFileName):
        self.lstFileName = lstFileName

    def cleanup(self):
        for f in self.lstFileName:
            print(f'remove {f}')
            os.remove(f)