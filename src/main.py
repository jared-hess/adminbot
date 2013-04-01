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
activeUsers = [] #list of all users currently logged into the channel

bufsize = 0
userFile = open('userlist.txt', 'r')
userList = userFile.readlines()

#Get rid of new lines
userList = map(lambda s: s.strip(), userList)


def update_list(new_list):
    userFile = open('userlist.txt', 'w', bufsize)
    for item in new_list:
        userFile.write(item + '\n')
    userFile.close()
    
# this function performs a binary search on a list and returns the index of the item searched for
def search(currentUsers, item):
    low = 0
    # get the length of the list
    high = len(currentUsers) - 1
    while high >= low:
        # calculate the midpoint of the list
        mid = low + ((high - low) / 2)
        if item < currentUsers[mid]:
            high = mid - 1
        elif item > currentUsers[mid]:
            low = mid + 1
        elif item == currentUsers[mid]:
            return mid
    # if user was not found in the list
    return -1
    
    
#Record Class (records times)
#Should probably be moved to another file
class Record:
    def login(self, user, time):
        #Record login time
        f = open(user,'a')
        f.write('Login:' + time + '\n')
        f.close()
        return
    def logout(self, user, time):
        #Record logout time
        f = open(user,'a')
        f.write('Logout:' + time + '\n')
        f.close()
        return
        


#AdminBot is a customized IRC bot that listens for certain behaviors in an IRC channel and can respond to commands given by administrator
             
            
class AdminBot(bot.SimpleBot):
    
    #Gets called when a user joins the chat
    def on_join(self, event):
        #Passes user and login time to be recorded
        if event.source != self.nickname:
            self.send_message(event.target, "Welcome, " + event.source + "!")
        Record.login(event.source, datetime.now())
        # once a user joins the chat, add user name to the activeUser list
        activeUsers.append(event.source)
        # sort the list
        activeUsers.sort(key=str.lower)
        return
    
    #Gets called when a user leaves chat
    def on_quit(self, event):
        #Passes user and logout time to be recorded
        Record.logout(event.source, datetime.now())
        # search for the user name to delete from the list once the user leaves the chat
        index = search(activeUsers, event.source)
        del activeUsers[index]
        return
    
    #Defines how to handle private messages sent to the admin bot
    def on_private_message(self, event):
        msg = event.message.split()
        cmd = msg[0].upper()
        params = msg[1:]
    
        #Add user command
        if cmd == 'ADDUSER':
            for item in params:
                if item in userList:
                    self.send_message(event.source, item + ' is already in user list!')
                else:
                    userList.append(item.rstrip())
                    self.send_message(event.source, item + ' was added to list!')   
                update_list(userList)


        #Delete user command
        elif cmd == 'DELUSER':
            for item in params:
                if item in userList:
                    userList.remove(item)
                    self.send_message(event.source, item + ' was removed from the list!')
                else:
                    self.send_message(event.source, item + ' was not even in the list!')
                update_list(userList)
        
        # command to display all users currently logged into the channel
        elif cmd == 'SHOWUSERS':
            
            self.send_message(event.source, 'Users currently logged in:\n')
            print 'Users currently logged in\n'
            
            for user in activeUsers:
                self.send_message(event.source, user + '\n')
                print user



if __name__ == "__main__":
    # Create an instance of the bot
    # We set the bot's nickname here
    adminBot = AdminBot( adminBotName )
    
    # Let's connect to the host
    adminBot.connect(adminBotServer, channel=[ adminBotChannel ])

    # Start running the bot
    adminBot.start()




   

    

