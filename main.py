import webapp2

import os #added
try: 
  import simplejson as json
except:
  import json


from google.appengine.ext.webapp import template

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = "AIzaSyCkg-mkWeEZW0Bbr8MffrZh98J9WupxfV0"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class MainPage(webapp2.RequestHandler):
    
    def get(self):
        youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
        res = youtube.playlistItems().list(
            part="snippet",
            playlistId="PL268622A6AC2178E9",
            maxResults="50"
            ).execute()
        nextPageToken = res.get('nextPageToken')
        while ('nextPageToken' in res):
            nextPage = youtube.playlistItems().list(
                part="snippet",
                playlistId="PL268622A6AC2178E9",
                maxResults="50",
                pageToken=nextPageToken
                ).execute()
            res['items'] = res['items'] + nextPage['items']
            if 'nextPageToken' not in nextPage:
                res.pop('nextPageToken', None)
            else:
                nextPageToken = nextPage['nextPageToken']
        #res['items'] = res['items'].isoformat()
       
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html') 
        self.response.out.write(template.render(path, {'res':res['items']})) 
        #self.response.write("res")
    def post(self):
            youtube = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)
            res = youtube.playlistItems().list(
                part="snippet",
                playlistId="PL268622A6AC2178E9",
                maxResults="50"
                ).execute()
            nextPageToken = res.get('nextPageToken')
            while ('nextPageToken' in res):
                nextPage = youtube.playlistItems().list(
                    part="snippet",
                    playlistId="PL268622A6AC2178E9",
                    maxResults="50",
                    pageToken=nextPageToken
                    ).execute()
                res['items'] = res['items'] + nextPage['items']
                if 'nextPageToken' not in nextPage:
                    res.pop('nextPageToken', None)
                else:
                    nextPageToken = nextPage['nextPageToken']
            #res['items'] = res['items'].isoformat()
            self.response.out.write(json.dumps(res['items'])) 
            #self.response.write("res")

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)