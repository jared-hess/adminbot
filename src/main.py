#Configuration
#To be moved to another file later
wikiURL = "http://wiki.parc.com/"       #URL for your Wiki
userListPath = "user_list"              #URL where you store the user list on the wiki
adminBotChannel = "#adminbot-test1"     #IRC Channel you want the Admin Bot to join
adminBotName = "admin_bot"              #IRC Bot Name
adminBotServer = "irc.spotchat.org"     #IRC Server 

#Utility/Framework Imports
import re
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
''' This class records the times users joined and left the adminbot chatroom '''
class Record():
    
    def login(self, user, time):
        #Record login time
        f = open(user,'a')
        f.write('Login: ' + time.strftime('%d/%m/%Y %H:%M') + '\n')
        f.close()   
        return  
    
    def logout(self, user, time):
        #Record logout time
        f = open(user,'a')
        f.write('Logout: ' + time.strftime('%d/%m/%Y %H:%M') + '\n')
        f.close()
        return 
    
    def checkLate(self, user, time):
        with open(user.lower() + 'schedule.txt','r') as scheduleFile:
                    # read a list of lines into data
                    fileContents = scheduleFile.readlines()
                    dayOfTheWeek = time.weekday()
                    
                    todaysSchedule = fileContents[dayOfTheWeek].split()
                    
                    # check to make sure a schedule exists for the current day
                    if len(todaysSchedule) < 2:
                        return
                    
                    startTime = todaysSchedule[1].split(':')
                    hourDifference = time.hour - int(startTime[0])
                    minuteDifference = time.minute - int(startTime[1])
                    
                    return [hourDifference, minuteDifference]
                
         

class ScheduleHandler():
            
    def schedule(self, bot, params, event):
        action = params[0].upper()
        currentDay = params[2].upper()
        
        if action == 'ADD':
            
            # check syntax of time parameters
            timeFormat = re.compile(r'[0-2][0-9]\:[0-5][0-9]')
            #startTime = currentDay + 1
            #endTime = currentDay + 2
            if timeFormat.match(params[3]) is None:
                bot.send_message(event.source, 'Incorrect start time format')
            if timeFormat.match(params[4]) is None:
                bot.send_message(event.source, 'Incorrect end time format')
            
            
            try:
                with open(params[1].lower() + 'schedule.txt','r') as scheduleFile:
                    # read a list of lines into data
                    fileContents = scheduleFile.readlines()
                    
                    # find correct line in file  
                    for i in xrange(len(fileContents)):   
                    #for line in fileContents:
                        if currentDay in fileContents[i]:
                            fileContents[i] = currentDay + ' ' + params[3] + ' ' + params[4] + '\n'
                            #print fileContents[i]
                            
                            
                    # and write everything back
                with open(params[1].lower() + 'schedule.txt', 'w') as scheduleFile:
                    #print fileContents
                    scheduleFile.writelines( fileContents )
                    
            # file does not exist - create it
            except IOError:
                days = ['MONDAY\n', 'TUESDAY\n', 'WEDNESDAY\n', 'THURSDAY\n', 'FRIDAY\n', 'SATURDAY\n', 'SUNDAY']
                with open(params[1] + 'schedule.txt', 'w') as scheduleFile:
                    scheduleFile.writelines(days)








''' This class handles private message commands to add a user, delete a user and show users
        currently logged into the irc channel '''
class UserManager():
    
    def addUser(self, bot, params, nick):
        for item in params:
            if item in userList:
                bot.send_message(nick, item + ' is already in user list!')
                
            else:
                userList.append(item.rstrip())
                bot.send_message(nick, item + ' was added to list!')   
        
        update_list(userList)
        return 
    
    ''' @param nick - name of user who sent the private message
        @param params - list of users to delete '''
    def deleteUser(self, bot, params, nick):
        
        # error checking - for testing purposes
        # check to see user's nickname is a string. If not, raise a TypeError
        if not isinstance(nick, str):
            raise TypeError
        
        for item in params:
            if item in userList:
                userList.remove(item)
                bot.send_message(nick, item + ' was removed from the list!')
                
            else:
                bot.send_message(nick, item + ' was not even in the list!')
        
        update_list(userList)
        return 
    
    
    
    def showUsers(self, bot, nick):
        bot.send_message(nick, 'Users currently logged in:')
        print 'Users currently logged in\n'
            
        for user in activeUsers:
            bot.send_message(nick, user)
            print user
        
    



   
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
            ScheduleHandler().schedule(self, params, event)
            



if __name__ == "__main__":
    # Create an instance of the bot
    # We set the bot's nickname here
    adminBot = AdminBot( adminBotName )
    
    # Let's connect to the host
    adminBot.connect(adminBotServer, channel=[ adminBotChannel ])

    # Start running the bot
    adminBot.start()
