import json
import requests

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import youtube_dl

from secrets import spotify_token, user_id


class CreatePlaylist:

    def __init__(self):
        self.song_info = {}
        self.youtube_client = self.get_youtube_api_client()

    # Gets a youtube api client for logging into youtube and accessing liked videos in get_liked_videos
    # Copied from the api explorer at https://developers.google.com/youtube/v3/docs/videos/list
    def get_youtube_api_client(self):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # Using a youtube api client, get the 50 newest liked videos
    def get_liked_videos(self):
        request = self.youtube_client.videos().list(
            part="snippet,contentDetails,statistics",
            maxResults=50,
            myRating="like"
        )
        response = request.execute()

        return response

    # Given a song name and artist, query the spotify ap to get and return the uri for that song
    def get_spotify_uri(self, song_name, artist):
        """
        Search for a song
        Query should look as follows:
        https://api.spotify.com/v1/search?query=track:song_name artist:artist&type=track&limit=20&offset=5
        with relevant encoding for spaces and colons
        """
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track&limit=20&offset=0".format(
            song_name,
            artist
        )
        # Create a json request that gets the spotify uri for a song given the song and artist name
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )
        response_json = response.json()
        song = response_json["tracks"]["items"]

        return song[0]["uri"]

    # Create a spotify playlist and return the id for that playlist
    def create_spotify_playlist(self):
        # The user id is imported from the secrets file.
        # Create a query to gain access to the user's playlists
        query = "https://api.spotify.com/v1/users/{}/playlists".format(user_id)
        response = requests.post(
            query,
            data=json.dumps({
                "name": "Test Playlist",
                "description": "Testing out the feature",
                "public": "false"
            }),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        response_json = response.json()
        return response_json["id"]

    # Add all the songs to the spotify playlist created earlier
    def add_songs_to_playlist(self):
        self.get_song_info()
        uris = []
        # Go through all the songs in song_info and add the uri to uris[]
        for key in self.song_info:
            uris.append(self.song_info[key]["spotify_uri"])

        playlist_id = self.create_spotify_playlist()

        # Create a query to gain access to the tracks of the playlist with the id returned from create_spotify_playlist
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
        # post the query, the uris of the songs to be added, and the appropriate headers
        response = requests.post(
            query,
            data=json.dumps({"uris": uris}),
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(spotify_token)
            }
        )

        if response.status_code < 200 or response.status_code > 205:
            print("Could not add songs to playlist")

        response_json = response.json()

        print(response_json)

    """ Go through all the liked videos and check if the video has an artist and song name, if the has, 
        add it to the song_info dictionary, along with the spotify uri"""
    def get_song_info(self):
        videos = self.get_liked_videos()
        for item in videos["items"]:
            title = item["snippet"]["title"]
            url = "https://www.youtube.com/watch?v={}".format(item["id"])
            video = youtube_dl.YoutubeDL().extract_info(url, False)
            song_name = video["track"]
            artist = video["artist"]

            if song_name is not None and artist is not None:
                self.song_info[title] = {
                    "url": url,
                    "song_name": song_name,
                    "artist": artist,
                    # Get and add the spotify uri to add it to the playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)
                }


if __name__ == '__main__':
    createPlaylist = CreatePlaylist()
    createPlaylist.add_songs_to_playlist()
