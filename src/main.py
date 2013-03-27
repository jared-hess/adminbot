#Configuration
#To be moved to another file later
wikiURL = "http://wiki.parc.com/"       #URL for your Wiki
userListPath = "user_list"              #URL where you store the user list on the wiki
adminBotChannel = "#adminbot-test1"     #IRC Channel you want the Admin Bot to join
adminBotName = "admin_bot"              #IRC Bot Name
adminBotServer = "irc.spotchat.org"     #IRC Server 

#Utility/Framework Imports
import getpass
import time
from ircutils import bot, format
import dokuwikixmlrpc
from datetime import datetime

#Global Vars
joinDict = {}   #Dictionary containing the last join time of users
msgQ = []       #Queue containing the last 5 messages received in the channel the bot resides in
userList = []   #List of the users

#Record Class (records times)
#Should probably be moved to another file
class Record:
    def login(self, user, time):
        #Do whatever
        return
    def logout(self, user, time):
        #Do whatever
        return

#IRC Bot Definition
class RoomBot(bot.SimpleBot):
    #Gets called when a user joins the chat
    def on_join(self, event):
        Record.login(event.source, datetime.now())
        return
    #Gets called when a user leaves chat
    def on_quit(self, event):
        Record.logout(event.source, datetime.now())
        return

    

