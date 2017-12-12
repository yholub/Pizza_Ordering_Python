import os
import unittest
import shutil
from app import *
from models import *

TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):

    app = __import__("app")
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://(localdb)\\v11.0/Pizza_OrderingTest?driver=SQL+Server+Native+Client+11.0?trusted_connection=yes'
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        db = SQLAlchemy(app, metadata=metadata)
        app.config['db'] = db
  
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        ing = Ingredient()
        ing.Name = "Сир"
        ing.Price = 10
        ing.Weight = 5
        db.session.add(ing)
        db.session.commit()

    def test_main_page(self):
	    response = self.app.get('/', follow_redirects=True)
	    self.assertEqual(response.status_code, 200)

    def test_pizza_ordering(self):
        response = self.app.get('/api/ingredients', follow_redirects=True)
        data = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['Name'], "Сир")


suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
unittest.TextTestRunner(verbosity=2).run(suite)