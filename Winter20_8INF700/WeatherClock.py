import time
from darksky import forecast
from getAuthTokens import getDarkSkyWeatherApiKey
from Location import Location


class Weather():
    def __init__(self):

        self.__positionLongitude=-71.0657272
        self.__positionLatitude=48.4167519
        location=Location()
        self.__weather=forecast(getDarkSkyWeatherApiKey(), location.getLatitude(), location.getLongitude(), units='si',lang="en") #Data units are those from the  International System of Units (ISU).
        self.__actualWeatherData=self.__weather['currently'] #Fetch a dictionnary containning the actual wheater condition depending of the geographical position
        self.__dailyForecast=self.__weather['daily']
        self.setDailyForecastData()


    ##Public method to refresh the weather dictionnaries.
    #A weather object has two dictionnaries: a dictionnary containing the actual weather's data and another one containing the daily forecast's data.
    #The daily forecast data are used to have the daily maximal and the minimal feeled temperature.
    #
    #arg: none
    #
    #return: none
    def Update(self):

        ##ctualise forecast object's data with the canadian units.
        # The canadian units are those in the Internationnal Units System but wndSpeed and windGust are expressed in kilometer by hour.
        #
        #source: https://pypi.org/project/darkskylib/
        self.__weather.refresh(units="ca", lang='fr')
        self.__actualWeatherData=self.__weather['currently']
        self.setDailyForecastData()


    ##Public method to affect the dailyforecast's dictionnary into the dailyForecast dictionnary by extracting it from the weather forecast object.
    #
    #arg: none
    #
    #return: none
    def setDailyForecastData(self):
        self.__dailyForecast = self.__weather['daily']
        self.__dailyForecast = self.__dailyForecast.get('data')
        self.__dailyForecast = self.__dailyForecast[0]


    ##Public method used to return the actual temp into the interface.
    #
    #arg: none
    #
    #return: actualWeatherData.get('temperature'): Actual temperature.
    def getTemp(self):
        return (self.__actualWeatherData.get('temperature'))


    ##Public method used to return the actual feeled temp into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('apparentTemperature'): Actual feeled temperature.
    def getFeeledTemp(self):
        return (self.__actualWeatherData.get('apparentTemperature'))


    ##Public method used to return the actual weather description into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('summary'): Actual weather's description.
    def getWeatherDesc(self):
        return (self.__actualWeatherData.get('summary'))


    ##Public method used to return the actual probability of precipitation into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('precipProbability'): Actual precipitation probability.
    def getPrecipitationProb(self):
        return(self.__actualWeatherData.get('precipProbability'))


    ##Public method used to return the actual precipitation intensity into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('precipIntensity'): Actual precipitation intensity.
    def getPrecipitationIntensity(self):
        #round probability ?
        if((self.__actualWeatherData.get('precipProbability') >= 10)):
            return (self.__actualWeatherData.get('precipIntensity'))
        else:
            return(0)


    ##Public method used to return the actual precipitation type into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('precipitationType'): Actual precipitation type.
    def getPrecipitationType(self):
        precipitationType=self.__actualWeatherData.get('precipType')
        precipitationProbability=self.__actualWeatherData.get('precipProbability')
        if(precipitationProbability<=0.10):
            return("none")
        else:
            return(precipitationType)


    ##Public method used to return the actual wind speed into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('windSpeed'): Actual wind speed.
    def getWindSpeed(self):
        return (self.__actualWeatherData.get('windSpeed'))


    ##Public method used to return the actual wind direction into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('windBearing'): Actual wind direction.
    def getWindDir(self):
        return (self.__actualWeatherData.get('windBearing'))


    ##Public method used to return the daily maximal feeled temperature into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('appparentTemperatureMax'): Daily maximal feeled temperature.
    def getDailyMaxFeeledTemp(self):
        return(self.__dailyForecast.get('apparentTemperatureMax'))


    ##Public method used to return the daily minimal feeled temperature into the interface.
    #
    # arg: none
    #
    # return: actualWeatherData.get('apparentTemperatureMin'): Daily minimal feeled temperature.
    def getDailyMinFeeledTemp(self):
        return (self.__dailyForecast.get('apparentTemperatureMin'))






##Function to return the time into the interface.
#
# arg: none
#
# return: hour.
def Hour():
    hour = time.strftime("%H : %M : %S")
    return hour



##Function to return the date into the interface.
#
# arg: none
#
# return: date.
def Date():
    #weekday - day - month - year
    date=time.strftime("%A %d %B %Y")
    return date




