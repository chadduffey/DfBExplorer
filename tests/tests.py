import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		user1 = User(password = 'phone')
		self.assertTrue(user1.password_hash is not None)

	def test_no_password_getter(self):
		user1 = User(password = 'phone')
		with self.assertRaises(AttributeError):
			user1.password

	def test_password_verification(self):
		user1 = User(password = 'chicken')
		self.assertTrue(user1.verify_password('chicken'))
		self.assertFalse(user1.verify_password('toad'))

	def test_salts_are_random(self):
		user1 = User(password='bone')
		user2 = User(password='bone')
		self.assertTrue(user1.password_hash != user2.password_hash)