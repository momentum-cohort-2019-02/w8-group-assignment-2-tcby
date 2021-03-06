from django.db import models
from django.urls import reverse
    # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
    # Required to make use of 'User' class
from django.utils.text import slugify

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
    
    def display_deck(self):
        """Create a string for Decks. This is required to display Decks in Admin."""
        return ', '.join(deck.title for deck in self.decks.all()[:10])

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return reverse('category_detail', args=[str(self.slug)])
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Quiz(models.Model):
    """Model representing each instance of a user quizzing themself."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Foreign Key used b/c a Quiz can only be taken by 1 User, but User can take many quizzes.
    total_score = models.IntegerField(null=True, blank=True)
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#integerfield
    deck = models.ForeignKey(to='Deck', on_delete=models.SET_NULL, null=True, blank=True, related_name='quiz')
    

class Deck(models.Model):
    """
    Model representing deck of flashcards
    """
    title = models.CharField(max_length=200, unique=True)
    creator = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='deck')
    categories = models.ManyToManyField(to='Category', related_name='decks')
    public = models.BooleanField(default=True, editable=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def set_slug(self):
        """
        Creates unique slug for every deck
        """
        if self.slug:
            return

        base_slug = slugify(self.title)
        slug = base_slug
        n = 0

        while Deck.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + '-' + str(n)

        self.slug = slug

    def save(self, *args, **kwargs):
        """
        Hides slug field in admin, saves slug to use in url
        """
        self.set_slug()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # need to create view and template 
        return reverse('quiz-view', args=[(self.slug)])
    
    def __str__(self):
        return self.title

    def display_card(self):
        """Create a string for Cards. This is required to display Cards in Admin."""
        return ', '.join(card.question for card in self.card.all()[:10])

class Card(models.Model):
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500)
    correct = models.BooleanField(blank=True, null=True, default=None)
        # https://docs.djangoproject.com/en/2.1/ref/models/fields/#booleanfield
    decks = models.ManyToManyField(to=Deck, related_name='card', blank=True)

    def display_deck(self):
        """Create a string for Decks. This is required to display Decks in Admin."""
        return ', '.join(deck.title for deck in self.decks.all()[:3])
            # str.join(iterable) --> https://docs.python.org/3.7/library/stdtypes.html?highlight=join#str.join
            # 1st three '[:3]' deck items in the 'self.deck.all()' for a 'Card' object will be joined separated by a comma ', '
    
    def __str__(self):
        return self.question 

    def get_absolute_url(self):
        """Returns the url to access a detail record for this card."""
        return reverse('index')
