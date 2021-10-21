import json
from googleapiclient.discovery import build
from model.youtube_api import YouTubeAPI
from view.console import Console
from repository.channels_repository import ChannelsRepository
from controller.channels_controller import ChannelsController
from repository.eliminated_repository import EliminatedRepository
import os


if __name__ == '__main__':
    with open("Data/config.json", 'r') as f:
        data = json.load(f)
        api_key = data['api_key']
    service = build('youtube', 'v3', developerKey=api_key)
    myAPI = YouTubeAPI(service)
    eliminated_repo = EliminatedRepository()
    repo = ChannelsRepository()
    ctr = ChannelsController(repo, myAPI, eliminated_repo)
    program = Console(ctr)
    program.run()
    try:
        os.remove('activity.json')
        os.remove('stats.json')
    except FileNotFoundError:
        pass
