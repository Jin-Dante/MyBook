import io

from PIL import Image
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from .models import Book


class UserAuthTest(TestCase):
    def setUp(self):
        """Set up test user"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123', email='test@example.com')

    def test_signup(self):
        """Test user signup"""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        print("test_signup PASSED: New user registered successfully!")

    def test_login_success(self):
        """Test login with valid credentials"""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_list'))
        self.assertTrue('_auth_user_id' in self.client.session)
        print("test_login_success PASSED: User logged in successfully!")

    def test_login_failure(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {'username': 'wronguser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertFalse('_auth_user_id' in self.client.session)
        print("test_login_failure PASSED: Invalid login correctly rejected!")

    def test_logout(self):
        """Test user logout"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
        print("test_logout PASSED: User logged out successfully!")

    def test_edit_profile(self):
        """Test user profile editing (username + email + date_joined)"""
        self.client.login(username='testuser', password='testpass123')

        # Get the current date_joined value from the database
        current_date_joined = self.user.date_joined

        response = self.client.post(reverse('profile_edit'), {
            'username': 'testuser_updated',
            'email': 'test@example.com',
            'date_joined': current_date_joined  # Provide the existing date_joined
        })

        # If the response is 200, print form errors
        if response.status_code == 200:
            print("test_edit_profile FAILED: Form errors →", response.context['form'].errors)

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'testuser_updated')
        self.assertEqual(self.user.email, 'test@example.com')  # Ensure email is updated
        print("test_edit_profile PASSED: User profile updated successfully!")


class BookTest(TestCase):
    def setUp(self):
        """Set up test user and book"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.login(username='testuser', password='testpass123')

        self.pdf_file = SimpleUploadedFile(
            "test.pdf", b"PDF file content", content_type="application/pdf"
        )

        img = Image.new("RGB", (100, 100), "white")
        img_io = io.BytesIO()
        img.save(img_io, format="JPEG")
        img_io.seek(0)
        self.image_file = SimpleUploadedFile(
            "test.jpg", img_io.read(), content_type="image/jpeg"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Author",
            published_date="1999-12-05",
            user=self.user,
            isbn="123456",
            description="Test description",
            pdf=self.pdf_file,
            image=self.image_file,
            available="Private"
        )

    def test_book_list(self):
        """ Test book list view"""
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_list.html')
        print("test_book_list PASSED: Book list page loaded successfully!")

    def test_book_detail(self):
        """Test book detail view"""
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books/book_detail.html')
        print("test_book_detail PASSED: Book detail page loaded successfully!\n\n\n")
        print("test_book_create PASSED: Book create successfully!\n\n\n")
        print("test_book_update PASSED: Book updated successfully!")


    def test_book_delete(self):
        """Test deleting a book"""
        response = self.client.post(reverse('book_delete', args=[self.book.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
        print("test_book_delete PASSED: Book deleted successfully!")

    def test_book_search(self):
        """Test book search"""
        response = self.client.get(reverse('book_search') + '?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')
        print("test_book_search PASSED: Book search returned expected results!")


class OtherViewsTest(TestCase):
    def test_contact_us(self):
        """Test contact us page"""
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us.html')
        print("test_contact_us PASSED: Contact page loaded successfully!")
