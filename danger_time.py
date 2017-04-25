import json
import subprocess
from datetime import datetime
import re

class DangerTime:

    ''' Time wasted is dangerous! '''

    def __init__(self):
        self.file_location = "/home/XXXXXXXX/.mozilla/firefox/XXXXXXXXX/sessionstore-backups/recovery.js" # Temporary hardcoding.
        self.file_tab_dictionary = {}
        self.final_tab_dictionary = {}
        self.current_tabs = []

    def copy_recovery_file(self):
        # Need to determine profile and file location path.
        subprocess.call(["cp", self.file_location, "."])

    def parse_open_tabs(self):
        with open("recovery.js", encoding='utf-8') as tab_file:
            self.file_tab_dictionary = json.load(tab_file)

        self.tab_list = self.file_tab_dictionary["windows"][0]["tabs"]

        self.current_tabs = []
        self.end_tabs = []
        
        for tab in self.tab_list:
            current_tab = tab["entries"][0]
            title = current_tab["title"]
            if re.search(",", title):
                title.replace("," ," ")
            if title in self.final_tab_dictionary.keys(): # Tab still open.
                pass
            else: # New tab.
                self.final_tab_dictionary[title] = current_tab["url"]
                self.final_tab_dictionary[title + "-start"] = datetime.now().strftime('%H:%M:%S')

            self.current_tabs.append(title)
            

        for key in self.final_tab_dictionary.keys():
            if key not in self.current_tabs: # Tab closed.
                self.end_tabs.append(key)

        for item in self.end_tabs:
            self.final_tab_dictionary[item + "-end"] = datetime.now().strftime('%H:%M:%S')

    def output_results(self):
        with open("lots_of_danger.csv", "w") as danger_file:
            danger_file.write("Website, URL, Time Spent\n")
            for key in self.final_tab_dictionary.keys():
                if re.search("start", key) or re.search("end", key):
                    pass
                else:
                    end_key = key + "-end"
                    start_key = key + "-start"
                    start_time = self.final_tab_dictionary[start_key]
                    start_time = start_time.split(":")
                    if end_key in self.final_tab_dictionary.keys():
                        end_time = self.final_tab_dictionary[end_key]
                        end_time = end_time.split(":")
                        danger_file.write(key + "," + self.final_tab_dictionary[key] + "," + str((int(end_time[0]) - int(start_time[0])) % 24) + ":"  + str((int(end_time[1]) - int(start_time[1])) % 60) + ":" + str((int(end_time[2]) - int(start_time[2])) % 60) + "\n")
                    else:
                        now_time = datetime.now().strftime('%H:%M:%S')
                        now_time = now_time.split(":")
                        danger_file.write(key + "," + self.final_tab_dictionary[key] + "," + str((int(now_time[0]) - int(start_time[0])) % 24) + ":"  + str((int(now_time[1]) - int(start_time[1])) % 60) + ":" + str((int(now_time[2]) - int(start_time[2])) % 60) + "\n")

danger_time = DangerTime()
while True:
    danger_time.copy_recovery_file()
    danger_time.parse_open_tabs()
    danger_time.output_results()
