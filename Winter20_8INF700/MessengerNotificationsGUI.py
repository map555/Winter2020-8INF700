from threading import Thread,Lock
import urllib.request
from MessengerUnreadMessageFetcher import UnreadMessageFetcher
from getAuthTokens import getMessengerUserName,getMessengerPassword
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QScrollArea,QListWidgetItem,QListWidget,QApplication, QSizePolicy, QFrame, QDialog, QVBoxLayout, QLabel, \
    QHBoxLayout, QWidget


## The graphical user interface class of the messenger notification functionnality
# The role of this class is to generate the graphical notifications list for the main interface.
class MessengerNotifGui(QDialog):
    def __init__(self):
        super().__init__()
        self.__mutex=Lock()#TODO useless?
        self.unreadMessageFetcher=UnreadMessageFetcher(getMessengerUserName(),getMessengerPassword())
        self.__list = QListWidget()
        self.UpdateNotificationList()

    ##Public method to return notifications widget to the application class' instance for fill the notification's 
    # scrollable area by returning all the notification widgets into a single widget list containing all the
    # notifications.
    #
    # arg: none
    #
    # return: __list: a QListWidget (a list for QWidget objects) containing all the notifications.
    def getWidget(self):
        return(self.__list)


    ##Public method used by the application class' instance to actualise the content of the thread list and the
    # notification dictionnary list.
    #
    # arg: none
    #
    # return: none
    def UpdateLists(self):
        self.unreadMessageFetcher.setLists()


    ##Public method to update the content of the graphical version of the notification list.
    # The method uses the size of __unreadMessageDictionnaryList and the value of __newUnreadMessageNb
    # deduce the new unread messages' indexes and loop into the new values add into the
    # __unreadMessageDictionnaryList to fetch the informations contained into the new dictionnaries of
    # the list.
    #
    # arg: none
    #
    # return: none
    def UpdateNotificationList(self):

        totalListSize=self.unreadMessageFetcher.getTotalUnreadMessageNumber()
        newListElementNb=self.unreadMessageFetcher.getNewUnreadMessageNumber()
        for i in range(newListElementNb):
            index=((totalListSize-newListElementNb)+i)
            notificationLayout=QHBoxLayout()
            messageLayout=QVBoxLayout()
            messageTextLayout=QVBoxLayout()
            authorLayout=QVBoxLayout()
            messageLabel=QLabel(self.unreadMessageFetcher.getMessage(index))
            messageLabel.setWordWrap(True)

            authorLabel=QLabel(self.unreadMessageFetcher.getAuthorName(index))
            conversationPicURL=self.unreadMessageFetcher.getConversationPic(index)
            conversationPic=QtGui.QImage()

            conversationPic.loadFromData(urllib.request.urlopen(conversationPicURL).read())
            pixmap=QPixmap(conversationPic)
            pixmap.scaled(50,50)
            conversationPicLabel=QLabel()
            conversationPicLabel.setPixmap(pixmap)
            authorLayout.addWidget(authorLabel)
            messageTextLayout.addWidget(messageLabel)


            if (i < (newListElementNb - 1)):
                separatorLine = QFrame()
                separatorLine.setFrameShape(QFrame.HLine)
                separatorLine.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
                messageTextLayout.addWidget(separatorLine)

            messageLayout.addLayout(authorLayout)
            messageLayout.addLayout(messageTextLayout)
            notificationLayout.addWidget(conversationPicLabel)
            notificationLayout.addLayout(messageLayout)
            notificationWidget=QWidget()
            notificationWidget.setLayout(notificationLayout)
            notificationItem=QListWidgetItem()
            notificationItem.setSizeHint(notificationWidget.sizeHint())
            self.__list.addItem(notificationItem)
            self.__list.setItemWidget(notificationItem,notificationWidget)



            #Esthetics
            messageLabel.setAlignment(Qt.AlignLeft)
            authorLabel.setAlignment(Qt.AlignLeft)
            messageLayout.setAlignment(Qt.AlignLeft)
            font=QtGui.QFont()
            font.setBold(True)
            authorLabel.setFont(font)

        self.unreadMessageFetcher.resetNewUnreadMessageNb()


    ##Public method used by the application class' instance to empty the graphical and the data notification
    # structures from the MessengerNotifGui and UnreadMessageFetcher class instances.
    # notification dictionnary list.
    #
    # arg: none
    #
    # return: none
    def DeleteNotifications(self):

        emptyListsThread=Thread(target=self.unreadMessageFetcher.EmptyLists)
        emptyListsThread.start()
        self.__list.clear()





