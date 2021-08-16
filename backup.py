from main import *
import json
client_id = get_id()
client_secret = get_client_secret()
playlist_id = get_playlist_id(
    "https://open.spotify.com/playlist/3yCw34zzlSGr3CMcFrLgK8?si=20121727c0464e86")
playlist = sp.playlist(playlist_id=playlist_id)
# print(playlist)
json_playlist = json.dumps(playlist, indent=4)
with open("playlist.json", "w") as outfile:
    outfile.write(json_playlist)
music_id_list = []
for item in playlist['tracks']['items']:
    music_track = item['track']
    music_id_list.append(music_track['id'])
print(f"Your playlist has {len(music_id_list)} songs")
data = []
metas = []
for id in music_id_list:
    t_data = get_track_data(id)
    data.append(t_data)
    meta = sp.track(track_id=id)
    metas.append(meta)


with open("details.json", "w") as outfile:
    outfile.write(json.dumps(data, indent=4))

# Get details from playlist itself


# def get_from_playlist(p):
#     tracks = p['tracks']['items']
#     for track in tracks:
#         print(track)
#         custom_track_data={"id":track['id'],"name":track['name'], ""}
