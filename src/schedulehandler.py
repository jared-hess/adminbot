import re

class ScheduleHandler():
            
    def addSchedule(self, bot, params, event):
        #action = params[0].upper()
        currentDay = params[2].upper()
        
        #if action == 'ADD':
            
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
            ScheduleHandler.addSchedule(bot, params, event)
        
        
        
    def removeSchedule(self, bot, params, event):
        #action = params[0].upper()
        currentDay = params[2].upper()
        try:
            with open(params[1].lower() + 'schedule.txt','r') as scheduleFile:
                # read a list of lines into data
                fileContents = scheduleFile.readlines()
                    
                # find correct line in file  
                for i in xrange(len(fileContents)):   
                #for line in fileContents:
                    if currentDay in fileContents[i]:
                        fileContents[i] = currentDay + '\n'

                with open(params[1].lower() + 'schedule.txt', 'w') as scheduleFile:
                    #print fileContents
                    scheduleFile.writelines( fileContents )
                    
        # file does not exist - create it
        except IOError:
            return
