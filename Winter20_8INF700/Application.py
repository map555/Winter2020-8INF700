import csv
import datetime
import os
import sys
from threading import Thread
import time
import urllib.request
from WeatherClock import Weather
from SpotifyData import  Spotify
from MessengerNotificationsGUI import MessengerNotifGui
from Sounds import PlayAlarmBell
from EditScreenBackLightConfigFile import setBackLight
import RestartRaspotify
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QScrollArea,QListWidgetItem,QListWidget, QSizePolicy, QPushButton, QFrame, QDialog, QVBoxLayout, QLabel, \
    QStackedWidget, \
    QHBoxLayout, QWidget, QCheckBox, QSpinBox




##The main class of the program
# Contains the graphical user interface and the alarm clock fonctionnality
class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.__messenger=MessengerNotifGui()
        self.__timeUntilNextAlarmCheck=0
        self.__alarmToday=False
        self.__fileName = "alarmSettings.csv"
        self.__activeDaysList = []
        self.__alarmActivationHoursList = []
        self.__alarmActivationMinuteList = []
        self.mainLayout = QHBoxLayout()
        self.buttonLayout = QVBoxLayout()
        self.__changingContentWidget = QStackedWidget()
        self.spotifyButton = QPushButton()
        self.weatherAndHourButton = QPushButton()
        self.__alarmButton=QPushButton()
        self.__separatorLine=QFrame()

        #For hour and Wheater
        self.weatherHourContent = QVBoxLayout()
        self.dateAndHourLayout=QHBoxLayout()
        self.__hourLayout=QHBoxLayout()
        self.__weatherLayout=QVBoxLayout()
        self.__weatherDescriptionLayout=QHBoxLayout()
        self.__weatherDataLayout=QHBoxLayout()
        self.__temperatureDataLayout=QVBoxLayout()
        self.__precipitationAndWindDataLayout=QVBoxLayout()
        self.__windDataLayout=QVBoxLayout()
        self.__precipitationDataLayout=QVBoxLayout()
        self.__weatherClockWidget=QWidget()
        self.__weatherCondition=Weather()
        self.hourLabel=QLabel()
        self.dateLabel=QLabel()
        self.actualTemperatureLabel=QLabel()
        self.actualFeeledTemperatureLabel=QLabel()
        self.weatherDescriptionLabel=QLabel()
        self.actualPrecipationProbabilityLabel=QLabel()
        self.actualPrecipitationIntensityLabel=QLabel()
        self.actualPrecipitationTypeLabel=QLabel()
        self.actualWindSpeedLabel=QLabel()
        self.actualWindDirectionLabel=QLabel()
        self.dailyMaxTempLabel=QLabel()
        self.dailyMinTempLabel=QLabel()

        #Pour spotify
        self.spotify=Spotify()
        self. spotifyLayoutContent=QHBoxLayout()
        self.songInfoLayout=QVBoxLayout()
        self.__spotifyWidget=QWidget()
        self.songTitleLabel=QLabel()
        self.artistsLabel=QLabel()
        self.albumTitleLabel=QLabel()
        self.albumCoverLabel=QLabel()
        self.albumCover=QtGui.QImage()


        #For the Alarm settings interface:
        self.__alarmSettingsLayout=QVBoxLayout()
        self.__dailySettingsLayout=QHBoxLayout()
        self.__mondaySettingsLayout=QVBoxLayout()
        self.__tuesdaySettingsLayout=QVBoxLayout()
        self.__wednesdaySettingsLayout=QVBoxLayout()
        self.__thursdaySettingsLayout=QVBoxLayout()
        self.__fridaySettingsLayout=QVBoxLayout()
        self.__saturdaySettingsLayout=QVBoxLayout()
        self.__sundaySettingsLayout=QVBoxLayout()

        self.__mondayHourSpinbox:QSpinBox=QSpinBox()
        self.__tuesdayHourSpinbox:QSpinBox=QSpinBox()
        self.__wednesdayHourSpinbox:QSpinBox=QSpinBox()
        self.__thursdayHourSpinbox: QSpinBox = QSpinBox()
        self.__fridayHourSpinbox: QSpinBox = QSpinBox()
        self.__saturdayHourSpinbox: QSpinBox = QSpinBox()
        self.__sundayHourSpinbox: QSpinBox = QSpinBox()


        self.__mondayMinuteSpinbox:QSpinBox=QSpinBox()
        self.__tuesdayMinuteSpinbox:QSpinBox=QSpinBox()
        self.__wednesdayMinuteSpinbox:QSpinBox=QSpinBox()
        self.__thursdayMinuteSpinbox: QSpinBox = QSpinBox()
        self.__fridayMinuteSpinbox: QSpinBox = QSpinBox()
        self.__saturdayMinuteSpinbox: QSpinBox = QSpinBox()
        self.__sundayMinuteSpinbox: QSpinBox = QSpinBox()

        self.__weekAlarmCheckBox=QCheckBox("Activer alarme")
        self.__mondayAlarmCheckBox=QCheckBox("Lundi")
        self.__tuesdayAlarmCheckBox = QCheckBox("Mardi")
        self.__wednesdayAlarmCheckBox = QCheckBox("Mercredi")
        self.__thursdayAlarmCheckBox = QCheckBox("Jeudi")
        self.__fridayAlarmCheckBox = QCheckBox("Vendredi")
        self.__saturdayAlarmCheckBox = QCheckBox("Samedi")
        self.__sundayAlarmCheckBox = QCheckBox("Dimanche")

        self.__weekWidget=QWidget()
        self.__mondayWidget=QWidget()
        self.__tuesdayWidget=QWidget()
        self.__wednesdayWidget=QWidget()
        self.__thursdayWidget=QWidget()
        self.__fridayWidget=QWidget()
        self.__saturdayWidget=QWidget()
        self.__sundayWidget=QWidget()
        self.__alarmWidget=QWidget()


        self.__confirmButton=QPushButton("Apply change")
        self.__confirmButton.clicked.connect(self.ApplySettingsChange)

        #Other variables who don't need to be attrbutes of the class
        hourSpinBoxSuffix= " h"
        minuteSpinBoxSuffix= " min"


        self.Interface()

        self.__changingContentWidget.setCurrentIndex(0)
        self.__initiateHourAndWeatherUpdate()
        self.__initiateMessengerTimers()
        self.__InitiateBacklight()

        self.__FillLists()
        self.__ImportAlarmSettingsToGUI()
        self.__setAlarmTimers()
        self.setGeometry(0,0,400,240)
        self.__initialiseRaspotify()

        self.showFullScreen()#fullscreen
        self.setCursor(Qt.BlankCursor)#invisible mouse

    ##Public method to initiate the graphical user interface. The graphical user containt two main elements:
    # a a side bar with buttons to navigate between the interfaces of the fonctionnalities of the application and
    # a QStackedWidget. A QStackedWidget object allow to store multiple widgets and with an index system, the
    # the programmer can select wich widget to show. The user interface use a QStackStackedWidget to select wich
    # functionnality's interface to show depending on wich button the user touches.
    #
    # arg: none
    #
    # return: none
    def Interface(self):

        self.spotifyButton.setIcon(QtGui.QIcon("spotify-logo.png"))
        self.spotifyButton.setIconSize(QSize(50, 50))
        self.spotifyButton.setFlat(True)
        self.weatherAndHourButton.setIcon(QtGui.QIcon("clock-logo"))
        self.weatherAndHourButton.setIconSize(QSize(50, 50))
        self.weatherAndHourButton.setFlat(True)
        self.__alarmButton.setIcon((QtGui.QIcon("alarm-clock-icon.png")))
        self.__alarmButton.setIconSize(QSize(50,50))
        self.__alarmButton.setFlat(True)
        self.__messengerNotificationButton=QPushButton()
        self.__messengerNotificationButton.setIcon((QtGui.QIcon("messenger-logo.png")))
        self.__messengerNotificationButton.setIconSize(QSize(50,50))
        self.__messengerNotificationButton.setFlat(True)
        self.spotifyButton.page=1
        self.weatherAndHourButton.page=0
        self.__alarmButton.page=2
        self.__messengerNotificationButton.page=3
        self.weatherAndHourButton.clicked.connect(lambda :self.__ButtonsAction(self.weatherAndHourButton.page))
        self.spotifyButton.clicked.connect(lambda :self.__ButtonsAction(self.spotifyButton.page))
        self.__alarmButton.clicked.connect(lambda :self.__ButtonsAction(self.__alarmButton.page))
        self.__messengerNotificationButton.clicked.connect(lambda :self.__ButtonsAction(self.__messengerNotificationButton.page))

        self.buttonLayout.addWidget(self.weatherAndHourButton)
        self.buttonLayout.addWidget(self.spotifyButton)
        self.buttonLayout.addWidget(self.__alarmButton)
        self.buttonLayout.addWidget(self.__messengerNotificationButton)
        self.__buttonsWidget=QWidget()
        self.__buttonsWidget.setLayout(self.buttonLayout)



        #Hour and weather
        self.dateWeatherLayout=QVBoxLayout()
        self.dateWeatherLayout.addWidget(self.dateLabel)
        self.dateWeatherLayout.addWidget(self.weatherDescriptionLabel)
        self.__hourLayout=QHBoxLayout()
        self.__hourLayout.addWidget(self.hourLabel)
        self.__weatherDateHourLayout=QHBoxLayout()
        self.__weatherDateHourLayout.addLayout(self.dateWeatherLayout)
        self.__weatherDateHourLayout.addLayout(self.__hourLayout)
        self.hourLabel.setStyleSheet("font:25pt")




        self.weatherHourContent.addLayout(self.__weatherDateHourLayout)

        self.__temperatureSectionLabel=QLabel("TEMPÉRATURE")
        self.__feeledTemperatureSectionLabel=QLabel("RESSENTIE")
        self.__temperatureSectionLabel.setContentsMargins(0, 0, 0, 0)
        self.actualTemperatureLabel.setContentsMargins(0, 0, 0, 0)
        self.__feeledTemperatureSectionLabel.setContentsMargins(0, 0, 0, 0)
        self.actualFeeledTemperatureLabel.setContentsMargins(0, 0, 0, 0)
        self.dailyMaxTempLabel.setContentsMargins(0, 0, 0, 0)
        self.dailyMinTempLabel.setContentsMargins(0, 0, 0, 0)



        self.__temperatureDataLayout.addWidget(self.__temperatureSectionLabel)
        self.__temperatureDataLayout.addWidget(self.actualTemperatureLabel)
        self.__temperatureDataLayout.addWidget(self.__feeledTemperatureSectionLabel)
        self.__temperatureDataLayout.addWidget(self.actualFeeledTemperatureLabel)
        self.__temperatureDataLayout.addWidget(self.dailyMaxTempLabel)
        self.__temperatureDataLayout.addWidget(self.dailyMinTempLabel)
        self.__temperatureDataLayout.setContentsMargins(0,0,0,0)
        self.__temperatureDataLayout.setAlignment(Qt.AlignLeft)


        self.__weatherDataLayout.addLayout(self.__temperatureDataLayout)


        self.__precipitationSectionLabel=QLabel("PRÉCIPITATION")
        self.__precipitationSectionLabel.setMinimumSize(QSize(0,0))

        self.actualPrecipitationIntensityLabel.setMinimumSize(QSize(0,0))
        self.actualPrecipationProbabilityLabel.setMinimumSize(QSize(0,0))
        self.actualPrecipitationTypeLabel.setMinimumSize(QSize(0,0))
        self.__precipitationSectionLabel.setContentsMargins(0,0,0,0)
        self.actualPrecipitationIntensityLabel.setContentsMargins(0,0,0,0)
        self.actualPrecipationProbabilityLabel.setContentsMargins(0,0,0,0)
        self.actualPrecipitationTypeLabel.setContentsMargins(0,0,0,0)



        self.__precipitationDataLayout.addWidget(self.__precipitationSectionLabel)
        self.__precipitationDataLayout.addWidget(self.actualPrecipationProbabilityLabel)
        self.__precipitationDataLayout.addWidget(self.actualPrecipitationIntensityLabel)
        self.__precipitationDataLayout.addWidget(self.actualPrecipitationTypeLabel)
        self.__precipitationDataLayout.setAlignment(Qt.AlignLeft)
        self.__precipitationDataLayout.setSpacing(0)


        self.__precipitationAndWindDataLayout.addLayout(self.__precipitationDataLayout)

        self.__windSectionLabel=QLabel("VENT")
        self.__windSectionLabel.setMinimumSize(QSize(0,0))
        self.actualWindSpeedLabel.setMinimumSize(QSize(0,0))
        self.actualWindDirectionLabel.setMinimumSize(QSize(0,0))

        self.__windSectionLabel.setContentsMargins(0,5,0,0)
        self.actualWindSpeedLabel.setContentsMargins(0,0,0,0)
        self.actualWindDirectionLabel.setContentsMargins(0,0,0,0)


        self.__windDataLayout.addWidget(self.__windSectionLabel)
        self.__windDataLayout.addWidget(self.actualWindSpeedLabel)
        self.__windDataLayout.addWidget(self.actualWindDirectionLabel)
        self.__windDataLayout.setContentsMargins(0,0,0,0)
        self.__windDataLayout.setAlignment(Qt.AlignLeft)
        self.__windDataLayout.setSpacing(0)


        self.__precipitationAndWindDataLayout.addLayout(self.__windDataLayout)
        self.__precipitationAndWindDataLayout.setSpacing(0)

        self.__precipitationAndWindDataLayout.setContentsMargins(0,0,0,0)


        self.__weatherDataLayout.addLayout(self.__precipitationAndWindDataLayout)
        self.__weatherDataLayout.setContentsMargins(0,11,0,0)



        self.weatherWidget=QWidget()
        self.weatherWidget.setLayout(self.__weatherDataLayout)
        self.weatherHourContent.addWidget(self.weatherWidget)
        self.__weatherClockWidget.setLayout(self.weatherHourContent)
        self.__weatherClockWidget.setStyleSheet("font: 10pt")





        #Spotify
        self.songInfoLayout.addWidget(self.songTitleLabel)
        self.songInfoLayout.addWidget(self.artistsLabel)
        self.songInfoLayout.addWidget(self.albumTitleLabel)


        self.spotifyLayoutContent.addWidget(self.albumCoverLabel)

        self.spotifyLayoutContent.addLayout(self.songInfoLayout)

        self.__spotifyWidget.setLayout(self.spotifyLayoutContent)


        #Alarm
        # Other variables who don't need to be attrbutes of the class
        hourSpinBoxSuffix = " h"
        minuteSpinBoxSuffix = " min"

        # SPINBOX CONFIGURATION
        # Define the range and the step for all the Hour spinboxes.
        self.__mondayHourSpinbox.setRange(0, 23)  # Define  the minimal and maximal value of the spinbox.
        self.__mondayHourSpinbox.setSingleStep(
            1)  # Define the step value between two values in the spinbox. See the Qt doc for more details
        self.__mondayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        self.__tuesdayHourSpinbox.setRange(0, 23)
        self.__tuesdayHourSpinbox.setSingleStep(1)
        self.__tuesdayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        self.__wednesdayHourSpinbox.setRange(0, 23)
        self.__wednesdayHourSpinbox.setSingleStep(1)
        self.__wednesdayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        self.__thursdayHourSpinbox.setRange(0, 23)
        self.__thursdayHourSpinbox.setSingleStep(1)
        self.__thursdayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        self.__fridayHourSpinbox.setRange(0, 23)
        self.__fridayHourSpinbox.setSingleStep(1)
        self.__fridayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        self.__saturdayHourSpinbox.setRange(0, 23)
        self.__saturdayHourSpinbox.setSingleStep(1)
        self.__saturdayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        self.__sundayHourSpinbox.setRange(0, 23)
        self.__sundayHourSpinbox.setSingleStep(1)
        self.__sundayHourSpinbox.setSuffix(hourSpinBoxSuffix)

        # Define the range and the step for all the Minute spinboxes
        self.__mondayMinuteSpinbox.setRange(0, 23)
        self.__mondayMinuteSpinbox.setSingleStep(1)
        self.__mondayMinuteSpinbox.setSuffix(minuteSpinBoxSuffix)

        self.__tuesdayMinuteSpinbox.setRange(0, 59)
        self.__tuesdayMinuteSpinbox.setSingleStep(1)

        self.__wednesdayMinuteSpinbox.setRange(0, 59)
        self.__wednesdayMinuteSpinbox.setSingleStep(1)
        self.__wednesdayMinuteSpinbox.setSuffix(minuteSpinBoxSuffix)

        self.__thursdayMinuteSpinbox.setRange(0, 59)
        self.__thursdayMinuteSpinbox.setSingleStep(1)
        self.__thursdayMinuteSpinbox.setSuffix(minuteSpinBoxSuffix)

        self.__fridayMinuteSpinbox.setRange(0, 59)
        self.__fridayMinuteSpinbox.setSingleStep(1)
        self.__fridayMinuteSpinbox.setSuffix(minuteSpinBoxSuffix)

        self.__saturdayMinuteSpinbox.setRange(0, 59)
        self.__saturdayMinuteSpinbox.setSingleStep(1)
        self.__saturdayMinuteSpinbox.setSuffix(minuteSpinBoxSuffix)

        self.__sundayMinuteSpinbox.setRange(0, 59)
        self.__sundayMinuteSpinbox.setSingleStep(1)
        self.__sundayMinuteSpinbox.setSuffix(minuteSpinBoxSuffix)

        # Add the hour and minute spinbox of each day in the QVBox of each day.
        self.__mondaySettingsLayout.addWidget(self.__mondayAlarmCheckBox)
        self.__mondaySettingsLayout.addWidget(self.__mondayHourSpinbox)
        self.__mondaySettingsLayout.addWidget(self.__mondayMinuteSpinbox)

        self.__tuesdaySettingsLayout.addWidget(self.__tuesdayAlarmCheckBox)
        self.__tuesdaySettingsLayout.addWidget(self.__tuesdayHourSpinbox)
        self.__tuesdaySettingsLayout.addWidget(self.__tuesdayMinuteSpinbox)

        self.__wednesdaySettingsLayout.addWidget(self.__wednesdayAlarmCheckBox)
        self.__wednesdaySettingsLayout.addWidget(self.__wednesdayHourSpinbox)
        self.__wednesdaySettingsLayout.addWidget(self.__wednesdayMinuteSpinbox)

        self.__thursdaySettingsLayout.addWidget(self.__thursdayAlarmCheckBox)
        self.__thursdaySettingsLayout.addWidget(self.__thursdayHourSpinbox)
        self.__thursdaySettingsLayout.addWidget(self.__thursdayMinuteSpinbox)

        self.__fridaySettingsLayout.addWidget(self.__fridayAlarmCheckBox)
        self.__fridaySettingsLayout.addWidget(self.__fridayHourSpinbox)
        self.__fridaySettingsLayout.addWidget(self.__fridayMinuteSpinbox)

        self.__saturdaySettingsLayout.addWidget(self.__saturdayAlarmCheckBox)
        self.__saturdaySettingsLayout.addWidget(self.__saturdayHourSpinbox)
        self.__saturdaySettingsLayout.addWidget(self.__saturdayMinuteSpinbox)

        self.__sundaySettingsLayout.addWidget(self.__sundayAlarmCheckBox)
        self.__sundaySettingsLayout.addWidget(self.__sundayHourSpinbox)
        self.__sundaySettingsLayout.addWidget(self.__sundayMinuteSpinbox)

        # Set the layout of each day in a widget to add those layouts into an another layout
        self.__mondayWidget.setLayout(self.__mondaySettingsLayout)
        self.__tuesdayWidget.setLayout(self.__tuesdaySettingsLayout)
        self.__wednesdayWidget.setLayout(self.__wednesdaySettingsLayout)
        self.__thursdayWidget.setLayout(self.__thursdaySettingsLayout)
        self.__fridayWidget.setLayout(self.__fridaySettingsLayout)
        self.__saturdayWidget.setLayout(self.__saturdaySettingsLayout)
        self.__sundayWidget.setLayout(self.__sundaySettingsLayout)

        self.__dailySettingsLayout.addWidget(self.__mondayWidget)
        self.__dailySettingsLayout.addWidget(self.__tuesdayWidget)
        self.__dailySettingsLayout.addWidget(self.__wednesdayWidget)
        self.__dailySettingsLayout.addWidget(self.__thursdayWidget)
        self.__dailySettingsLayout.addWidget(self.__fridayWidget)
        self.__dailySettingsLayout.addWidget(self.__saturdayWidget)
        self.__dailySettingsLayout.addWidget(self.__sundayWidget)

        self.__weekWidget.setLayout(self.__dailySettingsLayout)


        self.__alarmSettingsLayout.addWidget(self.__weekAlarmCheckBox)
        self.__alarmSettingsLayout.addWidget(self.__weekWidget)
        self.__alarmSettingsLayout.addWidget(self.__confirmButton)
        self.__alarmWidget.setLayout(self.__alarmSettingsLayout)
        self.__alarmWidget.setStyleSheet("font:8pt")






        self.__changingContentWidget.addWidget(self.__weatherClockWidget)
        self.__changingContentWidget.addWidget(self.__spotifyWidget)
        self.__changingContentWidget.addWidget(self.__alarmWidget)
        self.__scrollZone=QScrollArea()
        self.__scrollZone.setWidgetResizable(True)
        self.__scrollZone.setWidget(self.__messenger.getWidget())
        self.__changingContentWidget.addWidget(self.__scrollZone)


        self.mainLayout.addWidget(self.__buttonsWidget)
        self.mainLayout.addWidget(self.__separatorLine)
        self.mainLayout.addWidget(self.__changingContentWidget)



        self.mainWidget=QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.layout=QHBoxLayout()
        self.layout.addWidget(self.mainWidget)
        self.setLayout(self.layout)


        #esthetics
        #General
        self.layout.setContentsMargins(0,0,0,0)
        self.__separatorLine.setFrameShape(QFrame.VLine)
        self.__separatorLine.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

        #Hour & Weather
        self.__weatherDescriptionLayout.setContentsMargins(0,0,0,0)
        self.__weatherDescriptionLayout.SetMinimumSize
        self.__weatherLayout.setContentsMargins(0,0,0,0)
        self.__weatherDataLayout.SetMinimumSize


        #spotify
        self.songTitleLabel.setStyleSheet("font: 16pt;")
        self.artistsLabel.setStyleSheet("font: 14pt;")
        self.albumTitleLabel.setStyleSheet("font: 12pt;")

    #Used by the code?
    def MessengerButtonAction(self):

        if(self.__changingContentWidget.currentIndex()==0):
            self.StopWeatherAndHourActualisation()
        elif(self.__changingContentWidget.currentIndex() == 1):
            self.StopSpotifyActualisation()
        self.__changingContentWidget.setCurrentIndex(self.__messengerNotificationButton.page)

    ##Private method to update the content of the Messenger notification's interface.
    # To update the content, the QWidgetList of the MessengerNotifGui class is returned regularly (each ten seconds)
    # and set into the QScrollArea object, __scrollZone.
    #
    # arg: none
    #
    # return: none
    def __UpdateMessengerNotificationInterface(self):
        self.__scrollZone.setWidget(self.__messenger.getWidget())


    ##Private method used by the instance of the Application class to update
    # the graphical and data notification structures of the MessengerNotifGui and UnreadMessageFetcher
    #
    # arg: none
    #
    # return: none
    def __UpdateNotification(self):
        self.__messenger.UpdateLists()
        self.__messenger.UpdateNotificationList()


    ##Private method used to initiate two QTimers used for calling the methods used to update the notifications.
    #
    # arg: none
    #
    # return: none
    def __initiateMessengerTimers(self):
        self.__messengerListTimer=QTimer()
        self.__messengerguiListTimer=QTimer()

        self.__messengerListTimer.timeout.connect(self.__UpdateNotification)
        self.__messengerguiListTimer.timeout.connect(self.__UpdateMessengerNotificationInterface)
        self.__StartMessengerTimer()


    ##Private method used to start two QTimers used for calling the methods used to update the notifications.
    #
    # arg: none
    #
    # return: none
    def __StartMessengerTimer(self):
        self.__messengerListTimer.start(6000)
        self.__messengerguiListTimer.start(10000)


    ##Private method used to stop two QTimers used for calling the methods used to update the notifications.
    #
    # arg: none
    #
    # return: none
    def __StopMessengerTimer(self):
        self.__messengerListTimer.stop()


    ##Private method used to specify what to do depending the actual widget showed by the QStackWidget and wich button the user is pressing.
    #
    # arg: selectionId: The id associated to the pressed button.
    #
    # return: none
    def __ButtonsAction(self,selectionId):
        currentIndex=self.__changingContentWidget.currentIndex()

        #What to do before change the widget showed by the QStackedWidget
        if(selectionId!=currentIndex):
            if(currentIndex==0):
                self.StopWeatherAndHourActualisation()
            elif(currentIndex==1):
                self.StopSpotifyActualisation()
            elif(currentIndex==3):

                """
                if (selectionId == 0):
                    self.__changingContentWidget.setCurrentIndex(self.weatherAndHourButton.page)
                    self.__UpdateHourAndWeather()
                    
                elif (selectionId == 1):
                    self.__changingContentWidget.setCurrentIndex(self.spotifyButton.page)
                    self.UpdateSongInfo()
                    
                elif (selectionId == 2):
                    self.__changingContentWidget.setCurrentIndex(self.__alarmButton.page)
                """

                self.__messenger.DeleteNotifications()
                self.__UpdateMessengerNotificationInterface()

            #What to do depending wich button was pressed by the user.
            if(selectionId==0):
                self.__changingContentWidget.setCurrentIndex(self.weatherAndHourButton.page)
                self.__initiateHourAndWeatherUpdate()
            elif(selectionId==1):
                self.__changingContentWidget.setCurrentIndex(self.spotifyButton.page)
                self.__initialiseSongInfoUpdate()
            elif(selectionId==2):
                self.__changingContentWidget.setCurrentIndex(self.__alarmButton.page)
            elif(selectionId==3):
                self.__changingContentWidget.setCurrentIndex(self.__messengerNotificationButton.page)


    ##Private method to set the content of the actual temperature label.
    #
    # arg: none
    #
    # return: none
    def __setActualTemp(self):
        realTemp = self.__weatherCondition.getTemp()
        self.actualTemperatureLabel.setText("Actual: " + str(realTemp) + " °C")


    ##Private method to set the content of the actual feeled temperature label.
    #
    # arg: none
    #
    # return: none
    def __setFeeledTemp(self):
        feeledTemp = self.__weatherCondition.getFeeledTemp()
        self.actualFeeledTemperatureLabel.setText("Actuelle: "+str(feeledTemp) + " °C")


    ##Private method to set the content of the actual weather description label.
    #
    # arg: none
    #
    # return: none
    def __setWeatherDesc(self):
        weatherDesc = self.__weatherCondition.getWeatherDesc()
        self.weatherDescriptionLabel.setText(weatherDesc)


    ##Private method to set the content of the actual precipitation probability label.
    #
    # arg: none
    #
    # return: none
    def __setActualPrecipitationProb(self):
        actualPrecipProb = self.__weatherCondition.getPrecipitationProb()
        self.actualPrecipationProbabilityLabel.setText("Probabilité: " + str(actualPrecipProb) + " %")


    ##Private method to set the content of the actual precipitation intensity label.
    #
    # arg: none
    #
    # return: none
    def __setActualPrecipIntensity(self):
        actualPrecipIntensity = self.__weatherCondition.getPrecipitationIntensity()
        self.actualPrecipitationIntensityLabel.setText("Intensité: " + str(actualPrecipIntensity) + " mm")


    ##Private method to set the content of the actual precipitation type label.
    #
    # arg: none
    #
    # return: none
    def __setActualPrecipType(self):
        actualPrecipType = self.__weatherCondition.getPrecipitationType()
        self.actualPrecipitationTypeLabel.setText("Type: " + str(actualPrecipType))


    ##Private method to set the content of the actual wind speed label.
    #
    # arg: none
    #
    # return: none
    def __setActualWindSpeed(self):
        actualWindSpeed = self.__weatherCondition.getWindSpeed()
        self.actualWindSpeedLabel.setText("Vitesse: " + str(actualWindSpeed) + " KM/H")


    ##Private method to set the content of the actual wind direction label.
    #
    # arg: none
    #
    # return: none
    def __setActualWindDir(self):
        actualWindDir = self.__weatherCondition.getWindDir()
        self.actualWindDirectionLabel.setText("Direction: " + str(actualWindDir) + "°")


    ##Private method to set the content of the daily maximum feeled temperature label.
    #
    # arg: none
    #
    # return: none
    def __setDailyMaxFeeledTemp(self):
        dailyMaxFeeledTemp = self.__weatherCondition.getDailyMaxFeeledTemp()
        self.dailyMaxTempLabel.setText("Maximum: " + str(dailyMaxFeeledTemp) + " °C")


    ##Private method to set the content of the daily minimum feeled temperature label
    #
    # arg: none
    #
    # return: none
    def __setDailyMinFeeledTemp(self):
        dailyMinFeeledTemp = self.__weatherCondition.getDailyMinFeeledTemp()
        self.dailyMinTempLabel.setText("Minimum: " + str(dailyMinFeeledTemp) + " °C")


    ##Private method to set the content of the hour Label
    #
    # arg: none
    #
    # return: none
    def setHour(self):
        self.hourLabel.setText(Hour())


    ##Private method to set the content of the date Label
    #
    # arg: none
    #
    # return: none
    def setDate(self):
        self.dateLabel.setText(Date())

    #def AfficherDate(self):
        #self.__label_Date.setText(Date())


    ##Private method to set the hour, the date and the weather at the beginning of the program.
    # The timeout.connect method of the QTimer class allow execute a fonction at a regular time interval. The fonction
    # is executed at each timeout of the QTimer. The __initialiseWeatherDateHourUpdate method initialises the timers
    # and set the weather, the hour and the date before the first timeout of the timers.
    #
    # arg: none
    #
    # return: none
    def __initialiseWeatherDateHourUpdate(self):

        self.setDate()
        self.setHour()
        self.setWeather()

        #Timer for WeatherClock's interface actualisation management
        self.__displayDateTimer = QTimer()
        self.__displayHourTimer = QTimer()
        self.__displayWeatherTimer = QTimer()

        #Timeout associated to the call of a method
        self.__displayDateTimer.timeout.connect(self.setDate)
        self.__displayHourTimer.timeout.connect(self.setHour)
        self.__displayWeatherTimer.timeout.connect(self.setWeather)

        #Initialisation of WeatherClock's timers
        #Connected methods will be called at each timer's timeout
        self.__displayDateTimer.start(60000)
        self.__displayHourTimer.start(200)  # Start a timer of 200ms
        self.__displayWeatherTimer.start(600000)


    ##Public method to stop weather, hour and date timers
    #
    # arg: none
    #
    # return: none
    def StopWeatherAndHourActualisation(self):
        self.__displayDateTimer.stop()
        self.__displayHourTimer.stop()
        self.__displayWeatherTimer.stop()


    ##Private method to do the same task as the __initialiseWeatherDateHourUpdate method but for the Spotify's song informations.
    #
    # arg: none
    #
    # return: none
    def __initialiseSongInfoUpdate(self):

        self.spotify.CheckSongInfo()
        self.UpdateSpotify()
        self.__songInfoActualisationTimer=QTimer()
        self.__spotifyInterfaceTimer=QTimer()
        self.__apiTokenTimer=QTimer()
        self.__songInfoActualisationTimer.timeout.connect(self.spotify.CheckSongInfo)
        self.__spotifyInterfaceTimer.timeout.connect(self.UpdateSpotify)
        self.__apiTokenTimer.timeout.connect(self.spotify.setAuthToken)
        self.__songInfoActualisationTimer.start(5000)
        self.__spotifyInterfaceTimer.start(5000)
        self.__apiTokenTimer.start(3590000)


    ##Public method to stop the Spotify's songs informations actualisation functionnality.
    #
    # arg: none
    #
    # return: none
    def StopSpotifyActualisation(self):
        self.__songInfoActualisationTimer.stop()
        self.__apiTokenTimer.stop()

        self.__spotifyInterfaceTimer.stop()


    ##Public method to update the Spotify functionnality's interface
    #
    # arg: none
    #
    # return: none
    def UpdateSpotify(self):
        self.songTitleLabel.setText(self.spotify.getSongTitle())
        self.artistsLabel.setText(self.spotify.getArtist())
        self.albumTitleLabel.setText(self.spotify.getAlbum())

        #Load the picture of the album cover from the fetched url of the Spotify class instance of this class.
        self.albumCover.loadFromData(urllib.request.urlopen(self.spotify.getAlbumCoverURL()).read())
        imagePixMap = QPixmap(self.albumCover)
        imagePixMap.scaled(100,100,QtCore.Qt.KeepAspectRatio)
        self.albumCoverLabel.setPixmap(imagePixMap)





    ##Public method to set the weather's data by calling all the private methods for setting the weather data used for the
    # weather-clock functionnality's interface.
    #
    # arg: none
    #
    # return: none
    def setWeather(self):
        self.__weatherCondition.Update()
        self.__setWeatherDesc()
        self.__setActualTemp()
        self.__setFeeledTemp()
        self.__setDailyMaxFeeledTemp()
        self.__setDailyMinFeeledTemp()
        self.__setActualWindSpeed()
        self.__setActualWindDir()
        self.__setActualPrecipitationProb()
        self.__setActualPrecipIntensity()
        self.__setActualPrecipType()


    ##This method does the same task as __initialiseSongInfoUpdate and __initialiseWeatherDateHourUpdate
    # but for the weather and clock functionnality.
    def __initiateHourAndWeatherUpdate(self):

        self.setDate()
        self.setHour()
        self.setWeather()


        self.__displayDateTimer = QTimer()
        self.__displayHourTimer = QTimer()
        self.__displayWeatherTimer = QTimer()


        self.__displayDateTimer.timeout.connect(self.setDate)
        self.__displayHourTimer.timeout.connect(self.setHour)
        self.__displayWeatherTimer.timeout.connect(self.setWeather)


        self.__displayDateTimer.start(60000)
        self.__displayHourTimer.start(200)  # démarre un timer de 200ms
        self.__displayWeatherTimer.start(600000)


    ##Private method to set the lists for the alam clock by reading the saved settings into a csv.
    #
    # The csv contains 3 rows of 8 columns.
    #
    # The first column contains the parameter for the whole week and each other columns are for each day of the weak
    # (monday to sunday).
    # First row: Contain the status of the alarm clock, the possible values are "on" or "off" for each column. If
    # the first column of the first row is off, the alarm clock is disabled for the entire week.
    # Second row: This row contains the hour where the alarm will ring (if enabled) for each day of the week.
    # Note that the second and third row of the first column are not used.
    #Third row: This row contains the minute of the hour where the alarm will ring (if enabled) for each day of the week.
    #
    # arg: none
    #
    # return: none
    def __FillLists(self):
        with open(self.__fileName) as csvDataFile:
            csvReader = csv.reader(csvDataFile)

            for row in csvReader:

                    rangee=csvReader.line_num
                    for x in range(8):
                        if(rangee==1):
                            self.__activeDaysList.append(row[x])
                        elif(rangee==2):
                            self.__alarmActivationHoursList.append(row[x])
                        elif(rangee==3):
                            self.__alarmActivationMinuteList.append(row[x])
        csvDataFile.close()

    ##Private method to display the content of the alarm clock' data lists into the alarm clock' interface.
    # weather-clock functionnality's interface.
    #
    # arg: none
    #
    # return: none
    def __ImportAlarmSettingsToGUI(self):
        self.__FillLists()

        isAlarmAlwaysOff=False

        for x in range(8):
            if(x==0):
                if(self.__activeDaysList[x]== "on"):
                    self.__weekAlarmCheckBox.setChecked(True)
                    self.__mondayAlarmCheckBox.setCheckable(True)
                    self.__tuesdayAlarmCheckBox.setCheckable(True)
                    self.__wednesdayAlarmCheckBox.setCheckable(True)
                    self.__thursdayAlarmCheckBox.setCheckable(True)
                    self.__fridayAlarmCheckBox.setCheckable(True)
                    self.__saturdayAlarmCheckBox.setCheckable(True)
                    self.__sundayAlarmCheckBox.setCheckable(True)
                else:
                    isAlarmAlwaysOff=True
                    self.__weekAlarmCheckBox.setChecked(False)
                    self.__mondayAlarmCheckBox.setCheckable(False)
                    self.__tuesdayAlarmCheckBox.setCheckable(False)
                    self.__wednesdayAlarmCheckBox.setCheckable(False)
                    self.__thursdayAlarmCheckBox.setCheckable(False)
                    self.__fridayAlarmCheckBox.setCheckable(False)
                    self.__saturdayAlarmCheckBox.setCheckable(False)
                    self.__sundayAlarmCheckBox.setCheckable(False)

            elif(x==1):
                if(isAlarmAlwaysOff==False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__mondayAlarmCheckBox.setChecked(True)
                    else:
                        self.__mondayAlarmCheckBox.setChecked(False)

                self.__mondayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__mondayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

            elif (x == 2):
                if (isAlarmAlwaysOff == False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__tuesdayAlarmCheckBox.setChecked(True)
                    else:
                        self.__tuesdayAlarmCheckBox.setChecked(False)

                self.__tuesdayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__tuesdayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

            elif (x == 3):
                if (isAlarmAlwaysOff == False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__wednesdayAlarmCheckBox.setChecked(True)
                    else:
                        self.__wednesdayAlarmCheckBox.setChecked(False)

                self.__wednesdayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__wednesdayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

            elif (x == 4):
                if (isAlarmAlwaysOff == False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__thursdayAlarmCheckBox.setChecked(True)
                    else:
                        self.__thursdayAlarmCheckBox.setChecked(False)

                self.__thursdayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__thursdayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

            elif (x == 5):
                if (isAlarmAlwaysOff == False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__fridayAlarmCheckBox.setChecked(True)
                    else:
                        self.__fridayAlarmCheckBox.setChecked(False)

                self.__fridayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__fridayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

            elif (x == 6):
                if (isAlarmAlwaysOff == False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__saturdayAlarmCheckBox.setChecked(True)
                    else:
                        self.__saturdayAlarmCheckBox.setChecked(False)

                self.__saturdayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__saturdayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

            elif (x == 7):
                if (isAlarmAlwaysOff == False):
                    if (self.__activeDaysList[x] == "on"):
                        self.__sundayAlarmCheckBox.setChecked(True)
                    else:
                        self.__sundayAlarmCheckBox.setChecked(False)

                self.__sundayHourSpinbox.setValue(int(self.__alarmActivationHoursList[x]))
                self.__sundayMinuteSpinbox.setValue(int(self.__alarmActivationMinuteList[x]))

    ##Private method to set the alarm clock's settings of the interface into the data structures when the user apply the change
    #
    # arg: none
    #
    # return: none
    def __ChangeSettingsListsValues(self):
        for x in range(8):
            if(x==0):
                if(self.__weekAlarmCheckBox.isChecked()==True):
                    self.__activeDaysList[x]= "on"
                else:
                    self.__activeDaysList[x] = "off"

            if(x==1):
                if(self.__mondayAlarmCheckBox.isChecked()==True):
                    self.__activeDaysList[x]= "on"
                    self.__alarmActivationHoursList[x]=str(self.__mondayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x]=str(self.__mondayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x]= "off"

            if (x == 2):
                if (self.__tuesdayAlarmCheckBox.isChecked() == True):
                    self.__activeDaysList[x] = "on"
                    self.__alarmActivationHoursList[x] = str(self.__tuesdayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x] = str(self.__tuesdayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x] = "off"

            if (x == 3):
                if (self.__wednesdayAlarmCheckBox.isChecked() == True):
                    self.__activeDaysList[x] = "on"
                    self.__alarmActivationHoursList[x] = str(self.__wednesdayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x] = str(self.__wednesdayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x] = "off"

            if (x == 4):
                if (self.__thursdayAlarmCheckBox.isChecked() == True):
                    self.__activeDaysList[x] = "on"
                    self.__alarmActivationHoursList[x] = str(self.__thursdayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x] = str(self.__thursdayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x] = "off"

            if (x == 5):
                if (self.__fridayAlarmCheckBox.isChecked() == True):
                    self.__activeDaysList[x] = "on"
                    self.__alarmActivationHoursList[x] = str(self.__fridayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x] = str(self.__fridayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x] = "off"

            if (x == 6):
                if (self.__saturdayAlarmCheckBox.isChecked() == True):
                    self.__activeDaysList[x] = "on"
                    self.__alarmActivationHoursList[x] = str(self.__saturdayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x] = str(self.__saturdayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x] = "off"

            if (x == 7):
                if (self.__sundayAlarmCheckBox.isChecked() == True):
                    self.__activeDaysList[x] = "on"
                    self.__alarmActivationHoursList[x] = str(self.__sundayHourSpinbox.value())
                    self.__alarmActivationMinuteList[x] = str(self.__sundayMinuteSpinbox.value())
                else:
                    self.__activeDaysList[x] = "off"

    ##Public method to delete the csv because the csv module doesn't have an overwrite mode.
    # So, the file is deleted and recreated with the new content.
    #
    # arg: none
    #
    # return: none
    def DeleteOldCSV(self):
        os.remove(self.__fileName)

    ##Private method to write the new alarm clock's settings into a new csv
    # weather-clock functionnality's interface.
    #
    # arg: none
    #
    # return: none
    def __ExportSettingsToCSV(self):
        newContent=[self.__activeDaysList, self.__alarmActivationHoursList, self.__alarmActivationMinuteList]
        file=open(self.__fileName, 'w')

        with file:
            writeNewSettings=csv.writer(file)
            writeNewSettings.writerows(newContent)
        file.close()

    ##Public method for calling all the private methods required to apply the settings change.
    #
    # arg: none
    #
    # return: none
    def ApplySettingsChange(self):
        self.__ChangeSettingsListsValues()
        self.DeleteOldCSV()
        self.__ExportSettingsToCSV()
        self.__ImportAlarmSettingsToGUI()

    ##Private method for iniating the alarm timer
    #useless?
    # arg: none
    #
    # return: none
    def __initiateAlarmTimer(self):
        self.__setAlarmTimers()
        self.timerAlarmTimer=QTimer()
        self.timerAlarmTimer.timeout.connect(self.__setAlarmTimers)
        self.timerAlarmTimer.start((3600000 * 24))

    ##Public method to set timers required to have a timeout to the time where the alarm clock has to ring.
    #
    # arg: none
    #
    # return: none
    def __setAlarmTimers(self):
        #Todo just alarmtimer is required-> updated the _alarmtimer at each settings update
        self.__setAlarmTimerTime()
        self.__updateTimerCheckTimeTimer = QTimer()
        self.__alarmTimer = QTimer()

        self.__updateTimerCheckTimeTimer.timeout.connect(self.__setAlarmTimerTime)
        self.__alarmTimer.timeout.connect(self.Alarm)


        extraTimeForChecking=self.__timeUntilNextAlarmCheck+120000
        self.__updateTimerCheckTimeTimer.start(extraTimeForChecking)
        if(self.__alarmToday==True):
            self.__alarmTimer.start(self.__timeUntilNextAlarmCheck)


    ##Private method to determine the number of milisecond before the next alarm
    #
    # arg: none
    #
    # return: none
    def __setAlarmTimerTime(self):
        actualDay=datetime.datetime.now()
        actualDayNumber=actualDay.weekday()+1

        alarmHour=self.__alarmActivationHoursList[actualDayNumber]
        alarmMin=self.__alarmActivationMinuteList[actualDayNumber]
        if(self.__activeDaysList[0]=='on'):

            if(self.__activeDaysList[actualDayNumber]=='on'):
                self.__alarmToday=True


            else:
                self.__alarmToday=False




        nextAlarmDate = datetime.datetime(actualDay.year, actualDay.month, actualDay.day, int(alarmHour), int(alarmMin), 0)
        if (nextAlarmDate > actualDay):
            timeDifference = nextAlarmDate - actualDay
            self.__timeUntilNextAlarmCheck= timeDifference.microseconds

        else:

            nextAlarmDate = nextAlarmDate+datetime.timedelta(days=1)
            timeDifference = nextAlarmDate - actualDay
            self.__timeUntilNextAlarmCheck = timeDifference.microseconds



    ##Public method to play the alarm ring tone.
    #
    # arg: none
    #
    # return: none
    def Alarm(self):
        self.t=Thread(target=PlayAlarmBell)
        self.t.daemon=False
        self.t.start()
        self.__setAlarmTimers()


    ##Public method to initiate the baclight adjustement.
    # Between 5:30 and 21:30 the baclight is in day mode (max intensity)
    # and the backlight is in nightmode (very low intensity) the reste of the time.
    # The method determine if the programm begin in daymode or in darkmode and initialise the timer to determine when
    # the programm will change tbacklight mode again.
    #
    # arg: none
    #
    # return: none
    def __InitiateBacklight(self):
        rightNow=datetime.datetime.now()
        dayModeTime=datetime.datetime(rightNow.year,rightNow.month,rightNow.day,5,30,0)
        nightModeTime=datetime.datetime(rightNow.year,rightNow.month,rightNow.day,21,30,0)
        timeUntilModeChange:datetime
        self.__isDayMode=True

        if(dayModeTime>=rightNow):
            timeUntilModeChange=dayModeTime-rightNow
            self.__isDayMode=False
            setBackLight(15)


        elif(nightModeTime>=rightNow):
            timeUntilModeChange=nightModeTime-rightNow
            self.__isDayMode=True
            setBackLight(255)

        else:#rightNow > nightModeTime
            self.__isDayMode=False
            setBackLight(15)
            dayModeTime=datetime.datetime(rightNow.year,rightNow.month,(rightNow.day+1),5,30,0)
            timeUntilModeChange=dayModeTime-rightNow

        self.__backlightActualisationTimer = QTimer()
        self.__backlightActualisationTimer.timeout.connect(self.__ChangeBackLightIntensity)


    ##Private methode to set the opposite backlight mode of the actual one.
    # Since the programm is iniatiated, determine when the backlight change happen is not required anymore.
    # The program will run constantly after his launch. So after the update time will be constant after the initialisation.
    #
    # arg: none
    #
    # return: none
    def __ChangeBackLightIntensity(self):
        self.__backlightActualisationTimer.stop()

        #set the opposite mode of the actual one
        if(self.__isDayMode==True):
            setBackLight(15)
            self.__isDayMode=False
            self.__backlightActualisationTimer.start(28800000)#8hours of sleep! :)

        else:
            setBackLight(255)
            self.__isDayMode=True
            self.__backlightActualisationTimer.start(57600000)#change backlight in 16hours

    def __initialiseRaspotify(self):
        t=Thread(target=RestartRaspotify.RestartService)
        t.start()

##Function to return the time into the interface.
#
# arg: none
#
# return: hour.
def Hour():
    heure = time.strftime("%H : %M : %S")
    return heure


##Function to return the date into the interface.
#
# arg: none
#
# return: date.
def Date():
    date=time.strftime("%A %d %B %Y")
    return date



## The code of the "main" is just an instanciation of the Application class.
if __name__ == '__main__':

    """
    A QApplication instance is instancied before the instanciation of the Application class
    because QApplication must be instancied before instanciating other Q objects. And of course,
    the Application class contains a lot of Q objects.
    """
    App=QApplication(sys.argv)
    window=Application()
    sys.exit(App.exec())
