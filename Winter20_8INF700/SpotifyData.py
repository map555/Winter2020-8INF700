import json


import requests
import spotify_token as st
from getAuthTokens import getSpotifyUsername
from getAuthTokens import getSpotifyPassword


## Spotify's data class for the Spotify functionnality
class Spotify():

    def __init__(self):
        super().__init__()

        self.__songTitle= ""
        self.__artist= ""
        self.__albumTitle= ""
        self.__albumCoverUrl= ""

        #Dictionnary to store the urls used for http requests.
        self.__requestUrlDict={'actually listened':"https://api.spotify.com/v1/me/player/currently-playing",
                               'most recently listened':"https://api.spotify.com/v1/me/player/recently-played?limit=1"}
        self.__songDict={}
        self.__tokenAutorisationApiSpotify=''
        self.__requestStatus=0
        self.__username = getSpotifyUsername()
        self.__password = getSpotifyPassword()
        self.__setSpotifyAuthToken(self.__username, self.__password)
        self.__setJSONData()
        self.setAlbum()
        self.setArtists()
        self.setSongTitle()
        self.setAlbumCover()





    ##Private method to initiate an authorisation token for the Spotify's web player API to the private attribute spotifyApiAuthorisationToken.
    #
    #arg:
    #&nbsp;&nbsp;&nbsp;&nbsp;username: the Spotify's username of the user
    #\tpassword: the Spotify's password of the user
    #
    #return:
    #    none
    def __setSpotifyAuthToken(self, username, password):
        token=[]
        token = st.start_session(username=username, password=password)
        self.__tokenAutorisationApiSpotify=token[0]



    ##Public method who doesn't need the username and the password as parameters. The method sets a new authorisation token by calling the private method setSpotifyAuthToken.
    # Each token is valid for a 60 minutes period.
    #
    #arg:
    #    none
    #
    #return:
    #    none
    def setAuthToken(self):
        self.__setSpotifyAuthToken(username=self.__username, password=self.__password)



    ##To set the song's information dictionnary into the private attribute songDict.
    #
    #arg:
    #    none
    #
    #return:
    #    none
    def __setJSONData(self):
        self.__songDict=self.__getJSONData()


    ##Private method to prepare the request's header.
    #
    #:arg
    #    none
    #
    #:return
    #    header: The header for the HTTP request.

    def __getAnHeader(self):
        """
        Spotify API's tokens always start by \"Bearer \", but the module used for generating tokens only return the
        variable part of a token. The concatenation of the constant part of the token is necessary to generate the header
        correctly.
        """
        autorisation = 'Bearer ' + str(self.__tokenAutorisationApiSpotify)
        header = {'Authorization': autorisation}
        return header


    ##This function does an HTTP GET request to the Spotify's API to get the JSON dictionnary
    #of actually listened song or the last listened song if nothing is playing.
    #
    #arg:
    #    none
    #
    #return:
    #    dict: The JSON dictionnary containing the sons's info.

    def __getJSONData(self):
        #Try to fetch the actually listened song first.
        httpGetRequest = requests.get(url=self.__requestUrlDict.get("actually listened"),headers=self.__getAnHeader())
        self.__requestStatus = httpGetRequest.status_code

        """
        If the user is actually listening to Spotify, the request will return code 200. Else, if
        the user isn't listening to Spotify, the request will return code 204. If status code is 204,
        the request returns an empty dictionnary and the fonction will request the last listened song.
        """

        if (self.__requestStatus == 200):
            dict = httpGetRequest.json()
            dict = json.loads(json.dumps(dict))
            dict = dict.get('item')

        elif (self.__requestStatus == 204):
            httpGetRequest = requests.get(url=self.__requestUrlDict.get('most recently listened'),headers=self.__getAnHeader())
            dict = httpGetRequest.json()
            dict = json.loads(json.dumps(dict))
            dict = dict.get('items')

        return dict



    ##Fetch the artist's or the artists' name from the song's dictionnary
    #
    #arg:
    #
    #return:
    #    artistsName: The name of the artist(s) concatanated into a string (ex: "artistName1, artistName2, artistName3")
    #            example: \"artistName1, artistName2, artistName3\"

    def __FetchArtists(self):
        x = 0  # To count the iteration number of the loop  and check if it's is last iteration
        artistsName = ''

        #Status code is used there to determine how to get the name of the artists depending wich request was used to get the dictionnary.
        """
        For status 204, the request returns a list of dictionnaries because this request can return more than one song's
        info dictionnary. In this program's context, the list contain only one dictionnary.
        """
        if (self.__requestStatus == 204):
            temporaryDictionnary = self.__songDict[0]
            temporaryDictionnary = temporaryDictionnary.get('track')
            artists=temporaryDictionnary.get('artists')

        elif(self.__requestStatus==200):
            artists = self.__songDict.get('artists')

        #Looping into the artist list of the dictionnary to concatanate all the artists' name into the string artistsName
        for artist in artists:
            artistsName += artist.get('name')

            #Checking if it's the last artist of the list. If it is not, an ", " is added before the next name.
            if (x != (len(artists) - 1)):
                artistsName = artistsName + ", "
            x += 1
        return(artistsName)


    ##Public method to affect the artists' name of the song into the artist attribute of the class.
    #
    #arg:
    #    none
    #
    #return:
    #    none

    def setArtists(self):
        self.__artist=self.__FetchArtists()



    ##Private method to fetch the title of the album from the song dictionnary.
    #
    #arg:
    #    none
    #
    #return:
    #    albumTitle: The title of the album.

    def __FetchAlbum(self):


        if(self.__requestStatus==204):
            temporaryDictionnary=self.__songDict[0] #The first song of the list of dictionnaries
            temporaryDictionnary=temporaryDictionnary.get('track')
            temporaryDictionnary=temporaryDictionnary.get('album')
            temporaryDictionnary=temporaryDictionnary.get('name')
            albumTitle=temporaryDictionnary
        elif(self.__requestStatus==200):
            album = self.__songDict.get('album')
            albumTitle=album.get('name')
        return(albumTitle)



    ##Public method to return the album's title for setting the interface's content.
    #
    #arg:
    #    none
    #
    #return:
    #    albumTitle: The title of the album.

    def getAlbum(self):
        return self.__albumTitle



    #Public method to return the name of the artist(s) for setting the interface's content.
    #
    #arg:
    #    none
    #
    #return:
    #    artist: The name of the artist(s).

    def getArtist(self):
        return self.__artist


    #Public method to return the song's title for setting the interface's content
    #
    #arg:
    #    none
    #
    #return:
    #    songTitle: The title of the song.

    def getSongTitle(self):
        return self.__songTitle



    #Public method to return the album cover picture's URL for loading the picture in the the interface.
    #
    #arg:
    #    none
    #
    #return:
    #    albumCoverUrl: The URL of the album cover picture's.

    def getAlbumCoverURL(self):
        return self.__albumCoverUrl


    ##Public method to affect the album's title into the albumTitle attribute of the class.
    #
    #arg:
    #    none
    #
    #return:
    #    none

    def setAlbum(self):
        self.__albumTitle=self.__FetchAlbum()



    ##Private method to fetch the song's title from the song dictionnary.
    #
    #arg:
    #    none
    #
    #return:
    #    songTitle: The title of the song.

    def __FetchSongTitle(self):
        if (self.__requestStatus == 204):
            temporaryDictionnary = self.__songDict[0]
            temporaryDictionnary = temporaryDictionnary.get('track')
            temporaryDictionnary = temporaryDictionnary.get('name')
            titreChanson = temporaryDictionnary
        elif(self.__requestStatus==200):
            titreChanson=self.__songDict.get('name')
        return(titreChanson)



    ##Public method to affect the song's title into the songTitle attribute of the class.
    #
    #arg:
    #    none
    #
    #return:
    #    none
    #
    def setSongTitle(self):
        self.__songTitle=self.__FetchSongTitle()



    ##Private method to fetch the album cover picture's URL from the song dictionnary.
    #
    #arg:
    #    none
    #
    #return:
    #    image[1].get('url'): The album cover picture's URL with the following dimmensions:300x300.

    def __FetchAlbumCoverURL(self):
        #    Spotify uses a list for the url of the image. They are three sizes of the image in the list: 640x640, 300x300 and 64x64.
        if (self.__requestStatus == 204):
            temporaryDictionnary = self.__songDict[0]
            temporaryDictionnary = temporaryDictionnary.get('track')
            temporaryDictionnary = temporaryDictionnary.get('album')
        elif(self.__requestStatus==200):
            temporaryDictionnary=self.__songDict.get('album')
        image=temporaryDictionnary.get('images')
        return(image[1].get('url')) #Get the 300x300 image's URL


    ##Public method to affect the album cover picture's url into the albumCoverUrl attribute of the class.
    #
    #arg:
    #    none
    #
    #return:
    #    none

    def setAlbumCover(self):
        self.__albumCoverUrl=self.__FetchAlbumCoverURL()



    ##Public method to check if the song's informations change before afecting them into the class' attributes.
    #
    #Maybe removing it (if I have the time) and emplement directly something into the interface for checking
    #if the URL change to avoid the Spotify functionnality's interface if the song doesn't changed yet.
    #
    #arg:
    #    none
    #
    #return:
    #    none

    def CheckSongInfo(self):

        self.__setJSONData()
        title=self.__FetchSongTitle()
        artists=self.__FetchArtists()
        album=self.__FetchAlbum()
        titleLabel=self.__songTitle
        albumLabel=self.__albumTitle
        artistsLabel=self.__artist

        if (title != titleLabel) or (album != albumLabel)or(artists != artistsLabel):
            self.setAlbumCover()
            self.setSongTitle()
            self.setArtists()
            self.setAlbum()

