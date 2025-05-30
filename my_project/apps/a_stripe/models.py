from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
CustomUser = get_user_model()
# Create your models here.


# products/models.py


User = settings.AUTH_USER_MODEL

def get_image_filename(instance, filename):
    name = instance.name
    slug = slugify(name)
    return f"products/{slug}-{filename}"

class ProductTag(models.Model):
    name = models.CharField(
        max_length=100, help_text=_("Designates the name of the tag.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    tags = models.ManyToManyField(ProductTag, blank=True)
    desc = models.TextField(_("Description"), blank=True)
    thumbnail = models.ImageField(upload_to=get_image_filename, blank=True)
    url = models.URLField()
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.product.name} {self.price}"


class PurchaseHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_success = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    amount_paid = models.CharField(max_length=50, default=0)
    created_at = models.DateTimeField(auto_now_add=True)



# class UserPayment(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=255)
#     stripe_checkout_id = models.CharField(max_length=255)
#     stripe_product_id = models.CharField(max_length=255)
#     product_name = models.CharField(max_length=255)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     currency = models.CharField(max_length=3)
#     has_paid = models.BooleanField(default=False)


#     def __str__(self):
#         return f"{self.user.username} - {self.product_name} - Paid: {self.has_paid}"
    

