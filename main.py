import os
import discord
import time
from dotenv import dotenv_values
from youtube.client import YoutubeClient
from spotify.client import SpotifyClient

# todo - add logger

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # idk if this is necessary tbh

config = dotenv_values()
scopes = config.get('YOUTUBE_API_SCOPES').split(',')

intents = discord.Intents.default()
intents.message_content = True
disc = discord.Client(intents=intents)

youtube = YoutubeClient(
    secrets_file = config.get('YOUTUBE_CLIENT_SECRETS_FILE'),
    scopes = config.get('YOUTUBE_API_SCOPES').split(','),
    api_service_name = 'youtube',
    api_version = 'v3'
    )

spotify = SpotifyClient(
    url = config.get('SPOTIFY_API_URL'), 
    client_id = config.get('SPOTIFY_CLIENT_ID'), 
    client_secret = config.get('SPOTIFY_CLIENT_SECRET'),
    auth_url = config.get('SPOTIFY_AUTH_URL')
    )

def convert_spotify_playlist(url, title):
    spotify.generate_token()  # maybe this can be moved to class constructor? fio ttl on token
    tracks = spotify.get_playlist_tracks(playlist_id=url.split('/')[-1])
    if len(tracks) > 0:
        yt_playlist = youtube.create_playlist(title=title)
        for track in tracks:
            yt_track = youtube.search(
                f"{track.get('name')} {track.get('artists')}"
            )
            youtube.insert_playlist_item(
                playlist_id = yt_playlist.get('id'),
                video_id = yt_track.get('items')[0].get('id').get('videoId')
                )
    return f"https://www.youtube.com/playlist?list={yt_playlist.get('id')}"


if __name__ == "__main__":
    # todo - playlist management thru disc bot?
    @disc.event
    async def on_message(message):

        if message.author == disc.user:
            return

        elif message.content.startswith('-sp'):
            await message.channel.send(f"ok chill {message.author.mention} i'll do it in a sec")
            playlist = convert_spotify_playlist(
                    url = message.content.split(' ')[-1],
                    title = f'{message.author}-{round(time.time()*1000)}'
                    )
            await message.channel.send(f'{message.author.mention} {playlist}')

    disc.run(config.get('DISCORD_BOT_TOKEN'))