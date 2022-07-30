from django.test import TestCase
from .models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
# Create your tests here.
class UserModelTestCase(TestCase):
    def create_user(self, username="Test", email="test@onet.pl", password="testpassword123"):
        return User.objects.create_user(username=username, email=email, password=password)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.username)
    
class UserViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username="Filip",email="filip@onet.pl", password="test123123!")
        user1.is_active = True 
        user1.save()

        user2= User.objects.create_user(username="Jan",email="jan@onet.pl", password="test123123!")
        user2.is_active = True 
        user2.save()


    def create_user(self, username="John", email="hhaha@onett.pl", password="testpasssword123"):
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True 
        user.save()

    def api_client(self):
        user = User.objects.all().get(id=1)
        client = APIClient() 
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client
    
    def test_get_user_view(self):
        client = self.api_client()
        response = client.get("/auth/get-user/Filip")
        self.assertEqual(response.status_code,200)

    def test_follow_user(self):
        client = self.api_client()
        response = client.post("/auth/follow-action/",{"username":"Jan"})
        self.assertEqual(response.status_code, 200)
        user2 = User.objects.all().get(id=2)
        self.assertEqual(user2.followed.count(), 1)

    

    def test_registration_view(self):
        response = self.client.post("/auth/registration/"
        ,{"username":"Jack","email":"jack@com.pl","password":"passwordtest123" })
        self.assertEqual(response.status_code, 201)
        user = User.objects.all().get(username="Jack")
        self.assertEqual(user.email, "jack@com.pl")
        self.assertEqual(user.is_active, False)

    def test_login_view(self):
        self.create_user()
        response = self.client.post("/auth/token/"
        ,{"username":"John","password":"testpasssword123" })
        self.assertEqual(response.status_code, 200)