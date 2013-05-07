from main import UserManager, AdminBot, ScheduleHandler
import unittest

class UserManagerTestCase(unittest.TestCase):
    
    # initialize the user manager class and other test variables
    def setUp(self):
        self.userManager = UserManager()
        self.adminbot = AdminBot("admin_bot")
        self.userList = ['James', 'Maya', 'Fred']
        self.schedule = ScheduleHandler()
    
    # test to see if a TypeError is throw when the us   
    def test_deleteUser_raises_TypeError_if_nick_is_an_int(self):
        self.assertRaises(TypeError, self.userManager.deleteUser, self.adminbot, self.userList, 7)
    
    def test_changePayPeriod_raises_SyntaxError_if_Date_is_not_in_the_correct_format(self):
        pass
    
    def test_changePayPeriod_raises_ValueError_if__day_is_greater_than_31(self):
        pass
    
    def test_changePayPeriod_raises_ValueError_if_month_is_greater_than_12(self):
        pass
    
    def test_changePayPeriod_raises_ValueError_if_year_is_less_than_2013(self):
        pass
    
    def test_changePayPeriod_returns_True_if_user_is_authorized_date_format_is_correct_date_is_valid(self):
        pass
    
    
    
    
    
    
    
    
    
    
    
# run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(UserManagerTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)