from googleapiclient.errors import HttpError


class Console:
    def __init__(self, controller):
        self.__controller = controller
        self.__keywords = []

    def run(self):
        try:
            self.__keywords = input("Provide keywords for search:").replace(' ', '').split(',')
            date = self.__controller.create_file_name(self.__keywords)
            channels, channels_per_keyword = self.__controller.process_keywords(self.__keywords)
            print(len(channels), end=' ')
            print('results to be processed...')
            n = 0
            channels_per_keyword_count = 1
            keyword_count = 0
            for channel in channels:
                if channels_per_keyword_count > channels_per_keyword[keyword_count]['count']:
                    keyword_count += 1
                    channels_per_keyword_count = 1
                n += 1
                channels_per_keyword_count += 1
                print(n, end='. ')
                print(channel)
                self.__controller.gather_data(channel, date, channels_per_keyword[keyword_count]['keyword'])
        except HttpError:
            print("NO MORE REQUESTS!")

        self.__controller.filter_results()
        self.__controller.save_results()

        print(len(self.__controller.get_channels()), end='')
        print(' new channels were inserted in the database!')
        print(len(self.__controller.get_eliminated()), end='')
        print(' new channels were saved in the eliminated list!')
