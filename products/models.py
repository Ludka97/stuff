from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)

    external_id = models.CharField(max_length=200, blank=True, null=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Product: {self.title}"
