from django.shortcuts import render
from .forms import Youtube
from youtubesearchpython import VideosSearch
from django.urls import reverse
from pytube import YouTube
import os
import openai
#import speech_recognition as sr
import assemblyai as aai
from django.http import JsonResponse
from .models import Content_Blog



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
def transcrib(link):
    aai.settings.api_key = f'openai api'
    mainVideo = YouTube(link)
    stream = mainVideo.streams.filter(only_audio=True).first()
    extension = 'mp3'
    name_of_file = f'{mainVideo.title}.{extension}'
    audio=stream.download(filename=name_of_file)
    FILE_URL =audio
    # pip install -U assemblyai
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(FILE_URL)
    text  = transcript.text
    return text
def openai_text(text):
    openai.api_key = 'assembleai api'
    prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article:\n\n{text}\n\nArticle:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    generated_content = response.choices[0].text.strip()
    return generated_content

def content(request,title=None,channel=None, id=None):
    if request.method == 'POST':
   # recognizer = sr.Recognizer()
       title = title
       link = f'https://www.youtube.com/watch?v={id}'
       channel = channel
       transcriber = transcrib(link)
       text = openai_text(transcriber)
       if not text:
           return JsonResponse({'error': " Failed to get transcript"}, status=500)
       if not text:
           return JsonResponse({'error': " Failed to generate blog article"}, status=500)
       new_blog_article = Content_Blog.objects.create(
            user=request.user,
            youtube_title=title,
            youtube_link=link,
            generated_content=text,
        )
       new_blog_article.save()
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
       #print(transcript.text)
       #print(f'duration {transcript.audio_duration}')    
    return render(request, 'content.html', {'text': text, 'title':title, 'channel':channel})
