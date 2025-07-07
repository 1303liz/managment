from django.test import TestCase, Client
from django.urls import reverse
from .models import CustomUser, Profile

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@example.com', username='testuser', password='testpass123')

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.user_type, 'user')

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='profile@example.com', username='profileuser', password='testpass123')
        self.profile = Profile.objects.create(user=self.user, bio='Test bio')

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'profileuser')
        self.assertEqual(self.profile.bio, 'Test bio')

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_registration_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration(self):
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())
