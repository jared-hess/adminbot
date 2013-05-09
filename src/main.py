#Utility/Framework Imports
from ircutils import bot
#import dokuwikixml
from record import *
from usermanager import *
from schedulehandler import *
import config

#Global Vars
userList = []   #List of the users
activeUsers = [] #list of all users currently logged into the channel
absentUsers = []#list of users who are more than 4 hours late

bufsize = 0
userFile = open('userlist.txt', 'r')
userList = userFile.readlines()

#Get rid of new lines
userList = map(lambda s: s.strip(), userList)


def updateList(newList):
    userFile = open('userlist.txt', 'w', bufsize)
    for item in newList:
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
    
    def getAdministrators(self):
        try:
            # open the file with name of administrators
            adminFile = open('admin.txt', 'r')
            administrators = adminFile.readlines()
            administrators = map(lambda s: s.strip(), administrators)

            return administrators
        
        except IOError as err:
            print err
            #self.send_message(nick, adminBotName + ' has encountered some errors. Please try again!')
            return False
        
        finally:
            if adminFile is not None:
                adminFile.close()
    
    
    def checkAuthentication(self, nick):
        try:
            administrators = self.getAdministrators()
              
            # check if the user is listed as an administrator
            if nick not in administrators:
                raise AuthenticationError("Not an admin")
            else:
                return True
    
       
        except AuthenticationError as err:
            print err
            return False
            
        
    
    #Gets called when a user joins the chat
    def on_join(self, event):
        #Passes user and login time to be recorded
        if event.source != self.nickname:
            self.send_message(event.target, "Welcome, " + event.source + "!")
            Record().login(event.source, datetime.now())
        
            timeLate = Record().checkLate(event.source, datetime.now())
            if timeLate == None:
                for admin in self.getAdministrators():
                        self.send_message(admin, event.source + " is not scheduled to work today")
            elif timeLate[0] > -1:
                if timeLate[1] > -1:
                    # employee is late, send message to all admins
                    sendString = event.source + " is late by " + str(timeLate[0]) + " hours and " + str(timeLate[1]) + " minutes"
                    for admin in self.getAdministrators():
                        self.send_message(admin, sendString)
        
        
        # once a user joins the chat, add user name to the activeUser list
        activeUsers.append(event.source)
        # sort the list
        activeUsers.sort(key=str.lower)
        return
    
    #Gets called when a user leaves chat
    def on_quit(self, event):
        #Passes user and logout time to be recorded
        Record().logout(event.source, datetime.now())
        # search for the user name to delete from the list once the user leaves the chat
        index = search(activeUsers, event.source)
        del activeUsers[index]
        return
    
    def on_part(self, event):
        self.on_quit(event)
        return
    
    #Defines how to handle private messages sent to the admin bot
    def on_private_message(self, event):
        msg = event.message.split()
        
        cmd = msg[0].upper()
        params = msg[1:]
        
        if not self.checkAuthentication(event.source):
            self.send_message(event.source, 'You are not authorized to change the pay period')
            return
        
        #Add user command
        if cmd == 'ADDUSER':
            UserManager().addUser(self, params, event.source, userList)

        #Delete user command
        elif cmd == 'DELETEUSER':
            UserManager().deleteUser(self, params, event.source, userList)
        
        # command to display all users currently logged into the channel
        elif cmd == 'SHOWUSERS':
            UserManager().showUsers(self, event.source, activeUsers)
            
        # command to display all users currently logged into the channel
        elif cmd == 'SCHEDULE':
            if msg[1].upper() == 'ADD':
                ScheduleHandler().addSchedule(self, params, event.source)
            if msg[1].upper() == 'REMOVE':
                ScheduleHandler().removeSchedule(self, params, event.source)
            
        elif cmd == 'CHANGEPERIODENDDATE':
            ScheduleHandler().changePayPeriod(self, params, event.source)
        
        # if command is invalid, send error message and throw an exception
        else:
            pass
            



if __name__ == "__main__":
    # Create an instance of the bot
    # We set the bot's nickname here
    adminBot = AdminBot( config.adminBotName )
    
    # Let's connect to the host
    adminBot.connect(config.adminBotServer, channel=[ config.adminBotChannel ])

    # Start running the bot
    adminBot.start()

