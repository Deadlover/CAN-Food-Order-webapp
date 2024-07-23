from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from django.forms import ValidationError
from django.conf import settings
from home.models import Fooditem

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.first_name}"
    
    @property
    def get_total(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def get_all_total(self):
        orderitems = self.items.all() # because related_name='items' if related name is given uwon't have to use modelname_set
        total = sum([item.quantity_item for item in orderitems])
        return total
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items') #
    food_item = models.ForeignKey(Fooditem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.Name}"
    
    @property
    def quantity_item(self):
        total = self.quantity * self.food_item.price
        return total
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], help_text="Fixed discount amount")
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True, help_text="Discount percentage (0-100). Leave blank if using a fixed amount.")
    valid_from = models.DateTimeField(default=datetime.datetime.now)
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=False)
    usage_limit = models.IntegerField(validators=[MinValueValidator(1)], default=1, help_text="How many times this coupon can be used.")
    times_used = models.IntegerField(default=0, editable=False, help_text="How many times this coupon has been used.")

    def __str__(self):
        return self.code

    def clean(self):
        # Custom validation to ensure either discount_amount or discount_percentage is provided, not both
        if self.discount_amount and self.discount_percentage:
            raise ValidationError(_('Provide either a discount amount or a discount percentage, not both.'))
        elif not self.discount_amount and not self.discount_percentage:
            raise ValidationError(_('You must provide either a discount amount or a discount percentage.'))
        
    def is_valid(self):
        # Check if the coupon is still valid based on date and usage
        now = datetime.datetime.now()
        if self.valid_from <= now <= self.valid_to and self.times_used < self.usage_limit and self.active:
            return True
        return False
