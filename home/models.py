from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


def start_with_zeor(value):
    if value < 0:
        raise ValidationError(
            _("%(value)s cannot exist"),
            params={"value": value},
        )

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Fooditem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fooditems')  # Linking to Category
    Name = models.CharField(max_length=50)
    descriptions = models.TextField(max_length=1000, null=True, blank=True)
    quantity = models.IntegerField(validators=[start_with_zeor])
    price = models.IntegerField()
    image = models.ImageField(upload_to="foodimage/")
    active = models.BooleanField(default=False)
    
    def average_rating(self):
        return self.ratings.aggregate(Avg('score'))['score__avg'] or 0
    
    def total_ratings_count(self):
        return self.ratings.count()

    def __str__(self):
        return self.Name

class Rating(models.Model):
    food_item = models.ForeignKey(Fooditem, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.score} by {self.user.first_name} for {self.food_item.Name}"
