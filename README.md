# Ortopilot-Stream-Indexer
The Streamer Ortopilot uploads VODs after his streams.

This tool indexes the songs played on stream and gives a time in seconds (maybe give a youtube link?)

## Usage
`python main.py [YoutubeURL] [options]`

This will download and index the video.

### Options
| option |  description  |
|--------|---------------|
|  -o / --Output | Specify the output file. If the file already exists, it will append to it. Default is the same as the video file|
| -v / --Video | Specify video file to analyse (if you have already downloaded it)|

## Requirements
Besides all the python requirements (pytesseract, opencv-python, pytube), you need [tesseract](https://github.com/tesseract-ocr/tesseract) installed and it needs to be in your PATH
