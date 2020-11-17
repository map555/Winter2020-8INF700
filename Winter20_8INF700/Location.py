import re
import json
from urllib.request import urlopen

## Simple class to get the coordinates of the user's city
class Location():
    def __init__(self):#Inspired by this thread on stackoverflow:
        #https://stackoverflow.com/questions/24678308/how-to-find-location-with-ip-address-in-python
        super().__init__()
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        self.__ipData = json.load(response)
        self.__location=self.__ipData['loc']#get the lattitude and the longitude into a single string
        self.__comaPosition=self.__location.find(',') # the coma position who separates the longitude and lattitude in the self.__location string

    ##Publig method to return the latitude the user's city
    # Extract the latitude from the self.__location string
    #
    # arg: none
    #
    # return: the latitude of the user's city
    def getLatitude(self):
        latitude=self.__location[0:self.__comaPosition]#get the characters from the beginning of the string to coma separator
        return(latitude)

    ##Publig method to return the longitude the user's city
    # Extract the longitude from the self.__location string
    #
    # arg: none
    #
    # return: the longitude of the user's city
    def getLongitude(self):
        #get the characters from the character after the coma to the end of the string
        longitude=self.__location[(self.__comaPosition+1):(len(self.__location)-1)]
        return(longitude)


