# Spotify-listening-bot
A Python-written bot that can generate automatic listens to your last 50 added Songs.

## Usage
* First, clone this repo on your local machine with\
```git clone https://github.com/ThePrinoob/Spotipy-listening-bot```\
or Download the ZIP from here.

* Next you will need the spotipy Library, install it with this command:\
```pip install spotipy```

* Done! You can now simply run the bot with\
```python spotifyListeningBot.py [options]```

To get started create an app on https://developers.spotify.com/.
Add your new ID and SECRET to your environment:

### Linux
```export SPOTIPY_CLIENT_ID='your-spotify-client-id'```

```export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'```

```export SPOTIPY_REDIRECT_URI='your-spotify-redirect-uri'```

or run the Script and it will automatically ask for your Credentials

### Windows
```setx SPOTIPY_CLIENT_ID your-spotify-client-id```

```setx SPOTIPY_CLIENT_SECRET your-spotify-client-secret```

```setx SPOTIPY_REDIRECT_URI your-spotify-redirect-uri```

or run the Script and it will automatically ask for your Credentials

## Run options
These are optionals parameters, they are not necessary to run the program.

* ```-s``` or ```--silent``` puts the Script in silent mode, that means no Output :(
* ```-c``` or ```--cache``` puts the Script in cache mode, that means your Credential will be saved to the .cache Folder in the current Folder.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/ThePrinoob/spotify-listening-bot/issues). Or just send me a pull request.