# reddit-publisher

## Requirements
- ffmpeg
- tkinter

```
apt install python3-tk ffmpeg
```

## Setup
```
python3 -m venv .venv
source .venv/bin/activate
pip install praw
```

## Usage

Setup an app on https://www.reddit.com/prefs/apps/

Get application id and secret and fill `praw.ini` file