from subprocess import call




##Function to play a notification sound when the user receives a new message on Messenger.
#
# arg: none
#
# return: none
def PlayNotificationSound():
    """
    MP3 file took from:
    https://notificationsounds.com/message-tones/get-outta-here-505
    """
    call('mpg123 get-outta-here.mp3',shell=True)

##Function to play a ring-tone for the alarm clock..
#
# arg: none
#
# return: none
def PlayAlarmBell():
        call('mpg123 StarTrek_TNG_Red_Alert.mp3',shell=True)

