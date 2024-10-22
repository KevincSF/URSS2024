import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from isodate import parse_duration,isodatetime
import requests

class youtubeAPI():
    def __init__(self,DEVELOPER_KEY = "",api_service_name = "youtube",api_version = "v3",client_secrets_file = "client_secret.json") -> None:
        self.DEVELOPER_KEY=DEVELOPER_KEY
        self.api_service_name=api_service_name
        self.api_version=api_version
        self.client_secrets_file = client_secrets_file
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        self.flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        self.client_secrets_file, scopes)
        self.credentials = self.flow.run_local_server(port=0)
        self.youtube = googleapiclient.discovery.build(
        self.api_service_name, self.api_version, credentials=self.credentials)
    def get_comments(self, vid: str = "", max_result: int = 100) -> str:
        youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.DEVELOPER_KEY
        )
        if vid == "":
            return None
        json_file = open(f"Data/requests/{vid}.json", "w")
        comment_file = open(f"Data/comments/{vid}.csv", "w")
        comment_file.write("comment|likes|time\n")
        nextPageToken = None
        total_results = 0
        page = 0
        try:
            while total_results < max_result:
                page += 1
                request = youtube.commentThreads().list(
                    part="snippet",
                    videoId=vid,
                    maxResults=min(100, max_result - total_results),
                    pageToken=nextPageToken
                )
                response = request.execute()
                json_file.write(json.dumps(response) + "\n")

                for item in response["items"]:
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                    likes = str(item["snippet"]["topLevelComment"]["snippet"]["likeCount"])
                    time = str(isodatetime.parse_datetime(item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]))
                    comment = comment.replace('\n', ' ').replace('|', " ")
                    comment_file.write(f"{comment}|{likes}|{time}\n")
                total_results += len(response["items"])
                nextPageToken = response.get("nextPageToken")
                if not nextPageToken:
                    print(f"{vid} completed, {total_results} comment, {page} page scraped, ")
                    break
        except googleapiclient.errors.HttpError as e:
            print(e)
            return ["error"]
        finally:
            json_file.close()
            comment_file.close()
        return response
    def get_videos(self,playlistid="",max_result:int =100):
        if playlistid == "":
                return None
        pages = (max_result//50)+1
        result = []
        next_page = ""
        for i in range(pages):
            request = self.youtube.playlistItems().list(
                part="snippet",
                playlistId=playlistid,
                maxResults=max_result,
                pageToken = next_page
            )
            response = request.execute()
            for item in response["items"]:
                id = item["snippet"]["resourceId"]["videoId"]
                publish = str(isodatetime.parse_datetime(item["snippet"]["publishedAt"]))
                title = item["snippet"]["title"]
                result.append(
                    {"vid":id,"title":title,"publish":publish})
            next_page = response["nextPageToken"]
        return result
            
    def request_details(self, vids=[]):
        vid_dict = []
        pages = (len(vids) + 49) // 50 
        for page in range(pages):
            start_index = page * 50
            end_index = min((page + 1) * 50, len(vids))
            vids_string = ",".join([vids[i]["vid"] for i in range(start_index, end_index)])
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=vids_string
            )
            response = request.execute()
            with open(f"video_request_{page}.json", "w") as json_file:
                json.dump(response, json_file)
            for index, item in enumerate(response["items"]):
                vid_dict.append({
                    "vid": vids[start_index + index]["vid"],
                    "title": vids[start_index + index]["title"],
                    "publish": vids[start_index + index]["publish"],
                    "duration": parse_duration(item["contentDetails"]["duration"]).seconds,
                    "views": item["statistics"]["viewCount"]
                })
        return vid_dict