class YoutubeChannel:
    def __init__(self, channel_id, subscriber_count, last_published_video, average_views, average_likes,
                 average_comments, relevance, posting_frequency, country, instagram, topics, scrape_date, scrape_keyword):
        self.__channel_id = channel_id
        self.__subscriber_count = subscriber_count
        self.__last_published_video = last_published_video
        self.__average_views = average_views
        self.__average_likes = average_likes
        self.__average_comments = average_comments
        self.__relevance = relevance
        self.__posting_frequency = posting_frequency
        self.__country = country
        self.__instagram = instagram
        self.__topic = topics
        self.__scrape_date = scrape_date
        self.__scrape_keyword = scrape_keyword

    def get_channel_id(self):
        return self.__channel_id

    def get_subscriber_count(self):
        return self.__subscriber_count

    def get_last_published_video(self):
        return self.__last_published_video

    def get_average_views(self):
        return self.__average_views

    def get_average_likes(self):
        return self.__average_likes

    def get_average_comments(self):
        return self.__average_comments

    def get_relevance(self):
        return self.__relevance

    def get_posting_frequency(self):
        return self.__posting_frequency

    def get_country(self):
        return self.__country

    def get_instagram(self):
        return self.__instagram

    def get_topics(self):
        return self.__topic

    def to_string(self):
        return self.__channel_id + ',' + self.__subscriber_count + ',' + self.__last_published_video + ',' + \
               self.__average_views + ',' + self.__average_likes + ',' + self.__average_comments + ',' + \
               str(self.__relevance) + ',' + self.__posting_frequency + ' days,' + self.__country + ',' + \
               self.__instagram + ',' + self.__topic + ',' + self.__scrape_date + ',' + self.__scrape_keyword + '\n'
