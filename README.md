# **Spotify_Project**

A simple project that takes your liked videos on YouTube, creates a Spotify playlist, and adds any songs in those liked videos to the Spotify playlist.

## **Before you run it**
- [Install all Dependencies](#install-all-dependencies)
- [Add information to the secrets.py file](#add-information-to-the-secretspy-file)
- [Enable Youtube Oauth authentication](#enable-youtube-oauth-authentication)

### **Install all dependencies**
`pip install -r requirements.txt`

### **Add information to the secrets.py file**
To get your Spotify User ID, Log into Spotify and then go to [Account Overview](https://www.spotify.com/us/account/overview/). Your ID is displayed as "Username" in "Account Overview".
An Oauth token for spotify can be copied from [The Spotify 'Create a Playlist' documentation section](https://developer.spotify.com/console/post-playlists/) by clicking on "Get Token". Note, the token expires rather quickly, so if you see a `KeyError` it is very likely because the Spotify token has expired.

### **Enable Youtube Oauth authentication**
Follow the guide at ["YouTube Data API Overview"](https://developers.google.com/youtube/v3/getting-started/). Check out this [Stackoverflow question](https://stackoverflow.com/questions/11485271/google-oauth-2-authorization-error-redirect-uri-mismatch/) or this [Client Secrets documentation](https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md/) for help.

## To Do
- Implement Error Handling
- Check if the playlist exists before creating one
- Add the option for the user to give a name and description to the Spotify playlist that will be created
