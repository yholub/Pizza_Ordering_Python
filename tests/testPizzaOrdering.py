#!/usr/bin/python
import unittest
import os
import shutil
import sqlline3

TEST_DB = 'test.db'


class TestPizzaOrdering(unittest.TestCase):

	# executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        db = SQLAlchemy(app)
        app.config['db'] = db

            
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass

	#check ingredients
	def test_ingredients(self):

		connection = sqlline3.connect(TEST_DB)
		comm = """
		CREATE TABLE ingredients {
		Id BIGINTEGER PRIMARY KEY,
		Name VARCHAR(20),
		Price Numeric(18, 2),
		Weight Float(53)
		"""
		cursor.execute(comm)

		sql_command = """INSERT INTO ingredients (Id, Name, Price, Weight)
		    VALUES (1, "Фета", 25.0, 100);"""
		cursor.execute(sql_command)


		sql_command = """INSERT INTO ingredients (Id, Name, Price, Weight)
		    VALUES (1, "Фета", 25.0, 100);"""
		cursor.execute(sql_command)

		# never forget this, if you want the changes to be saved:
		connection.commit()

		connection.close()

		cursor.execute(sql_command)

		cursor.execute("SELECT name, age FROM person")

		for row in cursor.fetchone():


suite = unittest.TestLoader().loadTestsFromTestCase(TestPizzaOrderings)
unittest.TextTestRunner(verbosity=2).run(suite)