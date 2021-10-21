import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class ChannelsRepository:
    def __init__(self):
        self.__channels = []
        self.__new_channels = []
        self.__file_name = ""
        self.__sheet = self.access_sheet()
        self.read_from_sheet()

    def repo_set_file_name(self, full_path):
        self.__file_name = full_path

    @staticmethod
    def access_sheet():
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('Data/client_secret.json', scope)
        client = gspread.authorize(credentials)
        return client.open("Channels").sheet1

    def read_from_sheet(self):
        records = self.__sheet.get_all_records()
        for record in records:
            self.__channels.append(record['Channel ID'])

    def check_for_duplicates(self, channels):
        to_be_eliminated = []
        for channel in channels:
            if channel in self.__channels:
                to_be_eliminated.append(channel)

        return_list = []
        for channel in channels:
            if channel not in to_be_eliminated:
                return_list.append(channel)
        return return_list

    def add_channel(self, channel):
        self.__new_channels.append(channel)

    def filter_list(self, new_channels):
        self.__new_channels = new_channels

    def get_channels(self):
        return self.__new_channels

    def save_results(self):
        cnt = 0
        with open(self.__file_name, 'w+') as f:
            for channel in self.__new_channels:
                cnt += 1
                if cnt < 60:
                    f.write(channel.to_string())
                    self.__sheet.append_row(channel.to_string().split(','), 'RAW')
                else:
                    time.sleep(65)
                    cnt = 0
            f.close()
