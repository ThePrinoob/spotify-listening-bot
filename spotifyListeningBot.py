# Imports
import sys
import os
import time
import json
import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import webbrowser
import random
import re

username = None
client_id = None
client_secret = None
redirect_uri = None
device_id = None
devices = None
device = 0
waitTime = 300
waitTimePlaying = 5
_auth_finder = re.compile("code=(.*?)$", re.MULTILINE)
cacheCredentials = ".cache/.cachedCredentials"

class Main:
    def __init__(self):
        self.spo = oauth2.SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            cache_path=".cache/.cachedToken-{}".format(username))
        self.sp = spotipy.Spotify(auth=self.get_token())
        
    def refresh_token(self):
        cached_token = self.spo.get_cached_token()
        refreshed_token = cached_token['refresh_token']
        new_token = self.spo.refresh_access_token(refreshed_token)
        self.sp = spotipy.Spotify(auth=new_token['access_token'])
        return new_token

    def get_token(self):
        token_info = self.spo.get_cached_token()
        if token_info:
            access_token = token_info['access_token']
            return access_token
        else:
            auth = self.spo.get_authorize_url()
            print(auth)
            webbrowser.open_new_tab(auth)
            auth_url = input(
                'Click the link above and copy and paste the url here: ')
            _re_auth = re.findall(_auth_finder, auth_url)
            access_token = self.spo.get_access_token(_re_auth[0])
            return access_token

    def getDevice(self):
        self.devices = self.sp.devices()
        if self.devices == None:
            print("Spotify couldn't find any devices :(\nExiting now...")
            sys.exit()
        print("-------------------------\n")
        print("available Devices:")
        for i in range(len(self.devices.get("devices"))):
            print("Nr: " + str(i))
            print("Name: " + self.devices.get("devices")[i].get("name"))
            print("ID: " + self.devices.get("devices")[i].get("id") + "\n")
        print("-------------------------\n")
        self.device = input(
            "On which Device would you like to stream, when nothing is playing?\nNr: ")
        if self.device.isdigit() == False:
            print("Thats not a number! Try again\n")
            main.getDevice()
        elif int(self.device) >= len(self.devices.get("devices")):
            print("not a valid Option! Try again\n")
            main.getDevice()
        else:
            self.device_id = self.devices.get("devices")[int(self.device)].get("id")
            if "--silent" in sys.argv or "-s" in sys.argv:
                print("aight im silent now but still doing my thing")
                sys.stdout = open(os.devnull, 'w')

    def checkPlayback(self, timeChecking = 0):
        print("\ngetting current Playback...")
        pb = self.sp.current_playback()  # info to the current playback
        
        if timeChecking == 0:
            print("checking if Spotify is playing...")
            if pb == None or pb["is_playing"] == False:
                print("Not Playing...\nChecking Every " + str(waitTimePlaying) + " Seconds for " + str(waitTime) + " Seconds if its still not playing")
                timeChecking = waitTimePlaying
                print("\n-------------------------")
                time.sleep(waitTimePlaying)
                main.checkPlayback(timeChecking)
            else:
                print("Already Playing...")
            print("checking again in " + str(waitTime) + " seconds")
            print("\n-------------------------")

        elif timeChecking <= waitTime:
            print("checking if Spotify is still not playing...")
            if pb == None or pb["is_playing"] == False:
                print("Not Playing... Checking again in " + str(waitTimePlaying) +  " seconds")
                timeChecking += waitTimePlaying
                print("\n-------------------------")
                time.sleep(waitTimePlaying)
                main.checkPlayback(timeChecking)
            else:
                print("Plays again! Going back to normal Rythmus.")
                
        else:
            print("didn't play for " + str(waitTime) + " seconds...")
            tracks = []
            print("getting user saved tracks...")
            savedTracks = self.sp.current_user_saved_tracks(50)  # saved tracks
            for tracks_uri in savedTracks.get("items"):
                tracks.append(tracks_uri.get("track").get("uri"))
            # Randomizes the Tracks
            print("randomizing Tracks...")
            random.shuffle(tracks)
            # starts the Playback on raspbify
            print("starting Playback on " + str(self.devices.get("devices")[int(self.device)].get("name")))
            self.sp.start_playback(
                self.device_id, None, tracks)
            print("\n-------------------------\n")
        


print(r"""
                           __  _ ____            ___      __             _                   __          __
         _________  ____  / /_(_) __/_  __      / (_)____/ /____  ____  (_)___  ____ _      / /_  ____  / /_
        / ___/ __ \/ __ \/ __/ / /_/ / / /_____/ / / ___/ __/ _ \/ __ \/ / __ \/ __ `/_____/ __ \/ __ \/ __/
        (__  ) /_/ / /_/ / /_/ / __/ /_/ /_____/ / (__  ) /_/  __/ / / / / / / / /_/ /_____/ /_/ / /_/ / /_
        /____/ .___/\____/\__/_/_/  \__, /     /_/_/____/\__/\___/_/ /_/_/_/ /_/\__, /     /_.___/\____/\__/
            /_/                    /____/                                      /____/
""")

