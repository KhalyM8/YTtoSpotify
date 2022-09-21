from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from secrets import client_id, client_secret, redirect_uri, PATH, scope, username
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import sys
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel

s = Service(PATH)
chrome_options = Options()
chrome_options.headless = True
driver = webdriver.Chrome(service = s, options=chrome_options)

token = SpotifyOAuth(scope=scope, username=username, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
spotifyObject = spotipy.Spotify(auth_manager=token)

songs = []


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        with open("style.qss", "r") as qss:
            self.setStyleSheet(qss.read())

        self.setFixedSize(QSize(500,200))
        self.setWindowTitle("Youtube to Spotify")

        self.nameInput = QLineEdit(self)
        self.nameInput.setGeometry(60,70,100,30)
        self.nameLabel = QLabel("Name of playlist",self)
        self.nameLabel.setGeometry(67.5,30,100,30)

        self.descInput = QLineEdit(self)
        self.descInput.setGeometry(200,70,100,30)
        self.descLabel = QLabel("Playlist description",self)
        self.descLabel.setGeometry(201,30,100,30)

        self.urlInput = QLineEdit(self)
        self.urlInput.setGeometry(340,70,100,30)
        self.urlLabel = QLabel("Playlist URL",self)
        self.urlLabel.setGeometry(360,30,100,30)

        self.button = QPushButton("Confirm!", self)
        self.button.clicked.connect(self.confirmButton)
        self.button.setGeometry(200,150,100,30)

    def confirmButton(self):
        playlistName = self.nameInput.text()
        playlistDesc = self.descInput.text()
        playlistURL = self.urlInput.text()
        driver.get(playlistURL)
        time.sleep(10)
        elements = driver.find_elements(By.ID, "video-title")
        for element in elements:
            print(element.text)
            result = spotifyObject.search(q=element.text)
            songs.append(result["tracks"]["items"][0]["uri"])
        driver.quit()
        print(songs)
        spotifyObject.user_playlist_create(user=username, name=playlistName, public=True,
                                           description=playlistDesc)
        prePlaylist = spotifyObject.user_playlists(user=username)
        playlist = prePlaylist["items"][0]["id"]
        spotifyObject.playlist_add_items(playlist_id=playlist, items=songs)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
