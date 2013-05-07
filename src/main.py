#Utility/Framework Imports
import time
from ircutils import bot, format
#import dokuwikixml
from datetime import datetime
from record import *
from usermanager import *
from schedulehandler import *
from config import *

#Global Vars
userList = []   #List of the users
activeUsers = [] #list of all users currently logged into the channel
absentUsers = []#list of users who are more than 4 hours late

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
    

#AdminBot is a customized IRC bot that listens for certain behaviors in an IRC channel and can respond to commands given by administrator
                        
class AdminBot(bot.SimpleBot):
    
    #Gets called when a user joins the chat
    def on_join(self, event):
        record = Record()
        #Passes user and login time to be recorded
        if event.source != self.nickname:
            self.send_message(event.target, "Welcome, " + event.source + "!")
            Record.login(record, event.source, datetime.now())
        
            timeLate = Record.checkLate(record, event.source, datetime.now())
            if timeLate[0] > -1:
                if timeLate[1] > -1:
                    sendString = event.source + " is late by " + str(timeLate[0]) + " hours and " + str(timeLate[1]) + " minutes"
                    self.send_message(event.target, sendString)
        
        
        # once a user joins the chat, add user name to the activeUser list
        activeUsers.append(event.source)
        # sort the list
        activeUsers.sort(key=str.lower)
        return
    
    #Gets called when a user leaves chat
    def on_quit(self, event):
        record = Record()
        #Passes user and logout time to be recorded
        Record.logout(record, event.source, datetime.now())
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
            UserManager().addUser(self, params, event.source)

        #Delete user command
        elif cmd == 'DELUSER':
            UserManager().deleteUser(self, params, event.source)
        
        # command to display all users currently logged into the channel
        elif cmd == 'SHOWUSERS':
            UserManager().showUsers(self, event.source)
            
        # command to display all users currently logged into the channel
        elif cmd == 'SCHEDULE':
            if msg[1].upper() == 'ADD':
                ScheduleHandler().addSchedule(self, params, event)
            if msg[1].upper() == 'REMOVE':
                ScheduleHandler().removeSchedule(self, params, event)
            
        elif cmd == 'CHANGEPERIODENDDATE':
            ScheduleHandler().changePayPeriod(self, params, event.source)
        
        # if command is invalid, send error message and throw an exception
        else:
            pass
            



if __name__ == "__main__":
    # Create an instance of the bot
    # We set the bot's nickname here
    adminBot = AdminBot( adminBotName )
    
    # Let's connect to the host
    adminBot.connect(adminBotServer, channel=[ adminBotChannel ])

    # Start running the bot
    adminBot.start()

