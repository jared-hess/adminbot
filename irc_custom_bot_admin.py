# This program creates an IRC bot which joins a single channel where it monitors users log in and log out times and records them in a wiki database.
# The wiki used in this project is a dokuwiki and it uses the XML RPC to access pages of the wiki


import getpass
import time
from ircutils import bot, format
import dokuwikixmlrpc


joinDict = {}	#global var, a dictionary containing the last join time of users
msgQ = []		#global var, a queue containing the last 5 messages received in the channel the bot resides in

wikiURL = "http://wiki.parc.com/"  	#URL for your Wiki
userListPath = "user_list"			#URL where you store the user list on the wiki
userList = []						#global var, stores the user list in a Python list

adminBotChannel = "#test"			#IRC Channel you want the Admin Bot to join
adminBotName = "admin_bot"			#IRC Bot Name
adminBotServer = "talk.parc.com"	#IRC Server 


#AdminWiki adds calls to other dokuwiki functions provided by the dokuwiki XML RPC.  We can apparently call them, but I'm not sure where they are!
class AdminWiki(dokuwikixmlrpc.DokuWikiClient):

    def _dokuwiki_time(self):
        """Returns the current time at the remote wiki server as Unix timestamp"""
        try:
            return self._xmlrpc.dokuwiki.getTime() #don't know where this lives...
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

    def appendPage(self, page_id, text, summary='', minor=False):
        """Appends text to a Wiki Page."""
        try:
            params = {}
            params['sum'] = summary
            params['minor'] = minor

            self._xmlrpc.dokuwiki.appendPage(page_id, text, params) #don't know where this lives...
        except xmlrpclib.Fault, fault:
            raise DokuWikiXMLRPCError(fault)

			
#Get the current username and silently ask for the user's password
un = getpass.getuser()
pw = getpass.getpass(un + "'s Wiki Password: ")


#Use the above credentials to log on to our Wiki and retrieve the user_list page which contains a comma-separated list of users the admin bot works with
#This is the only time we read the list (script start / initialization) from the wiki.  We modify this page as the bot is instructed by astanton
adminWiki = AdminWiki(wikiURL, un, pw, False)
userList = adminWiki.page( userListPath ).split(',')


#A function to update the list to the wiki
def update_list(new_list):
        listStr = ''
        for item in new_list:
                listStr = listStr + item + ','
        adminWiki.put_page(userListPath, listStr, '', False)

		
#User input to initialize the admin bot so that it is aware of the current payroll period
while True:
	try:	
		payrollStart = time.strptime(raw_input("What is the next payroll period starting date (Sunday)?\nEnter as MO/DA/YR\n"), "%m/%d/%y")
		if time.strftime('%w', payrollStart) == '0':
			break
		else:
			print "Try Again. Date is not a Sunday."
	except ValueError:
		print "Try Again. Invalid format or date."
#Use the payroll start to calculate payroll end 	
payrollEnd = time.localtime( int(time.mktime(payrollStart))	+ (60 * 60 * 24 * 13) ) #add 13 days

# This function is called by method(s) in the class AdminBot and essentially checks the status of the wiki pages for a single user
# It returns the page the bot should use to update the user's time recording, etc.  It also fills pages with necessary static information
weekTransitioned = False
def admin_checks_for_user(user):
	global weekTransitioned
	global payrollStart
	global payrollEnd

	thePage = user + time.strftime("_%m_%d_%y", payrollStart)

	#Check for Payroll Period Update
	if not (payrollStart.tm_yday <= time.localtime().tm_yday <= payrollEnd.tm_yday):
		payrollStart = time.localtime( int(time.mktime(payrollStart))	+ (60 * 60 * 24 * 14) ) #add 14 (recalc payroll dates)
		payrollEnd = time.localtime( int(time.mktime(payrollStart))	+ (60 * 60 * 24 * 14) ) #add 14
		#insert finish touches to current wiki page
		thePage = user + time.strftime("_%m_%d_%y", payrollStart)
		weekTransitioned = False
	
	
	theUserPage = adminWiki.page(user)
	if not theUserPage:
		firstLink = 
	
		#Finalize current period and initialize next
		print 'sAME payroll'
		
		#Check for Week1 end / Week2 start
		if (time.localtime().tm_yday - payrollStart.tm_yday) >= 7:
			firstDaySecondWeek = time.localtime( int(time.mktime(payrollStart))	+ (60 * 60 * 24 * 7) )
			check_append_blank_days_to_wiki(thePage, firstDaySecondWeek) #need to limit
			#insert finish touches to first week
			weekTransitioned = True
		
		check_append_blank_days_to_wiki(thePage)
	#Return the page that needs to be updated
	return thePage

