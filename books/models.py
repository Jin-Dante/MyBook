from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

class Book(models.Model):
    PRIVATE = 'Private'
    GLOBAL = 'Global'
    AVAILABILITY_CHOICES = [
        (PRIVATE, _('Private')),
        (GLOBAL, _('Global')),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=17)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateField(_("Date"))
    description = models.TextField()
    pdf = models.FileField(upload_to='books/pdfs/')
    image = models.ImageField(upload_to='books/images/')
    available = models.CharField(
        max_length=8,
        choices=AVAILABILITY_CHOICES,
        default=PRIVATE,
    )
    liked_users = models.ManyToManyField(User, related_name='liked_books', blank=True)

    


    
