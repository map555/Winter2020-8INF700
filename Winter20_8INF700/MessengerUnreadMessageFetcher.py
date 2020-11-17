from threading import Thread
from fbchat import Client
from Sounds import PlayNotificationSound

## The data class for the messenger notification functionnality
# The role of this class is to fetch the notifications' data.
class UnreadMessageFetcher():
    def __init__(self, username, password):
        self.__newUnreadMessageNb = 0  # Number of unread messages before the next graphic user interface actualusation.
        self.__unreadMessageDictionnaryList = []
        self.__threadList = []
        self.__unRodeThread = []

        self.__client = Client(username, password)
        self.__setThreadList()
        self.__setUnreadMessagesList()

    ##Public method to empty the list of notifications.
    #
    # arg: none
    #
    # return: none
    def EmptyLists(self):
        """
        To avoid to refill the list with already fetched notification, each conversation with at least one unread message is marked as read. To avoid to empty an already empty list,
        the size of the notification list must be superior to zero to empty the list.
        """
        if (len(self.__unreadMessageDictionnaryList) > 0):
            self.__unreadMessageDictionnaryList = []
            for i in range(len(self.__unRodeThread)):
                self.__client.markAsRead(self.__unRodeThread[i].uid)
            self.__threadList = []

    ##Private method to affect the list of the ten most recent messenger conversations of the user into the __threadlist attribute.
    #
    # arg: none
    #
    # return: none
    def __setThreadList(self):
        self.__threadList = self.__client.fetchThreadList(limit=10)

    ##Private method for setting the  __unreadMessageDictionnaryList attribute by storing the unread messages dictionnaries' into the list.
    #
    # arg: none
    #
    # return: none
    def __setUnreadMessagesList(self):
        i = 0
        isDictEmpty = False
        while ((i < 10) and (isDictEmpty == False)):
            dict = self.__getUnReadMessageDict(i)
            if ((dict != {}) and (not (dict in self.__unreadMessageDictionnaryList))):
                self.__unreadMessageDictionnaryList.append(dict)
                self.__newUnreadMessageNb += 1

                # ToDo check if the thread is already into the list before adding the thread into the list. For avoiding to mark as read a thread twice.
                self.__unRodeThread.append(self.__threadList[i])
                notifSoundThread = Thread(
                    target=PlayNotificationSound)  # For running the sound notification into a second thread who will run in a parallel of the main one.
                notifSoundThread.start()  # Starting the thread.
            else:
                isDictEmpty = True
            i += 1

    ##Private method to get the unread message dictionnary of the selected conversation.
    #
    # arg: threadIndex: the index of the conversation.
    #
    # return: unReadMessageDict: the unread message dictionnary of the selected conversation.
    def __getUnReadMessageDict(self, threadIndex):
        unreadMessageDict = {}

        fetchedMessage = self.__client.fetchThreadMessages(thread_id=self.__threadList[threadIndex].uid, limit=1)

        if (fetchedMessage[0].is_read == False):
            if (self.__threadList[threadIndex].type.name == "USER"):
                name = self.__threadList[threadIndex].name
            else:

                authorname = self.__getaUserName(fetchedMessage[
                                                     0].author)  # Get the name of the author of the last message in a group conversation with his user ID
                name = self.__threadList[
                           threadIndex].name + " (" + authorname + ")"  # Concatenate the author name in parenthesis with the name of the conversation
            message = fetchedMessage[0].text
            photo = self.__threadList[threadIndex].photo
            unreadMessageDict = {"name": name, "photo": photo, "message": message}

        return (unreadMessageDict)

    ##Public method to reset the unread message counter when emptying the notification list.
    #
    # arg: none
    #
    # return: none
    def resetNewUnreadMessageNb(self):
        self.__newUnreadMessageNb = 0

    ##Public method to update the __threadList and __unreadMessageLis attributes
    #
    # arg: none
    #
    # return: none
    def setLists(self):
        self.__setThreadList()
        self.__setUnreadMessagesList()

    ## Private method to get the name of the user who sent the message in a group conversation.
    # Messenger uses the real name of the other user in the name attribut of the dictionnary for
    # user to user conversation and group's name for group conversation. To specify who sent the
    # message, this method fetches the profile's informations of the user who sends the message
    # by using is facebook id (each message dictionnary returned by the client object by the
    # fbchat module contains the id of the user who sent the message) and extract his name to
    # return it to the __getUnReadMessageDict method.
    #
    # arg: userId: The Facebook user's id of the user who sent the message.
    #
    # return: name: The name of the user who sent the message.
    def __getaUserName(self, userId):

        userInfo = self.__client.fetchUserInfo(userId)

        name = userInfo.get(userId).name
        return (name)


    ##Public method to optain the size of the list
    # Usefull?
    # arg: none
    #
    # return: d: The size of the __unreadMessageDictionnaryList attribute.
    def getTotalUnreadMessageNumber(self):
        d = len(self.__unreadMessageDictionnaryList)
        return (d)

    ##Public method to get the number of new unread messages fetched during an iteration of
    # the __setUnReadMessageList method. #Usefull? Must see that at the last refactorings.
    #
    # arg: none
    #
    # return: __newUnReadMessageNb: The number of new unread messages fetched during an iteration of the
    # __setUnReadMessageList method.
    def getNewUnreadMessageNumber(self):
        return (self.__newUnreadMessageNb)



    ##Public method to return the message author's name into the interface.
    #
    # arg: dictIndex: the index of the selected message dict into the __unreadMessageDictionnaryList attribute.
    #
    # return: self.__unreadMessageDictionnaryList[dictIndex].get('name'): The message author's name.
    def getAuthorName(self, dictIndex):
        return (self.__unreadMessageDictionnaryList[dictIndex].get('name'))


    ##Public method to return the url of the message author's profile picture for loading it into the interface.
    #
    # arg: dictIndex: the index of the selected message dict into the __unreadMessageDictionnaryList attribute.
    #
    # return: self.__unreadMessageDictionnaryList[dictIndex].get('photo'): The url of the message author's profile picture.
    def getConversationPic(self, dictIndex):
        return (self.__unreadMessageDictionnaryList[dictIndex].get('photo'))


    ##Public method to return the message into the interface.
    #
    # arg: dictIndex: the index of the selected message dict into the __unreadMessageDictionnaryList attribute.
    #
    # return: self.__unreadMessageDictionnaryList[dictIndex].get('message'): The unread message.
    def getMessage(self, dictIndex):
        return (self.__unreadMessageDictionnaryList[dictIndex].get('message'))
