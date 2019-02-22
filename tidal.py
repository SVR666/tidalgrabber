#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import tidalapi
from transliterate import translit
import os
from mutagen.flac import Picture, FLAC
from requests import get

session = tidalapi.Session(tidalapi.Config('LOSSLESS'))
session._config.api_token='BI218mwp9ERZ3PFI'
session.login('YOUR TIDAL LOGIN', 'YOUR TIDAL PASSWORD')

def start():

	if not os.path.exists("music/"):
		os.mkdir("music/")

	mode = input("Mode: \n 1) Playlist grabber\n 2) Track grabber\n 3) Album grabber\n 4) Search \n")

	if int(mode) == 1:
		playlist_id = input("Enter playlist id: ")
		playlist = session.get_playlist_tracks(playlist_id=playlist_id)
		for track in playlist:
			download_flac(track)
		want_start()
	elif int(mode) == 2:
		track_id = input("Enter track id: ")
		track = session._map_request('tracks/'+str(track_id), params={'limit': 100}, ret='tracks')
		download_flac(track)
		want_start()
	elif int(mode) == 3:
		album_id = input("Enter album id: ")
		album = session.get_album_tracks(album_id=album_id)
		for track in album:
			download_flac(track)
		want_start()
	elif int(mode) == 4:
		search_query = input("Enter search query: ")
		search = session.search(field='track', value=search_query)
		for track in search.tracks:
			print(track.artist.name+" - "+track.name+": "+str(track.id))
		want_start()
	else:
		print("Incorrect mode!")
		start()

def download_flac(track):
	url = session.get_media_url(track_id=track.id)
	name = translit(""+track.name, "ru", reversed=True)
	artist_name = translit(""+track.artist.name, "ru", reversed=True)
	album_name = translit(""+track.album.name, "ru", reversed=True)
	releaseDate = str(track.album.release_date)
	print(name+' - '+url)
	album_artist = translit(u""+track.album.artist.name, "ru", reversed=True).encode("UTF-8")
	download(url, 'music/'+name+'.flac')
	download(track.album.image, 'music/'+name+'.png')
	audio = FLAC("music/"+name+".flac")
	albumart = "music/"+name+".png"
	image = Picture()
	image.type = 3
	mime = 'image/png'
	image.desc = 'front cover'
	with open(albumart, 'rb') as f: # better than open(albumart, 'rb').read() ?
		image.data = f.read()
	audio['artist'] = artist_name
	audio['title'] = name
	audio['album'] = album_name
	audio['date'] = releaseDate
	audio.add_picture(image)
	audio.save()
	os.remove("music/"+name+".png")

def download(url, file_name):
	with open(file_name, "wb") as file:
		response = get(url) 											
		file.write(response.content)

def want_start():
	want = input("Do you want to continue [0/1]: ")
	if want == "1":
		start()
	elif want == "0":
		print("OK!")
	else:
		want_start()
start()
