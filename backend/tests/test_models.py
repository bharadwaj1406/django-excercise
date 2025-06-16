from django.test import TestCase
from backend.models import Country
from django.contrib.auth.hashers import check_password, make_password

class CountryModelTest(TestCase):
    def test_country_creation(self):
        country = Country.objects.create(
            name="Test Country",
            country_code="TC",
            currency_symbol="$",
            phone_code="+1"
        )
        self.assertEqual(country.name, "Test Country")
        self.assertEqual(country.country_code, "TC")
        self.assertEqual(country.currency_symbol, "$")
        self.assertEqual(country.phone_code, "+1")
        
        # country.delete()
    
    
class UserModelTest(TestCase):
    def test_user_creation(self):
        from backend.models import User
        user = User.objects.create(
            username="testuser@example.com",
            # password="testpassword" # Password should be set via save or serializer to be hashed
        )
        # Set password using the model's set_password method or ensure your serializer handles it
        # For direct model creation and testing, it's better to simulate how it's done in views/serializers
        # However, if User.objects.create is used directly, password won't be hashed automatically
        # unless User model's save method is overridden or a signal is used.
        # Assuming password hashing is handled by the serializer or a custom save method not shown here.
        # For this test, let's assume the serializer's behavior:
        user.password = make_password("testpassword")
        user.save()

        self.assertEqual(user.username, "testuser@example.com")
        self.assertTrue(check_password("testpassword", user.password))

        # user.delete()


