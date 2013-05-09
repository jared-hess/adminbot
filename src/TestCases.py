from usermanager import *
from schedulehandler import ScheduleHandler
from authenticationerror import AuthenticationError
from main import AdminBot
import config
import unittest

class BotTestCase(unittest.TestCase):
    
    # initialize the user manager class and other test variables
    def setUp(self):
        self.userManager = UserManager()
        self.adminbot = AdminBot(config.adminBotName)
        self.userList = ['James', 'Maya', 'Fred']
        self.schedule = ScheduleHandler()
    
    # test to see if a TypeError is throw when the nickname is not a string   
    def test_deleteUser_raises_TypeError_if_nick_is_an_int(self):
        self.assertRaises(TypeError, self.userManager.deleteUser, self.adminbot, self.userList, 7)
    
    def test_changePayPeriod_raises_AuthenticationError_if_user_not_authorized(self):
        self.assertRaises(AuthenticationError, self.schedule.changePayPeriod, self.adminbot, '05/05/13', 'Steve')
        
    def test_changePayPeriod_raises_SyntaxError_if_Date_is_not_in_the_correct_format_but_user_is_authorized(self):
        self.assertRaises(SyntaxError, self.schedule.changePayPeriod, self.adminbot, '07\08\13', 'Ife')
    
    def test_changePayPeriod_raises_ValueError_date_is_in_correct_format_but_day_is_greater_than_31(self):
        self.assertRaises(ValueError, self.schedule.changePayPeriod, self.adminbot, '05/56/13', 'Ife')
    
    def test_changePayPeriod_raises_ValueError_if_date_is_in_correct_format_but_month_is_greater_than_12(self):
        self.assertRaises(ValueError, self.schedule.changePayPeriod, self.adminbot, '34/24/13', 'Taylor')
    
    def test_changePayPeriod_raises_ValueError_if_date_is_less_than_todays_date(self):
        self.assertRaises(ValueError, self.schedule.changePayPeriod, self.adminbot, '05/09/12', 'Ife')
    
    def test_changePayPeriod_returns_True_if_user_is_authorized_date_format_is_correct_date_is_valid(self):
        self.assertTrue(self.schedule.changePayPeriod(self.adminbot, '07/14/15', 'Jared'))
    
    
# run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(BotTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
