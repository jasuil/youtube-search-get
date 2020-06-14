#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

from module import make

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "REPLACE_ME"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

videoIds = []
videoNames = []

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                  developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  channels = []
  playlists = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videoIds.append(search_result["id"]["videoId"])
      videoNames.append(search_result["snippet"]["title"])


if __name__ == "__main__":
  argparser.add_argument("--q", help="Search term", default="레드벨뱃")
  argparser.add_argument("--max-results", help="Max results", default=100)
  args = argparser.parse_args()

  try:
    youtube_search(args)
    for idx in range(len(videoIds)):
      make(videoNames[idx - 1], videoIds[idx - 1])
  except HttpError as e:
    print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
