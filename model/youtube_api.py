import json
from datetime import datetime
from model.date import Date
import re


class YouTubeAPI:
    def __init__(self, service):
        self.__service = service

    def get_channel_ids(self, keyword):
        req = self.__service.search().list(part='id,snippet', q=keyword, maxResults=50, order='date')
        res = req.execute()
        return res['items'], res['items'][len(res['items']) - 1]['snippet']['publishedAt']

    def get_channel_ids_before(self, keyword, last_date):
        req = self.__service.search().list(part='id,snippet', q=keyword, maxResults=50, order='date',
                                           publishedBefore=last_date)
        res = req.execute()
        return res['items'], res['items'][len(res['items']) - 1]['snippet']['publishedAt']

    def get_subscriber_count(self, channel_id):
        req = self.__service.channels().list(part='statistics, topicDetails', id=channel_id)
        res = req.execute()
        try:
            if 'subscriberCount' in res['items'][0]['statistics']:
                if 'videoCount' in res['items'][0]['statistics']:
                    if int(res['items'][0]['statistics']['videoCount']) > 5:
                        return res['items'][0]['statistics']['subscriberCount']
                    else:
                        return res['items'][0]['statistics']['subscriberCount'] + '!!!!!'
            else:
                return "NOT AVAILABLE"
        except KeyError:
            return "NOT AVAILABLE"

    def get_last_published_video(self, channel_id):
        req = self.__service.activities().list(part='contentDetails,snippet', channelId=channel_id, maxResults=1)
        res = req.execute()
        try:
            if len(res['items']) > 0:
                last_posted = Date(int(res['items'][0]['snippet']['publishedAt'][:4]),
                                   int(res['items'][0]['snippet']['publishedAt'][5:7]),
                                   int(res['items'][0]['snippet']['publishedAt'][8:10]))
                today = datetime.now()
                today = today.strftime("%Y-%m-%d")
                today = Date(int(today[:4]), int(today[5:7]), int(today[8:10]))
                if last_posted.get_days_gap(today).days <= 90:
                    return res['items'][0]['snippet']['publishedAt']
                else:
                    return res['items'][0]['snippet']['publishedAt'] + '!!!!!'
            else:
                return 'ACTIVITY NOT AVAILABLE'
        except KeyError:
            return 'ACTIVITY NOT AVAILABLE'

    def get_video_views(self, video_id):
        req = self.__service.videos().list(part='statistics', id=video_id)
        res = req.execute()
        try:
            if 'viewCount' in res['items'][0]['statistics']:
                return res['items'][0]['statistics']['viewCount']
            else:
                return -1
        except KeyError:
            return -1

    def get_average_views(self, channel_id):
        req = self.__service.activities().list(part='contentDetails,snippet', channelId=channel_id, maxResults=8)
        res = req.execute()
        try:
            if len(res['items']) > 0:
                video_ids = []
                for item in res['items']:
                    if item['snippet']['type'] == 'upload':
                        video_ids.append(item['contentDetails']['upload']['videoId'])

                views = []
                for item in video_ids:
                    views.append(self.get_video_views(item))

                min_views = 0x3f3f3f3f
                max_views = -1
                total = 0
                for item in views:
                    total += int(item)
                    min_views = min(int(item), min_views)
                    max_views = max(int(item), max_views)

                if len(views) - 2 > 0:
                    if (total - min_views - max_views) / (len(views) - 2) > 200:
                        return str((total - min_views - max_views) / (len(views) - 2))
                    else:
                        return str((total - min_views - max_views) / (len(views) - 2)) + '!!!!!'
                else:
                    return 'NOT ENOUGH RESOURCE'
            else:
                return 'ACTIVITY NOT AVAILABLE'
        except KeyError:
            return 'ACTIVITY NOT AVAILABLE'

    def get_video_likes(self, video_id):
        req = self.__service.videos().list(part='statistics', id=video_id)
        res = req.execute()
        try:
            if 'likeCount' in res['items'][0]['statistics']:
                return res['items'][0]['statistics']['likeCount']
            else:
                return -1
        except KeyError:
            return -1

    def get_average_likes(self, channel_id):
        req = self.__service.activities().list(part='contentDetails,snippet', channelId=channel_id, maxResults=8)
        res = req.execute()
        try:
            if len(res['items']) > 0:
                video_ids = []
                for item in res['items']:
                    if item['snippet']['type'] == 'upload':
                        video_ids.append(item['contentDetails']['upload']['videoId'])

                likes = []
                for item in video_ids:
                    likes.append(self.get_video_likes(item))

                min_likes = 0x3f3f3f3f
                max_likes = -1
                total = 0
                for item in likes:
                    total += int(item)
                    min_likes = min(int(item), min_likes)
                    max_likes = max(int(item), max_likes)

                if len(likes) - 2 > 0:
                    return str((total - min_likes - max_likes) / (len(likes) - 2))
                else:
                    return 'NOT ENOUGH RESOURCE'
            else:
                return 'ACTIVITY NOT AVAILABLE'
        except KeyError:
            return 'ACTIVITY NOT AVAILABLE'

    def get_video_comments(self, video_id):
        req = self.__service.videos().list(part='statistics', id=video_id)
        res = req.execute()
        try:
            if 'commentCount' in res['items'][0]['statistics']:
                return res['items'][0]['statistics']['commentCount']
            else:
                return -1
        except KeyError:
            return -1

    def get_average_comments(self, channel_id):
        req = self.__service.activities().list(part='contentDetails,snippet', channelId=channel_id, maxResults=8)
        res = req.execute()
        try:
            if len(res['items']) > 0:
                video_ids = []
                for item in res['items']:
                    if item['snippet']['type'] == 'upload':
                        video_ids.append(item['contentDetails']['upload']['videoId'])

                comments = []
                for item in video_ids:
                    comments.append(self.get_video_comments(item))

                min_comments = 0x3f3f3f3f
                max_comments = -1
                total = 0
                for item in comments:
                    total += int(item)
                    min_comments = min(int(item), min_comments)
                    max_comments = max(int(item), max_comments)

                if len(comments) - 2 > 0:
                    return str((total - min_comments - max_comments) / (len(comments) - 2))
                else:
                    return 'NOT ENOUGH RESOURCE'
            else:
                return 'ACTIVITY NOT AVAILABLE'
        except KeyError:
            return 'ACTIVITY NOT AVAILABLE'

    def get_posting_frequency(self, channel_id):
        req = self.__service.activities().list(part='contentDetails,snippet', channelId=channel_id, maxResults=8)
        res = req.execute()
        with open('activity.json', 'w') as f:
            json.dump(res, f, indent=4)
        try:
            if len(res['items']) > 0:
                posting_dates = []
                for item in res['items']:
                    if item['snippet']['type'] == 'upload':
                        posting_dates.append(item['snippet']['publishedAt'])

                dates = []
                for item in posting_dates:
                    dates.append(Date(int(item[:4]), int(item[5:7]), int(item[8:10])))

                days_gaps = []
                for i in range(len(dates) - 1):
                    days_gaps.append(dates[i].get_days_gap(dates[i + 1]))

                min_days = 0x3f3f3f3f
                max_days = -1
                total = 0

                for item in days_gaps:
                    total += item.days
                    min_days = min(min_days, item.days)
                    max_days = max(max_days, item.days)

                if len(days_gaps) - 2 > 0:
                    return str((total - min_days - max_days) / (len(days_gaps) - 2))
                elif len(days_gaps) > 0:
                    return str(total / len(days_gaps))
                else:
                    return 'NOT ENOUGH RESOURCE'
            else:
                return 'ACTIVITY NOT AVAILABLE'
        except KeyError:
            return 'ACTIVITY NOT AVAILABLE'

    def get_country(self, channel_id):
        req = self.__service.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
        res = req.execute()
        with open('stats.json', 'w') as f:
            json.dump(res, f, indent=4)
        try:
            if "country" in res['items'][0]['snippet']:
                with open("Data/config.json", 'r') as f:
                    data = json.load(f)
                    country = data['country']
                if res['items'][0]['snippet']['country'] == country:
                    return res['items'][0]['snippet']['country']
                else:
                    return res['items'][0]['snippet']['country'] + '!!!!!'
            else:
                return "NOT AVAILABLE"
        except KeyError:
            return 'NOT AVAILABLE'

    @staticmethod
    def get_instagram():
        result = "NOT AVAILABLE"
        with open('activity.json', 'r') as f:
            for line in f:
                if line.find('instagram.com') != -1:
                    result = line[line.find('instagram.com'):]
                    break
        if result != "NOT AVAILABLE":
            if result.find('/', 14) is not None:
                result = result[:result.find('/', 14) + 1]
            if result.find('\\') is not None:
                result = result[:result.find("\\")]
            return result
        else:
            with open('stats.json', 'r') as f:
                for line in f:
                    if line.find('instagram.com') != -1:
                        result = line[line.find('instagram.com'):]
                        break
                if result != "NOT AVAILABLE":
                    if result.find('/', 14) is not None:
                        result = result[:result.find('/', 14) + 1]
                    if result.find('\\') is not None:
                        result = result[:result.find("\\")]
                return result

    @staticmethod
    def get_email():
        result = []
        with open('stats.json', 'r') as f:
            content = f.read()
            content = content.split('\\n')
            email_pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9._]+.[a-zA-Z0-9._]+")
            for item in content:
                result += re.findall(email_pattern, item)
        if len(result) == 0:
            with open('activity.json', 'r') as f:
                content = f.read()
                content = content.split('\\n')
                email_pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9._]+.[a-zA-Z0-9._]+")
                for item in content:
                    result += re.findall(email_pattern, item)
        return_list = []
        for item in result:
            if item.find("\\") != -1:
                return_list.append(item[:item.find("\\")])
            else:
                return_list.append(item)
        return return_list

    def get_topics(self, channel_id):
        req = self.__service.channels().list(part='topicDetails', id=channel_id)
        res = req.execute()
        try:
            if 'topicDetails' in res['items'][0]:
                if 'topicCategories' in res['items'][0]['topicDetails']:
                    topics = ""
                    for item in res['items'][0]['topicDetails']['topicCategories']:
                        topics += item[item.find('wiki/') + 5:] + ';'
                    return topics
                else:
                    return 'NOT AVAILABLE'
            else:
                return 'NOT AVAILABLE'
        except KeyError:
            return 'NOT AVAILABLE'
