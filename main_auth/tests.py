from django.test import TestCase
from .models import User

# Create your tests here.
class UserModelTestCase(TestCase):
    def create_user(self, username="Test", email="test@onet.pl", password="testpassword123"):
        return User.objects.create_user(username=username, email=email, password=password)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)