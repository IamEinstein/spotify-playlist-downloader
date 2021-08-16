from __future__ import unicode_literals
# https://open.spotify.com/playlist/7kCXUhukUUnNYe5p7TkYfT?si=0f81e47275ed44c3
import re
import pafy
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pathlib import Path

# Basic functions


def get_id():
    from cryptography.fernet import Fernet
    f1 = open('./res/key.encrypt', "rb")
    key = f1.read()
    f1.close()

    fernet = Fernet(key)
    f2 = open("./res/encrypt.djank", "rb")
    encrypted = f2.read()
    f2.close()

    decMessage = fernet.decrypt(encrypted).decode()
    return decMessage


def get_client_secret():
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    file_in = open("./res/encrypted_data.bin", "rb")

    private_key = RSA.import_key(open("./res/private.pem").read())

    enc_session_key, nonce, tag, ciphertext = \
        [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return data.decode()


# Base setup
client_id = get_id()
# client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
client_secret = get_client_secret()
client_creds_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_creds_manager)


# ! Spotify Functions
# Function to get playlist id from playlist url
def create_folder(download_path, *args, **kwargs):
    try:
        os.mkdir(download_path)
    except FileExistsError:
        # for i in range(100):
        #     download_path = str(Path.home() / "Downloads" /
        #                         "MusicDownloader" / playlist_name)
        #     if FileExistsError:
        #         continue
        #     else:
        #         break
        pass


def get_playlist_id(url):
    import re
    pattern = r'https://open.spotify.com/playlist/.{22}\?.{16}'
    pattern2 = r'https://open.spotify.com/playlist/.{22}'

    if re.match(pattern, url) or re.match(pattern2, url):
        playlist_id = url[34:56]
        return playlist_id
    else:
        return "Invalid URL"


# Function to get ids of songs from playlist id

download_path = ""


def get_track_ids(playlist_id):
    music_id_list = []
    playlist = sp.playlist(playlist_id=playlist_id)
    playlist_name = playlist['name']
    global download_path
    download_path = str(Path.home() / "Downloads" /
                        "MusicDownloader" / playlist_name)
    create_folder(download_path=download_path, playlist_name=playlist_name)

    for item in playlist['tracks']['items']:
        music_track = item['track']
        music_id_list.append(music_track['id'])
    print(f"Your playlist has {len(music_id_list)} songs")
    return music_id_list

# Function to get data of song from song id


def get_track_data(track_id):
    meta = sp.track(track_id=track_id)
    track_details = {"name": meta['name'], "album": meta['album']
                     ['name'], "artist": meta["album"]['artists'][0]['name'], "id": meta['id'], "url": meta['external_urls']['spotify']}
    return track_details

# Function to export the data of all tracks in a playlist


def export_track_data(id):
    track_ids = get_track_ids(id)
    tracks = []
    for i in track_ids:
        time.sleep(0.5)
        track_details = get_track_data(i)
        tracks.append(track_details)

    return tracks


# ! Youtube Functions
def re_check(url):

    re1 = re.search(r'https://youtube.com/watch\?v=.+', url)
    re2 = re.search(r'https://www.youtube.com/watch\?v=.+', url)
    if re1 == None and re2 == None:
        return False
    else:
        return True


def search(song, singer):
    from youtubesearchpython import VideosSearch
    search = VideosSearch(f'{song} by {singer}', limit=1)

    links = []
    for i in search.result()['result']:
        links.append(i['link'])

    return links


def search_from_data(tracks):

    song_links = []
    for i in tracks:
        song_name = i['name']
        singer = i['artist']
        link = search(song_name, singer)
        song_links.append(link[0])
    return song_links

# DOWNLOADING


def download_audio(url):
    vid = pafy.new(url)
    bestaudio = vid.getbestaudio()
    bestaudio.download(filepath=download_path)


# Main
def main():
    try:
        os.mkdir(Path.home() / "Downloads" /
                 "MusicDownloader")
    except FileExistsError:
        pass
    playlist_url = input("Enter playlist url\n")
    playlist_id = get_playlist_id(playlist_url)
    if playlist_id == "Invalid URL":
        print("Playlist URL is not valid")
        quit()
    else:
        print("Okay, we are getting your songs, please wait")
    tracks = export_track_data(playlist_id)
    song_links = search_from_data(tracks)
    print(f"We are downloading the songs to {download_path}")
    for url in song_links:
        download_audio(url)
    print(f"We've downloaded the songs to {download_path}")
    input("Type enter to quit.")


if __name__ == "__main__":
    main()
