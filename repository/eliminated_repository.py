import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials


class EliminatedRepository:
    def __init__(self):
        self.__eliminated = []
        self.__new_eliminated = []
        self.__sheet = self.access_sheet()
        self.read_from_sheet()

    @staticmethod
    def access_sheet():
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('Data/client_secret.json', scope)
        client = gspread.authorize(credentials)
        return client.open("Channels").get_worksheet(1)

    def read_from_sheet(self):
        records = self.__sheet.get_all_records()
        for record in records:
            if len(record['Channel ID']) > 30:
                self.__eliminated.append(record['Channel ID'][32:])
            else:
                self.__eliminated.append(record['Channel ID'])

    def check_for_duplicates(self, channels):
        to_be_eliminated = []
        for channel in channels:
            if channel in self.__eliminated:
                to_be_eliminated.append(channel)

        return_list = []
        for channel in channels:
            if channel not in to_be_eliminated:
                return_list.append(channel)

        return return_list

    def add_channel(self, channel):
        self.__new_eliminated.append(channel)

    def get_channels(self):
        return self.__new_eliminated

    def save_results(self):
        for channel in self.__new_eliminated:
            to_write = channel.to_string().replace('!!!!!', '')
            self.__sheet.append_row(to_write.split(','), 'RAW')
            time.sleep(1.5)
