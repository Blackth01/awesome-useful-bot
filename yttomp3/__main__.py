import re, requests, json, subprocess, os, ffmpeg
from pytube import YouTube

class YTToMP3:
    def __init__(self, limit_size=None):
        self.limit_size = limit_size
        self.newfiles = []
        self.error_message = ""

    '''
        Downloads and converts to MP3 a video from YouTube
    '''
    def downloadmp3(self, url_or_keyword):
        
        if(not self.url_is_from_youtube(url_or_keyword)):
            url = self.search_youtube_video(url_or_keyword)
        else:
            url = url_or_keyword
            
        yt = YouTube(url) 

        stream = yt.streams.filter(only_audio=True).first()

        if(self.limit_size):
            if(stream.filesize > self.limit_size):
                self.error_message = "The video is too long!"
                return False
        
        mp4file = stream.default_filename

        print('Found the file %s, downloading it' % mp4file)
        stream.download()

        songname = mp4file.split('.')[0]

        if(not os.path.exists(mp4file)):
            print("File {} not found!".format(mp4file))
            self.error_message = "File {} not found!".format(mp4file)
            return False

        print('Started to convert %s to mp3' % mp4file)
        self.convert_to_mp3(mp4file, songname)
        
        print('New file: %s.mp3' % songname)
        self.newfiles.append(songname)

        return True

    '''
        Converts to MP3 a MP4 file
    '''
    def convert_to_mp3(self, mp4file, songname):
        stream = ffmpeg.input(mp4file)
        audio = stream.audio
        stream = ffmpeg.output(audio, songname+".mp3")
        ffmpeg.run(stream)
        os.remove(mp4file)

    '''
     Verifies if the url is a valid url from YouTube
    '''
    def url_is_from_youtube(self, url):
        regex = re.compile(
                r'^(?:http|https)s?://(www.youtube|youtube).com/', re.IGNORECASE)
                
        valid = re.match(regex, url) is not None
        
        return valid

    '''
     Gets the first YouTube video matching with specific keywords
    '''
    def search_youtube_video(self, keywords):
        url = "https://www.youtube.com/results?search_query="+keywords
        html = requests.get(url).text

        start = 'var ytInitialData = '

        end = "};"

        position = html.find(start)

        firstpart = html[position+len(start):]

        position = firstpart.find(end)

        jsonstring = firstpart[:position+1]

        jsonobject = json.loads(jsonstring)

        videos = jsonobject["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"]

        if(len(videos) < 3):
            videos = videos[0]["itemSectionRenderer"]["contents"]
        else:
            videos = videos[1]["itemSectionRenderer"]["contents"]
            
        i = 0
        while(i < len(videos)):
            if("videoRenderer" in videos[i]):
                videos = videos[i]
                break;
            i+=1

        valid_url = "https://youtube.com/watch?v="+videos["videoRenderer"]["videoId"]
        return valid_url
        