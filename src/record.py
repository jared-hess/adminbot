#Record Class (records times)
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
        try:
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
        
        except IOError:
            return

    def checkAbssent(self, time, userList, activeUsers, absentUsers):
        missingUsers = list( (set(userList) - set(activeUsers)) - set(absentUsers))   #users who aren't in chat and aren't abset yet
        for user in missingUsers: #For every user that isn't here
            with open(user.lower() + 'schedule.txt','r') as scheduleFile: #Check schedule
                fileContents = scheduleFile.readlines()
                dayOfTheWeek = time.weekday()
                    
                todaysSchedule = fileContents[dayOfTheWeek].split()
                startTime = todaysSchedule[1].split(':')
                hourDifference = time.hour - int(startTime[0])
                minuteDifference = time.minute - int(startTime[1])
                
                if (hourDifference > 4): #if more than 4 hours late
                    absentUsers.append(user) #count as absent