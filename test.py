import os
import unittest
import shutil
from app import *
 
class BasicTests(unittest.TestCase):

    app = __import__("app")

    def test_main_page(self):
	    response = self.app.get('/', follow_redirects=True)
	    self.assertEqual(response.status_code, 200)


suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
unittest.TextTestRunner(verbosity=2).run(suite)