#!/usr/bin/python
from pytube import YouTube
import cv2
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from Levenshtein import distance as lev
import argparse


def progress(self, stream, chunk):
    pass


def download(url):
    yt = YouTube(url, on_progress_callback=progress)
    video = yt.streams.filter(res="720p").first()
    video.download()
    return video.default_filename


def extractSongName(image):
    pictureString = pytesseract.image_to_string(image, lang="eng")
    song = ""
    try:
        song = pictureString[pictureString.index("CURRENT SONG"): pictureString.index("\n", pictureString.index("CURRENT SONG"))]
    except ValueError:
        song = "CURRENT SONG: -"
    return song


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL of the youtube Video to analyse")
    parser.add_argument("-o", "--Output", help="Specify output file. Defaults to filename of video.", type=argparse.FileType('a'), dest='outputfile')
    parser.add_argument("-v", "--Video", help="Specify video file to analyse. If this option is given, nothing will be downloaded")

    args = parser.parse_args()

    if args.url:
        title = download(args.url)
        vidcap = cv2.VideoCapture(title)
    else:
        if args.Video:
            vidcap = cv2.VideoCapture(args.Video)
            title = args.Video
        else:
            print("Please provide an url or a video")

    frame = 0
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, image = vidcap.read()
    crop = image[640:720, 230:230+500]
    currentSongname = extractSongName(crop)
    oldSongname = currentSongname

    frame += 30*10
    while success:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = vidcap.read()
        if not success:
            print("Done detecting songs")
            quit(1)
        crop = image[640:720, 230:230 + 500]
        currentSongname = extractSongName(crop)
        if lev(currentSongname, oldSongname)>2:
            m, s = divmod(frame/30, 60)
            h, m = divmod(m, 60)
            if args.outputfile:
                args.outputfile.write("Timestamp: {:1.0f}:{:2.0f}:{:2.0f}; Sekunde: {:6.0f}; Songname: {}\n".format(h, m, s, frame/30, currentSongname))
                args.outputfile.flush()
            else:
                with open(title + ".txt", 'a') as outputfile:
                    outputfile.write("Timestamp: {:1.0f}:{:2.0f}:{:2.0f}; Sekunde: {:6.0f}; Songname: {}\n".format(h, m, s, frame/30, currentSongname))
                    outputfile.flush()
            print("Timestamp: {:1.0f}:{:2.0f}:{:2.0f}; Sekunde: {:6.0f}; Songname: {}".format(h, m, s, frame/30, currentSongname))
        oldSongname = currentSongname
        frame += 30*10
