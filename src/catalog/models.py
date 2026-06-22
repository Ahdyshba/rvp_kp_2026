from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    def __str__(self):
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=255)
    attribute_type = models.CharField(max_length=20, choices=(
        ('string', 'Строка'),
        ('int', 'Число'),
        ('decimal', 'Десятичное'),
        ('boolean', 'Да/Нет'),
    ))

    def __str__(self):
        return self.name

class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    is_required = models.BooleanField(default=False)
    is_filter = models.BooleanField(default=False)

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value_string = models.TextField(null=True, blank=True)
    value_int = models.IntegerField(null=True, blank=True)
    value_decimal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    value_boolean = models.BooleanField(default=False)
