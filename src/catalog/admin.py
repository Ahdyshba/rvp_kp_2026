from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, Attribute, CategoryAttribute, ProductAttributeValue

admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product)
admin.site.register(Attribute)
admin.site.register(CategoryAttribute)
admin.site.register(ProductAttributeValue)