import requests

class SpotifyClient:
    def __init__(self, url, client_id, client_secret, auth_url):
        self.url = url
        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = ""
    
    def get_url(self):
        return self.url

    def generate_token(self):
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        auth_response = requests.post(self.auth_url, data=data)
        self.token = auth_response.json().get('access_token')
        return self.token   

    def get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self.token}'
        }

    def get_playlist_info(self, playlist_id):
        url = f"{self.url}playlists/{playlist_id}"
        resp = requests.get(url=url, headers=self.get_auth_headers())
        return resp.json()

    def get_playlist_tracks(self, playlist_id):
        tracks = list()
        url = f"{self.url}playlists/{playlist_id}/tracks"
        resp = requests.get(url=url, headers=self.get_auth_headers())
        if resp.json().get('next') == None:
            tracks += self._parse_playlist_tracks(resp)
        else:
            while resp.json().get('next') != None:
                tracks += self._parse_playlist_tracks(resp)
                resp = requests.get(url=resp.json().get('next'), headers=self.get_auth_headers())
        return tracks

    def _parse_playlist_tracks(self, payload):
        all = list()
        for track_info in payload.json().get('tracks').get('items'):
            track = track_info.get('track')
            artists = ""
            for a in track.get('artists'):
                artists += a.get('name') + " "
            all.append({
                'name': track.get('name'),
                'artists': artists.strip()
            })
        return all