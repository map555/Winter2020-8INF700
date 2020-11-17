import keyring
##Fonctions to get authentification tokens.


##Function to get user's Spotify username for connection.
#
# arg: none
#
# return: keyring.get_password("spotifyuser","user"): user's Spotify username..
def getSpotifyUsername():
    return(keyring.get_password("spotifyuser","user"))


##Function to get user's Spotify password for connection.
#
# arg: none
#
# return: keyring.get_password("spotipass","pass"): user's Spotify password.
def getSpotifyPassword():
    return(keyring.get_password("spotipass","pass"))


##Function to get user's Dark Weather api key for connection.
#
# arg: none
#
# return: keyring.get_password("darkskyapikey", "apikey"): user's Dark Weather's api key.
def getDarkSkyWeatherApiKey():
    mdp='68f2f11d08c1538bef173b8c168f1bd9'
    return (keyring.get_password("darkskyapikey", "apikey"))


##Function to get user's Messenger  username for connection.
#
# arg: none
#
# return: keyring.get_password("messengeruser","user"): user's Messenger/Facebook username.
def getMessengerUserName():
    return(keyring.get_password("messengeruser","user"))


##Function to get user's Messenger password for connection.
#
# arg: none
#
# return: keyring.get_password("messengerpass","pass"): user's Messenger/Facebook password.
def getMessengerPassword():
    return(keyring.get_password("messengerpass","pass"))


