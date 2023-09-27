from django.shortcuts import render
from .forms import Youtube
from youtubesearchpython import VideosSearch
from django.urls import reverse
from pytube import YouTube
import speech_recognition as sr

# Create your views here.
def youtube(request):
    if request.method == 'POST':
        form = Youtube(request.POST)
        if form.is_valid():
            text = request.POST['search']
            videosSearch = VideosSearch(text, limit = 20)
            lists = []
            for i in videosSearch.result()["result"]:
                data = {
                    'title':i["title"],
                    'channel':i["channel"].get("name"),
                    'duration':i["accessibility"].get("duration"),
                    'views':i["viewCount"].get("short"),
                    'publish':i["publishedTime"],
                    #'description':i["descriptionSnippet"][0].get("text"),
                    'link':i["link"],
                    'thumbnail':i["thumbnails"][0].get("url"),
                    'id':i["id"]
                }
                description = ''
                if i["descriptionSnippet"]:
                   for j in i["descriptionSnippet"]:
                       description += j["text"]
                       data['description'] = description
                    
                lists.append(data)
    else:
        form = Youtube()
        lists = []
    return render(request, 'youtube.html', {'form':form, 'lists':lists})
def content(request,title=None,channel=None, id=None):
   # recognizer = sr.Recognizer()
    title = title
    link = f'https://www.youtube.com/watch?v={id}'
    channel = channel
    mainVideo = YouTube(link)
    stream = mainVideo.streams.filter(only_audio=True).first()
    extension = 'mav'
    name_of_file = f'{mainVideo.title}.{extension}'
    audio= stream.download(filename=name_of_file)
    print(audio)
    #audio_s = recognizer.record(sr.AudioFile(audio))
#
    #text = recognizer.recognize_google(audio_s)
    #text = recognizer.recognize_sphinx(audio_s)

    return render(request, 'content.html', {'link': link, 'title':title, 'channel':channel,'audio':audio})
