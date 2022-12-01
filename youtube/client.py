import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# todo add delete playlist method

class YoutubeClient():
    def __init__(self, secrets_file, scopes, api_service_name, api_version):
        self.secrets_file = secrets_file
        self.scopes = scopes
        self.api_service_name = api_service_name
        self.api_version = api_version
        self.client = self._run_oauth_flow()

    def _run_oauth_flow(self):
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.secrets_file, self.scopes
        )
        creds = flow.run_console()
        return self._create_client(creds)
    
    def _create_client(self, creds):
        return googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=creds
        )
    
    def get_playlists(self):
        request = self.client.playlists().list(
            part = "snippet,contentDetails",
            maxResults = 25,
            mine = True
        )
        return request.execute()

    def create_playlist(self, title):  # todo - update to take args
        request = self.client.playlists().insert(
            part = "snippet,status",
            body = {
                "snippet": {
                    "title": title,
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
        )
        return request.execute()

    def insert_playlist_item(self, playlist_id, video_id):
        request = self.client.playlistItems().insert(
            part = "snippet",
            body = {
                "snippet": {
                    "playlistId": f"{playlist_id}",
                    "position": 0,
                    "resourceId": {
                    "kind": "youtube#video",
                    "videoId": f"{video_id}"
                    }
                }
            }
        )
        return request.execute()
        

    def search(self, term):
        request = self.client.search().list(
            part = "snippet",
            maxResults = 25,
            q = term
        )
        return request.execute()