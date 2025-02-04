# Discord YouTube Notification Bot

## Overview
This is a Discord bot that monitors specified YouTube channels and notifies a designated Discord channel whenever a new video is uploaded.

## Features
- Uses the YouTube Data API to track new video uploads.
- Allows users to pass YouTube channel handles instead of manually finding channel IDs.
- Sends a notification with the video link to a specified Discord channel.
- Runs continuously, checking for updates at regular intervals.

## Requirements
- Python 3.8+
- A Google Cloud API Key with YouTube Data API access.
- A Discord bot token.
- Required Python packages:
  - `google-api-python-client`
  - `discord.py`
  - `asyncio`
  - `argparse`

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/yt_notify_discoBot.git
   cd yt_notify_discoBot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the `config.json` file with the following keys:
   ```json
   {
     "youtube_token": "YOUR_YOUTUBE_API_KEY",
     "disco_token": "YOUR_DISCORD_BOT_TOKEN",
     "channel_id": "YOUR_DISCORD_CHANNEL_ID",
     "time_interval": 3600,
     "application_id": "YOUR_DISCORD_APPLICATION_ID"
   }
   ```
4. Run the bot with your desired YouTube channel handles:
   ```sh
   python bot.py --handles fireship mrbeast premierleague beINSPORTS
   ```

## Configuration
- **Check Interval**: Modify the `TIME_INTERVAL` value in `config.json` to change the frequency of YouTube checks.

## How It Works
1. The bot retrieves the latest uploads from the specified YouTube channels using their handles.
2. It compares the latest video ID with the last known video.
3. If a new video is found, the bot sends the YouTube video link to the configured Discord channel.
4. The process repeats at the specified time interval.

## Limitations
- If a non-existent YouTube handle is provided, the bot will not acknowledge it. Future updates may handle this more gracefully.

## Author
**Ahmed Senger**  
Created on: 01/02/2024

## License
This project is open-source. Feel free to modify and contribute!
