from main import UserManager, AdminBot
import unittest

class UserManagerTestCase(unittest.TestCase):
    
    # initialize the user manager class and other test variables
    def setUp(self):
        self.userManager = UserManager()
        self.adminbot = AdminBot("admin_bot")
        self.userList = ['James', 'Maya', 'Fred']
    
    # test to see if a TypeError is throw when the us   
    def test_deleteUser_raises_TypeError_if_nick_is_an_int(self):
        self.assertRaises(TypeError, self.userManager.deleteUser, self.adminbot, self.userList, 7)
    
    # to be done later
    def test_search_returns_negative_one_when_user_not_in_list(self):
        pass
    
    # more tests to be added
    
    
    
    
    
    
    
# run the tests
suite = unittest.TestLoader().loadTestsFromTestCase(UserManagerTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)