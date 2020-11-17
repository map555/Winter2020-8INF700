from threading import Thread
import os
import csv
import datetime
from Sounds import PlayAlarmBell
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

## The class of the alarm clock functionnality
class Alarm(QWidget):
    def __init__(self):
        super().__init__()

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

    ##Private method to delete the csv because the csv module doesn't have an overwrite mode.
    # So, the file is deleted and recreated with the new content.
    #
    # arg: none
    #
    # return: none
    def __DeleteOldCSV(self):
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
        self.__DeleteOldCSV()
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

    ##Private method to set timers required to have a timeout to the time where the alarm clock has to ring.
    #
    # arg: none
    #
    # return: none
    def __setAlarmTimers(self):
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
            self.__timeUntilNextAlarmCheck=(timeDifference.microseconds*1000) # *1000 to get miliseconds
        else:

            nextAlarmDate = nextAlarmDate+datetime.timedelta(days=1)
            timeDifference = nextAlarmDate - actualDay
            self.__timeUntilNextAlarmCheck = (timeDifference.microseconds*1000)


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

