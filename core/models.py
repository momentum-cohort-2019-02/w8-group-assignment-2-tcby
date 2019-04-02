from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.

User = get_user_model()

class Deck(models.Model):
    title = models.CharField(max_length=255)
    # creator = models.ForeignKey(Creator, on_delete=models.PROTECT)
    user = models.ManyToManyField(User, related_name="user_decks", on_delete=models.PROTECT)
    # category = models.ManyToManyField(Category, related_name=deck_categories, on_delete=models.PROTECT)
    # round = models.ForeignKey(Round, related_name="deck_rounds", on_delete=PROTECT)
    public = models.BooleanField()
    correct = models.BooleanField()
    slug = models.SlugField()
    date_created = date_added = models.DateField('Date Added', auto_now_add=True)


    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.set_slug()
        super().save(*args, **kwargs)    

    def set_slug(self):
        # If the slug is already set, stop here.
        if self.slug:
            return

        base_slug = slugify(self.title)
        slug = base_slug
        n = 0

        while Deck.objects.filter(slug=slug).count():
            n += 1
            slug = base_slug + "-" + str(n)

        self.slug = slug[:50]  