def getCredentials():
    global client_id
    global client_secret
    global redirect_uri

    if "SPOTIPY_CLIENT_ID" in os.environ:
        print("Got your Client_ID from Environment Variables")
        
        while True:
            environ = input("Do you want to use these Infos? (yes / no) ")
            if environ.lower() in ('yes', 'ye', 'y', 'j'):
                client_id = os.environ.get('SPOTIPY_CLIENT_ID')
                print("using these Values!\n")
                break
            elif environ.lower() in ('no', 'na', 'n'):
                client_id = input("Not Using those Values... Specify SPOTIPY_CLIENT_ID now: ")
                print("using user specific values!\n")
                break
            else:
                print("Not an appropriate answer. Try Again\n")
    else:
        client_id = input("Couldn't find SPOTIPY_CLIENT_ID in Environment Variables... Specify SPOTIPY_CLIENT_ID now: ")

    if "SPOTIPY_CLIENT_SECRET" in os.environ:
        print("Got your SPOTIPY_CLIENT_SECRET from Environment Variables")

        while True:
            environ = input("Do you want to use these Infos? (yes / no) ")
            if environ.lower() in ('yes', 'ye', 'y', 'j'):
                client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
                print("using these Values!\n")
                break
            elif environ.lower() in ('no', 'na', 'n'):
                client_secret = input("Not Using those Values... Specify SPOTIPY_CLIENT_SECRET now: ")
                print("using user specific values!\n")
                break
            else:
                print("Not an appropriate answer. Try Again\n")
    else:
        client_secret = input("Couldn't find SPOTIPY_CLIENT_SECRET in Environment Variables... Specify SPOTIPY_CLIENT_SECRET now: ")

    if "SPOTIPY_REDIRECT_URI" in os.environ:
        print("Got your SPOTIPY_REDIRECT_URI from Environment Variables")
        while True:
            environ = input("Do you want to use these Infos? (yes / no) ")
            if environ.lower() in ('yes', 'ye', 'y', 'j'):
                redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
                print("using these Values!\n")
                break
            elif environ.lower() in ('no', 'na', 'n'):
                redirect_uri = input("Not Using those Values... Specify SPOTIPY_REDIRECT_URI now: ")
                print("using user specific values!\n")
                break
            else:
                print("Not an appropriate answer. Try Again\n")
    else:
        redirect_uri = input("Couldn't find SPOTIPY_REDIRECT_URI in Environment Variables... Specify SPOTIPY_REDIRECT_URI now: ")

    if "-c" in sys.argv or "--cache" in sys.argv:
        print("saving Credentials to ./cache ...")
        credentials = {
            "username": username,
            "client_id": client_id, 
            "client_secret": client_secret,
            "redirect_uri": redirect_uri
        }
        f = open(cacheCredentials, 'w+')
        f.write(json.dumps(credentials))
        f.close()

try:
    if "-c" in sys.argv or "--cache" in sys.argv:
        print("Cache Mode activated")
        try:
            os.mkdir(".cache")
            print("Cache Folder Created") 
        except FileExistsError:
            print("Found cache!")
        f = open(cacheCredentials)
        accessTokenString = f.read()
        f.close()
        accessToken = json.loads(accessTokenString)
        username = accessToken.get("username")
        print("Welcome back ThePripanda\n")
        client_id = accessToken.get("client_id")
        client_secret = accessToken.get("client_secret")
        redirect_uri = accessToken.get("redirect_uri")
    else:
        username = input("Type your Spotify Username: ")
        getCredentials()

    parameter_dict = {}
    for user_input in sys.argv[1:]:
        if "=" not in user_input:
            continue
        varname = user_input.split("=")[0]
        varvalue = user_input.split("=")[1]
        parameter_dict[varname] = varvalue
    if "waitTime" in parameter_dict:
        if parameter_dict["waitTime"].isdigit() == False:
            print("Thats not a number! Using Basic Value for waitTime")
        else:
            waitTime = int(parameter_dict["waitTime"])
    if "waitTimePlaying" in parameter_dict:
        if parameter_dict["waitTimePlaying"].isdigit() == False:
            print("Thats not a number! Using Basic Value for waitTimePlaying")
        else:
            waitTimePlaying = int(parameter_dict["waitTimePlaying"])
except IOError:
    username = input("Type your Spotify Username: ")
    getCredentials()

main = Main()

def init():    
    try:
        main.refresh_token()
        main.getDevice()
    except OSError:
        print("No Internet Connection!")
        time.sleep(5)
        init()
    except KeyboardInterrupt:
        print('\nManual break by user! exiting')
        sys.exit()
init()

try:
    while True:
        try:
            main.checkPlayback()
            time.sleep(waitTime)  # 300 for 5 minutes
        except spotipy.client.SpotifyException:
            print("redefining Token")
            main.refresh_token()
        except (OSError, ConnectionError): 
            print("No Internet Connection!")
            time.sleep(5)
            pass
except KeyboardInterrupt:
    sys.stdout = sys.__stdout__
    print('Manual break by user! exiting')
