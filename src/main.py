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

#Global Vars
joinDict = {}   #Dictionary containing the last join time of users
msgQ = []       #Queue containing the last 5 messages received in the channel the bot resides in
userList = []   #List of the users



