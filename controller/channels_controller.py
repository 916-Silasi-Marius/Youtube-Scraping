from datetime import datetime
import os
import time
from model.youtube_channel import YoutubeChannel


class ChannelsController:
    def __init__(self, repository, api, eliminated):
        self.__repo = repository
        self.__eliminated_repo = eliminated
        self.__api = api

    def get_channel_ids_controller(self, keyword):
        return self.__api.get_channel_ids(keyword)

    def create_file_name(self, keywords):
        name = ""
        now = datetime.now()
        name += now.strftime("%d-%m-%Y -- %H-%M")
        for keyword in keywords:
            name += ' - ' + keyword
        name += '.csv'
        full_path = os.path.join(os.getcwd(), name)
        self.__repo.repo_set_file_name(full_path)
        return now.strftime("%d-%m-%Y")

    def process_keywords(self, keywords):
        channel_ids = []
        channels_per_keyword = []
        for keyword in keywords:
            temp_list, last_date = self.__api.get_channel_ids(keyword)
            temp_to_string = []
            for item in temp_list:
                temp_to_string.append(item['snippet']['channelId'])
            temp_to_string = list(dict.fromkeys(temp_to_string))
            temp_to_string = self.__eliminated_repo.check_for_duplicates(temp_to_string)
            temp_to_string = self.__repo.check_for_duplicates(temp_to_string)
            while len(temp_to_string) < 50:
                temp_list, last_date = self.__api.get_channel_ids_before(keyword, last_date)
                for item in temp_list:
                    temp_to_string.append(item['snippet']['channelId'])
                temp_to_string = list(dict.fromkeys(temp_to_string))
                temp_to_string = self.__eliminated_repo.check_for_duplicates(temp_to_string)
                temp_to_string = self.__repo.check_for_duplicates(temp_to_string)
            channel_ids += temp_to_string
            print(len(temp_to_string), end='')
            print(' channels for ', end='')
            print(keyword)
            channels_per_keyword.append({'keyword': keyword, 'count': len(temp_to_string)})
        channel_ids = list(dict.fromkeys(channel_ids))
        return channel_ids, channels_per_keyword

    def gather_data(self, channel, date, keyword):
        subscriber_count = self.__api.get_subscriber_count(channel)
        last_published_video = self.__api.get_last_published_video(channel)
        average_views = self.__api.get_average_views(channel)
        average_likes = self.__api.get_average_likes(channel)
        average_comments = self.__api.get_average_comments(channel)
        if average_comments.find('NOT') == -1 and average_likes.find('NOT') == -1 and average_views.find('NOT') == -1:
            if average_views.find('!') == -1:
                relevance = (float(average_comments) + float(average_likes) * 0.3) / float(average_views)
            else:
                relevance = "NOT AVAILABLE"
        else:
            relevance = "NOT AVAILABLE"
        posting_frequency = self.__api.get_posting_frequency(channel)
        country = self.__api.get_country(channel)
        instagram = self.__api.get_instagram()
        email = self.__api.get_email()
        topics = self.__api.get_topics(channel)
        self.__repo.add_channel(YoutubeChannel(channel, subscriber_count, last_published_video, average_views,
                                               average_likes, average_comments, relevance, posting_frequency, country,
                                               instagram, email, topics, date, keyword))

    def filter_results(self):
        channels = self.__repo.get_channels()
        to_be_eliminated = []
        for channel in channels:
            if channel.get_subscriber_count().find('!!!!!') != -1 or channel.get_average_views().find('!!!!!') != -1 \
                    or channel.get_last_published_video().find('!!!!!') != -1 \
                    or channel.get_country().find('!!!!!') != -1 or channel.get_average_views().find("NOT") != -1 or \
                    channel.get_average_likes().find("NOT") != -1 or channel.get_average_comments().find("NOT") != -1:
                to_be_eliminated.append(channel)

        return_list = []
        for channel in channels:
            if channel not in to_be_eliminated:
                return_list.append(channel)
            else:
                self.__eliminated_repo.add_channel(channel)
        self.__repo.filter_list(return_list)

    def get_channels(self):
        return self.__repo.get_channels()

    def get_eliminated(self):
        return self.__eliminated_repo.get_channels()

    def save_results(self):
        self.__repo.save_results()
        time.sleep(1.5)
        self.__eliminated_repo.save_results()
