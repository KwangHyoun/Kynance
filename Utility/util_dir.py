import os.path
import glob
import platform
from Utility.util_print import *

def display_tree(path, max_depth = 100, depth=0):
    for i, obj in enumerate(glob.glob(path+'/*')):
        if depth == 0:
            prefix = '\t' + str(i+1) + '. '
        else:
            prefix = '\t' + '   ' * depth + 'ㄴ'

        if depth < max_depth:
            if os.path.isdir(obj):
                print(prefix + os.path.basename(obj))
                display_tree(obj, max_depth, depth+1)
            elif os.path.isfile(obj):
                print(prefix + os.path.basename(obj))
            else:
                print(prefix + 'unknown object:', obj)

# Set up the iCloud Drive directory according to the operating system under work.
class dirSetting_kynance:
    def __init__(self):
        self.curr_os = None
        self.dir_iCloud = None
        self.dir_kynance = None
        self.dir_analysisTool = None
        self.dir_data = None
        self.dir_utility = None
        self.dir_strategy = None
        self._setting()

    def _setting(self):
        self.curr_os = platform.system()
        if self.curr_os == 'Windows':
            self.dir_iCloud = 'C:/Users/USER/iCloudDrive'
        elif self.curr_os == 'Darwin':
            self.dir_iCloud = '/Users/igwanghyeon/Library/Mobile Documents/com~apple~CloudDocs'
        self.dir_kynance = self.dir_iCloud + '/Package/Kynance'
        self.dir_analysisTool = self.dir_kynance + '/AnalysisTool'
        self.dir_data = self.dir_kynance + '/Data'
        self.dir_strategy = self.dir_kynance + '/Strategy'
        self.dir_utility = self.dir_kynance + '/Utility'

    def display(self):
        print_line('OS information : ' + self.curr_os, 100, pre_len=10)
        print_line('Kynance directory : ' + self.dir_kynance, 100, pre_len=10)
        print_line('Kynance package components', 100, pre_len=10)
        display_tree(os.path.abspath(self.dir_kynance), 1)