def check_append_blank_days_to_wiki(link, today=time.localtime() ):
	pageTxt = adminWiki.page( link )
	#process string to find last line
	
	#cut off last line at 3rd pipe --> "| %a | %b %d |" --> store in (partLastLine)
	#perhaps ensure it has the data in it... and forget having to try/except.  
	#What if we're looking at a line we already added or the last line does not have a time entered.  This is possible!
	#This fn will be called twice at the start of the second week, etc.
	try: lastRecordedDate = time.strptime(partLastLine, "| %a | %b %d |")
	except ValueError: #handler
		pass

	if lastRecordedDate.tm_yday < (today.tm_yday-1):
		#fill in blank dates!


#AdminBot is a customized IRC bot that listens for certain behaviors in an IRC channel and can respond to commands given by administrator
#The "administrator" is currently hardcoded as "astanton" username				
			
class AdminBot(bot.SimpleBot):

    def on_channel_message(self, event):
        # The target of the event was the channel itself, and since we want
        # to send a message to the same channel, we use the same target.
        #self.send_message(event.target, event.message)

        #Channel Message History Queue
        global msgQ
        msgQ.insert(0, [event.target, event.source, event.message, time.asctime()] )
        if len(msgQ) > 5:
            msgQ.pop()

    def on_join(self, event):
        #Admin Bot Recording
        if event.source in userList:
                timeInt = int(time.time())

				currentPgStr = admin_checks_for_user(event.source)
				
                currentPgTxt = adminWiki.page( currentPgStr )
                
				appendTxt = ''
                if not currentPg.endswith('\n'):
                        appendTxt = '\n'
                appendTxt = appendTxt + time.strftime("| %a | %b %d | %I:%M %p | ", time.localtime(timeInt) )
                adminWiki.appendPage(event.source, appendTxt, '', False)
                global joinDict
                joinDict[event.source] = timeInt
        #Admin Bot Greeting
        if msgQ != []:
                self.send_message(event.source, 'Here are the last 5 messages in ' + event.target + '!  Enjoy!')

                for item in reversed(msgQ):
                        test = []
                        test.append(format.color(item[0], format.GREEN))
                        test.append(format.color(item[1], format.RED))
                        test.append(format.color(': '+item[2], format.NAVY_BLUE))
                        test.append(format.color(item[3], format.PURPLE))
                        self.send_message(event.source, 'In channel ' + test[0] + ' ' + test[1] + ' said' + test[2] + ' @ ' + test[3])
        else:
                self.send_message(event.source, 'There are no previous messages in ' + event.target + '.')
				
        self.send_message(event.source, 'Thank you!')				
				
    def on_private_message(self, event):

        msg = event.message.split()
        cmd = msg[0].upper()
        params = msg[1:]

        if event.source == 'astanton':
                if cmd == '.ADDUSERS':
                        for item in params:
                                if item in userList:
                                        self.send_message(event.source, item + 'is already in user list!')
                                else:
                                        userList.append(item)
                                        self.send_message(event.source, item + 'was added to list!')
                                update_list(userList)
                elif cmd == '.DELUSERS':
                        for item in params:
                                if item in userList:
                                        userList.remove(item)
                                        self.send_message(event.source, item + 'was removed from the list!')
                                else:
                                        self.send_message(event.source, item + 'was not even in the list!')
                                update_list(userList)
								
                elif cmd == '.PRINTUSERS':
                        self.send_message(event.source, "See http://wiki.parc.com/admin_list for user list")
                        admin_list_page = adminWiki.page("admin_list")
                        self.send_message(event.source, admin_list_page)

                elif cmd == '.INFO':
                        self.send_message(event.source, '.ADDUSERS - adds users to the list of known users the admin bot is aware of')
                        self.send_message(event.source, '.DELUSERS - deletes users in the list of known users')
						self.send_message(event.source, '.PRINTUSERS - prints users in the list of known users')
                        self.send_message(event.source, '.INFO - does what it just did...')

    def on_part(self, event):

        #Admin Bot Record Quit
        if event.source in userList:
                timeInt = int(time.time())
                tdiff = timeInt - joinDict[event.source]
                sec = tdiff
                hour = sec / 3600
                sec_left = sec - (hour * 3600)
                min_left = sec_left / 60
                hour_part = '.00'

                if min_left >= 53:
                        hour = hour + 1
                elif min_left >= 38:
                        hour_part = '.75'
                elif min_left >= 23:
                        hour_part = '.50'
                elif min_left >= 8:
                        hour_part = '.25'

				appendTxt = time.strftime("%I:%M %p | ", time.localtime(timeInt) ) + str(hour) + hour_part + ' |\n'
                adminWiki.appendPage(event.source, appendTxt, '', False)

    def on_quit(self, event):
        on_part(self, event)		#This doesn't work... How to do this?  I want the same procedure to happen for quit as part (above)


if __name__ == "__main__":
    # Create an instance of the bot
    # We set the bot's nickname here
    adminBot = AdminBot( adminBotName )

    # Let's connect to the host
    adminBot.connect(adminBotServer, channel=[ adminBotChannel ])

    # Start running the bot
    adminBot.start()
