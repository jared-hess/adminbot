''' This class handles private message commands to add a user, delete a user and show users
        currently logged into the irc channel '''
class UserManager():
    
    
    def update_list(self, new_list):
        bufsize = 0
        userFile = open('userlist.txt', 'w', bufsize)
        for item in new_list:
            userFile.write(item + '\n')
        userFile.close()
    
    
    def addUser(self, bot, params, nick, userList):
        for item in params:
            if item in userList:
                bot.send_message(nick, item + ' is already in user list!')
                
            else:
                userList.append(item.rstrip())
                bot.send_message(nick, item + ' was added to list!')   
        
        self.update_list(userList)
        return 
    
    ''' @param nick - name of user who sent the private message
        @param params - list of users to delete '''
    def deleteUser(self, bot, params, nick, userList):
        
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
        
        self.update_list(userList)
        return 
    
    
    
    def showUsers(self, bot, nick, activeUsers):
        bot.send_message(nick, 'Users currently logged in:')
        print 'Users currently logged in\n'
            
        for user in activeUsers:
            bot.send_message(nick, user)
            print user