import os
import unittest
import shutil
from app import *
from models import *
import datetime
TEST_DB = 'test.db'
def getJson(response):
    return json.loads(response.data.decode("utf-8"))

def dbInit(db):
    db.drop_all()
    db.create_all()

    initUsers(db)
   
    address = Address()

houseId = 0
acceptedOrderId = 0
pendingOrderId = 0

def initUsers(db):
    #add moderator user
    modUser = User(Id = 1)
    modUser.Name = "modPython"
    modUser.UserName = "modPython"
    modUser.PasswordHash = "123456"
    modUser.Email="modPython@g"
    modUser.EmailConfirmed = True
    modUser.PhoneNumberConfirmed = True
    modUser.SecurityStamp = "security"
    modUser.TwoFactorEnabled = False
    modUser.LockoutEnabled = False
    modUser.AccessFailedCount = 0
    role = Role(Name = "Moderator")
    db.session.add(modUser)
    db.session.add(role)
    db.session.commit()
    modRole = UserRole(UserId = modUser.Id, RoleId = role.Id)
    db.session.add(modRole)
    db.session.commit()

    #add moderator user
    user = User(Id = 2)
    user.Name = "userPython"
    user.UserName = "userPython"
    user.PasswordHash = "123456"
    user.Email="userPython@g"
    user.EmailConfirmed = True
    user.PhoneNumberConfirmed = True
    user.SecurityStamp = "security"
    user.TwoFactorEnabled = False
    user.LockoutEnabled = False
    user.AccessFailedCount = 0
    db.session.add(user)
    db.session.commit()

    ing = Ingredient()
    ing.Name = "Сир"
    ing.Price = 10
    ing.Weight = 5
    db.session.add(ing)
    db.session.commit()

    fix_pizza = FixPizza(Name = "Маргарита", Price = 55)
    db.session.add(fix_pizza)
    db.session.commit()

    address = Address(City = "Львів", District = "13", Street = "Левицького", HouseNumber = "13", Lng = 13.5, Lat = 5.4)
    db.session.add(address)
    db.session.commit()

    house = PizzaHouse(AddressId = address.Id, OpenTime = datetime.time(9, 0, 0), CloseTime = datetime.time(22, 0 ,0), ModeratorId = modUser.Id, Capacity = 2)
    db.session.add(house)
    db.session.commit()
    houseId = house.Id

    ingAm = IngredientAmount(IngredientId = ing.Id, PizzaHouseId = house.Id, Quantity = 1)
    ingItem = IngredientItem(IngredientId = ing.Id, FixPizza_Id = fix_pizza.Id, Quantity = 1)
    db.session.add(ingAm)
    db.session.add(ingItem)
    db.session.commit()
    time = datetime.datetime.today() + datetime.timedelta(hours = 7)
    order = Order(Id = 1, Price = 55, PizzaHouseId = house.Id, Status = 0, TimeToTake = time)
    order2 = Order(Id = 2, Price = 55, PizzaHouseId = house.Id, Status = 1, TimeToTake = time)
    db.session.add(order)
    db.session.add(order2)
    db.session.commit()
    acceptedOrderId = order2.Id
    pendingOrderId = order.Id

    orderItem = OrderItem(PizzaId = fix_pizza.Id, \
                            OrderId = order.Id, \
                            Price = 55, \
                            EndTime = time, \
                            StartTime = time - datetime.timedelta(hours = 1),\
                            IsModified = False)

    orderItem2 = OrderItem(PizzaId = fix_pizza.Id, \
                            OrderId = order2.Id, \
                            Price = 55, \
                            EndTime = time, \
                            StartTime = time - datetime.timedelta(hours = 1),\
                            IsModified = False)
    db.session.add(orderItem)
    db.session.add(orderItem2)
    db.session.commit()

class BasicTests(unittest.TestCase):

    app = __import__("app")
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://(localdb)\\v11.0/Pizza_OrderingTest?driver=SQL+Server+Native+Client+11.0?trusted_connection=yes'
        db = SQLAlchemy(app, metadata=metadata)
        app.config['db'] = db
        dbInit(db)
        self.app = app.test_client()
        

    def test_main_page(self):
	    response = self.app.get('/', follow_redirects=True)
	    self.assertEqual(response.status_code, 200)

    def test_pizza_ordering(self):
        response = self.app.get('/api/ingredients', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = getJson(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['Name'], "Сир")

    def test_correct_user_login(self):
        response = self.app.post('/api/Account/Login', data={'userName' : 'userPython@g', 'password': '123456'})
        self.assertEqual(response.status_code, 200)
        data = getJson(response)
        self.assertIn('status', data)
        self.assertNotIn('redirect_url', data)
        self.assertEqual(data['status'], 'success')

    def test_correct_moderator_login(self):
        response = self.app.post('/api/Account/Login', data={'userName' : 'modPython@g', 'password': '123456'})
        self.assertEqual(response.status_code, 200)
        data = getJson(response)
        self.assertIn('status', data)
        self.assertIn('redirect_url', data)
        self.assertEqual(data['status'], 'success')

    def test_incorrect_login(self):
        response = self.app.post('/api/Account/Login', data={'userName' : 'modPython@g', 'password': '1233456'})
        self.assertEqual(response.status_code, 400)
    
    def test_registration(self):
        response = self.app.post('/api/Account/Register', data={'name' : 'testUser', 'password': '111111', 'email' : 'testUser@g'})
        self.assertEqual(response.status_code, 200)
        user = db.session\
            .query(User)\
            .filter(sqlalchemy.and_(User.UserName == 'testUser',\
                User.Email == 'testUser@g',\
                User.PasswordHash == '111111'))\
            .first()

        self.assertIsNotNone(user)

    def test_get_all_items(self):
        response = self.app.get('/api/Order/GetCurrent')
        self.assertEqual(response.status_code, 200)
        data = getJson(response)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["Price"], 55)

    def test_get_new_items(self):
        response = self.app.get('/api/Order/GetNew')
        self.assertEqual(response.status_code, 200)
        data = getJson(response)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["Price"], 55)
    
    def test_accept_order(self):
        response = self.app.post('/api/order/accept/%d' % 1)
        self.assertEqual(response.status_code, 200)
        ord = db.session.query(Order).filter(Order.Id == 1).first()
        self.assertEqual(ord.Status, 1)

    def test_reject_order(self):
        response = self.app.post('/api/order/reject/%d' % 1)
        self.assertEqual(response.status_code, 200)
        ord = db.session.query(Order).filter(Order.Id == 1).first()
        self.assertEqual(ord.Status, 4)
        response = self.app.post('/api/order/accept/%d' % 1)
        ord = db.session.query(Order).filter(Order.Id == 1).first()
        self.assertEqual(ord.Status, 4)
    
        

    

suite = unittest.TestLoader().loadTestsFromTestCase(BasicTests)
unittest.TextTestRunner(verbosity=2).run(suite)


