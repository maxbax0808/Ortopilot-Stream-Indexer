#!/usr/bin/python
from pytube import YouTube
import cv2
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from Levenshtein import distance as lev


def progress(stream, chunk, file_handle, bytes_remaining):
    contentSize = video.filesize
    size = contentSize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
        '█' * int(size * 20 / contentSize), ' ' * (20 - int(size * 20 / contentSize)), float(size / contentSize * 100)),
          end='')


def download(url):
    yt = YouTube(url, on_progress_callback=progress)
    video = yt.streams.filter(res="720p").first()
    video.download()


def extractSongName(image):
    pictureString = pytesseract.image_to_string(image, lang="eng")
    song = ""
    try:
        song = pictureString[pictureString.index("CURRENT SONG"): pictureString.index("\n", pictureString.index("CURRENT SONG"))]
    except ValueError:
        song = "CURRENT SONG: -"
    return song


if __name__ == '__main__':
    #download('https://www.youtube.com/watch?v=JwBXgJeqeOs')
    vidcap = cv2.VideoCapture('Weds July 14th 21.mp4')
    frame = 0
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    success, image = vidcap.read()
    crop = image[640:720, 230:230+500]
    currentSongname = extractSongName(crop)
    oldSongname = ""
    #print(currentSongname)
    frame += 30*10
    while success:
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = vidcap.read()
        crop = image[640:720, 230:230 + 500]
        currentSongname = extractSongName(crop)
        if lev(currentSongname, oldSongname)>2:
            print("Sekunde: %i Songname: %s" % (frame/30, currentSongname))
        oldSongname = currentSongname
        frame += 30*10
