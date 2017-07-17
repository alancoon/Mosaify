import argparse
import sys
import requests
import os

import spotipy
import spotipy.util as util

import math
from io import BytesIO
from PIL import Image

class Wallpapyr(object):
    def __init__(self, args):
        self.store_arguments(args)
        self.initialize_spotipy()
        self.authenticate()
        self.create_mosaic(self.get_top_albums())

    def store_arguments(self, args):
        self.username = args.user
        self.quality = args.quality
        self.rectangle = args.rectangle
        self.output = args.output
        self.validate_arguments()
        
    def validate_arguments(self):
        filename, file_extension = os.path.splitext(self.output)
        suitable_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        if file_extension.lower() not in suitable_extensions:
            print('Unsuitable filetype')
            raise Exception

    def initialize_spotipy(self):
        self.SPOTIPY_CLIENT_ID = '<YOUR SPOTIPY CLIENT ID>'
        self.SPOTIPY_CLIENT_SECRET = '<YOUR SPOTIPY CLIENT SECRET>'
        self.SPOTIPY_REDIRECT_URI = 'http://localhost:8080'

    def authenticate(self):
        scope = 'user-top-read'
        token = util.prompt_for_user_token(self.username, scope, client_id = self.SPOTIPY_CLIENT_ID, client_secret = self.SPOTIPY_CLIENT_SECRET, redirect_uri = self.SPOTIPY_REDIRECT_URI)
        
        if token:
            self.launch_client(token)
        else:
            print('Cannot get token for', username)
    
    def launch_client(self, token):
        self.client = spotipy.Spotify(auth = token)
        self.client.trace = False
    
    def quality_resolver(self, quality):
        quality_dict = {'high': 0, 'medium': 1, 'low': 2}
        if quality not in quality_dict:
            raise Exception
        else:
            return quality_dict[quality]

    def quality_index_resolver(self, quality_index):
        quality_index_dict = {0: (640, 640), 1: (300, 300), 2: (64, 64)}
        return quality_index_dict[quality_index]

    def check_queue(self, queue, name_of_album):
        for item in queue:
            if item[0] in name_of_album or name_of_album in item[0]:
                return True
        return False

    def add_term_to_queue(self, queue, term, quality_index):
        for track in term['items']:
            album = track['album']
            album_images = album['images']
            url = album_images[quality_index]['url']
            tuple = (album['name'], url)
            album_is_duplicate = self.check_queue(queue, album['name'])
            if not album_is_duplicate:
                print(album['name'], 'added to queue')
                queue.append(tuple)

    def get_top_albums(self):  
        queue = []
        long_term_tracks = self.client.current_user_top_tracks(limit = 50, time_range = 'long_term')
        medium_term_tracks = self.client.current_user_top_tracks(limit = 50, time_range = 'medium_term')
        short_term_tracks = self.client.current_user_top_tracks(limit = 50, time_range = 'short_term')
        quality_index = self.quality_resolver(self.quality)
        self.add_term_to_queue(queue, long_term_tracks, quality_index)
        self.add_term_to_queue(queue, medium_term_tracks, quality_index)
        self.add_term_to_queue(queue, short_term_tracks, quality_index)
        return queue

    def create_mosaic(self, albums):
        number_of_albums = len(albums)
        if self.rectangle:
            rows = 5
            columns = math.ceil(number_of_albums / rows) 
        else:
            rows = math.floor(math.sqrt(number_of_albums))
            columns = math.floor(number_of_albums / rows)
        quality_index = self.quality_resolver(self.quality)
        (height, width) = self.quality_index_resolver(quality_index)

        mosaic = Image.new('RGB', (columns * width, rows * height))
        for i in range(0, columns * width, width):
            for j in range(0, rows * height, height):
                if albums:
                    current_album = albums.pop(0)
                    print('Requesting album art for URI:', current_album[0])
                    response = requests.get(current_album[1])
                    mosaic.paste(Image.open(BytesIO(response.content)), (i, j))
                    print('Albums left:', len(albums))
        
        mosaic.save(self.output)

def parse():
    parser = argparse.ArgumentParser(description = 'Wallpapyr arguments')
    parser.add_argument('user', help = 'Your Spotify username')
    parser.add_argument('-q', '--quality', choices = ['low', 'medium', 'high'], default = 'high', help = 'Quality of images, default is high')
    rect_help = 'Enables rectangular wallpaper production, rather than discarding excess images, program will create a rectangular frame'
    parser.add_argument('-r', '--rectangle', action = 'store_true', help = rect_help)
    parser.add_argument('-o', '--output', help = 'Specify an output filename, .jpg .jpeg .gif .png .bmp accepted', default = 'out.png')
    return parser.parse_args() 


def main():
    wp = Wallpapyr(parse());

if __name__ == '__main__':
    main()




