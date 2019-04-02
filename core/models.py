from django.db import models
from django.urls import reverse
    # Used to generate URLs by reversing the URL patterns
from django.utils.text import slugify
from django.contrib.auth.models import User
    # Required to make use of 'User' class

# Create your models here.
class Category(models.Model):
    """Model representing a deck category."""
    name = models.CharField(max_length=200, help_text='Enter a deck category (e.g. Math, Geography, etc.)')
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        if self.slug:
            return
        base_slug = slugify(self.name)
        slug = base_slug
        n = 0
        while Category.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)
        self.slug =slug

    def get_absolute_url(self):
        """Returns the url to access a particular Category instance."""
        return reverse('category-detail', args=[str(self.slug)])
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Creator(models.Model):
    """Model representing a deck or flashcard creator."""
    name = models.ForeignKey(User, on_delete=models.CASCADE)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#foreign-key-arguments
        # Foreign Key used b/c Creator can only be one User, but a User can be a Creator on many decks/cards
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)

    def set_slug(self):
        if self.slug:
            return
        base_slug = slugify(self.name)
        slug = base_slug
        n = 0
        while Category.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)
        self.slug =slug

    def get_absolute_url(self):
        """Returns the url to access a particular Creator instance."""
        return reverse('creator-detail', args=[str(self.slug)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name.username
        
class Card(models.Model):
    """Model representing a flashcard that can be included in any deck"""
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True)
        # ForeignKey used b/c Card can only have one Creator, but Creator can have multiple Cards
    
    date_added = models.DateField(auto_now_add=True, null=True, blank=True)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/
        # 'auto_now_add=True' automatically set the field to now when the object is first created
        # useful for creation of datestamps

    category = models.ManyToManyField(Category, help_text='Select a category for this card')
        # ManyToManyField used b/c Category can have many Cards. Cards can have many Categories.

    correctly_answered_by = models.ManyToManyField(to=User, related_name='correctly_answered_cards', through='CorrectAnswer')
        # ManyToManyField used b/c Users can correctly answer many Cards. Cards can have many User correct answers.
        # 'through' option allows an intermediate table to be specified
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#field-types


    class Meta:
        ordering = ['-date_added',]

    def display_category(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(category.name for category in self.category.all()[:3])
            # str.join(iterable) --> https://docs.python.org/3.7/library/stdtypes.html?highlight=join#str.join
            # 1st three '[:3]' category items in the 'self.category.all()' for a 'Book' object will be joined separated by a comma ', '

    display_category.short_description = 'category'
        # '.short_description' is a built-in Django attribute to provide human-readable descriptions for callback functions
        # https://docs.djangoproject.com/en/2.1/ref/contrib/admin/actions/
        
    def display_correctly_answered_by(self):
        """Create a string for the Category. This is required to display category in Admin."""
        return ', '.join(correctly_answered_by.username for correctly_answered_by in self.correctly_answered_by.all()[:3])
            # str.join(iterable) --> https://docs.python.org/3.7/library/stdtypes.html?highlight=join#str.join
            # 1st three '[:3]' favorited_by items in the 'self.favorited_by.all()' for a 'Book' object will be joined separated by a comma ', '

    display_correctly_answered_by.short_description = 'correctly answered by'

    def __str__(self):
        """String for representing the Model object."""
        return self.question

    def get_absolute_url(self):
        """Returns the url to access a detail record for this card."""
        return reverse('index')

class CorrectAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
        # Foreign Key used b/c a user can only favorite a book once, but a user can have many book favorites
        # 'User' model class argument is declared to connect the relationship between the 'CorrectAnswer' and 'User' classes
        
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
        # Foreign Key used b/c a CorrectAnswer can only be on one Card per user, but a Card can have many CorrectAnswers by many users
