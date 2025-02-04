#-------------------------------------
# Author: Ahmed Senger
# Created at: 1/2/2024
#-------------------------------------

"""
This is a Discord bot that keeps an eye on your favorite YouTube channels and notifies a server channel
whenever a new video is uploaded. All you need to do is to provide youtube channels handles and it'll do the rest.
You also need to create a discord applciation on the discord development port before you can use this code.

Note that youtube handle is the word that comes after the @ symbol on a youtube channel main page.
If you entered a handle for youtube channel that doesn't exist, the bot won't acknowledge that.
This may be dealt with in future versions, but for now, be sure of youtube handles that you pass.
"""

import googleapiclient.discovery
import googleapiclient.errors
import json
import discord
import asyncio
import argparse

# getting youtube channels handles:
parser = argparse.ArgumentParser(
    description=(
        "A Discord bot that monitors YouTube channels for new video uploads. \n"
        "The bot retrieves each channel's global 'uploads' playlist based on the provided handles \n"
        "and continuously checks for new uploads, sending notifications to a Discord server channel."
    ),
    epilog="first_bot_v2.py --handles fireship mrbeast premierleague beINSPORTS"
)
parser.add_argument(
    "--handles", 
    required= True, 
    nargs='+',
    metavar= "ytChannel_1 ytChannel_2 ytChannel_3 ytChannel_n",
    help="Pass the handles of youtube channels that you want to monitor."
    )
args = parser.parse_args()

yt_channels = args.handles
# Keeping track of the last known video from each channel to avoid duplicate notifications.
yt_latest_vids = []

# Load API keys and bot config from a JSON file.
client_secrets_file = "D:\\My Notes\\Projects\\Discord_Apps\\config.json"
with open(client_secrets_file, 'r') as config:
    config = json.load(config)

# Extract required tokens and config values
YT_TOKEN = config["youtube_token"]
DISCO_TOKEN = config["disco_token"]
CHANNEL_ID = int(config["channel_id"])
TIME_INTERVAL = config["time_interval"]

# Initialize the Discord bot
intents = discord.Intents.default()
client = discord.Client(
    intents=intents,
    application_id=config["application_id"],
    enable_debug_events=True
)

def yt_loop():
    """
    Calls the YouTube API to check for new uploads from the specified channels.
    If a new video is detected, it generates a YouTube URL and yields it.
    """
    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=YT_TOKEN
    )
    # Retrieve the upload playlist for each channel
    uploads_playlists = []
    for channel_handle in yt_channels:
        request = youtube.channels().list(
            part="contentDetails",
            forHandle=channel_handle
        )
        response = request.execute()
        uploads_playlists.append(response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"])
    
    # Check the latest video in each upload playlist
    for index, playlist in enumerate(uploads_playlists):
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist
        )
        response = request.execute()
        last_vid = response["items"][0]["contentDetails"]["videoId"]
        
        # If a new video is detected, yield its URL
        try:
            if last_vid != yt_latest_vids[index]:
                yt_latest_vids[index] = last_vid
                yield f"https://www.youtube.com/watch?v={last_vid}"
        except IndexError:
            yt_latest_vids.append(last_vid)
            yield f"https://www.youtube.com/watch?v={last_vid}" 

@client.event
async def on_ready():
    """
    This function runs when the bot successfully connects to Discord.
    It continuously checks YouTube for new uploads and posts any new videos to the specified channel.
    """
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("Invalid channel ID! Check your config file.")
        return
    
    while True:
        for url in yt_loop():
            await channel.send(url)
        
        # Wait for 1 hour before checking YouTube again
        await asyncio.sleep(3600)

if __name__ == "__main__":
    client.run(DISCO_TOKEN)
