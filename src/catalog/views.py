from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, Category, Attribute, CategoryAttribute, ProductAttributeValue
from .serializers import ProductSerializer, CategorySerializer, CategoryAttributeSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        search_query = self.request.query_params.get('search')
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                child_ids = [category.id]
                queue = [category.id]
                while queue:
                    parent_id = queue.pop(0)
                    children = Category.objects.filter(parent_id=parent_id).values_list('id', flat=True)
                    for child_id in children:
                        if child_id not in child_ids:
                            child_ids.append(child_id)
                            queue.append(child_id)
                queryset = queryset.filter(category_id__in=child_ids)
            except Category.DoesNotExist:
                pass
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        for key, value in self.request.query_params.items():
            if key.startswith('attr_'):
                attr_name = key[5:]
                if value:
                    try:
                        attribute = Attribute.objects.get(name=attr_name)
                        if attribute.attribute_type == 'string':
                            queryset = queryset.filter(
                                productattributevalue__attribute=attribute,
                                productattributevalue__value_string__icontains=value
                            )
                        elif attribute.attribute_type == 'int':
                            try:
                                int_value = int(value)
                                queryset = queryset.filter(
                                    productattributevalue__attribute=attribute,
                                    productattributevalue__value_int=int_value
                                )
                            except ValueError:
                                pass
                        elif attribute.attribute_type == 'decimal':
                            try:
                                decimal_value = float(value)
                                queryset = queryset.filter(
                                    productattributevalue__attribute=attribute,
                                    productattributevalue__value_decimal=decimal_value
                                )
                            except ValueError:
                                pass
                        elif attribute.attribute_type == 'boolean':
                            bool_value = value.lower() in ['true', '1', 'yes', 'on']
                            queryset = queryset.filter(
                                productattributevalue__attribute=attribute,
                                productattributevalue__value_boolean=bool_value
                            )
                    except Attribute.DoesNotExist:
                        pass
        
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class FilterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryAttribute.objects.none()
    serializer_class = CategoryAttributeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if not category_id:
            return CategoryAttribute.objects.none()
        
        try:
            category = Category.objects.get(id=category_id)
            parent_ids = []
            current = category
            while current:
                parent_ids.append(current.id)
                current = current.parent
            return CategoryAttribute.objects.filter(
                category_id__in=parent_ids,
                is_filter=True
            )
        except Category.DoesNotExist:
            return CategoryAttribute.objects.none()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = response.data
        
        category_id = request.query_params.get('category')
        if category_id:
            for item in data:
                attr_id = item['attribute']
                attr_type = item['attribute_type']
                values = []
                
                if attr_type == 'string':
                    values = ProductAttributeValue.objects.filter(
                        attribute_id=attr_id,
                        value_string__isnull=False
                    ).exclude(value_string='').values_list('value_string', flat=True).distinct()
                elif attr_type == 'int':
                    values = ProductAttributeValue.objects.filter(
                        attribute_id=attr_id,
                        value_int__isnull=False
                    ).values_list('value_int', flat=True).distinct()
                elif attr_type == 'decimal':
                    values = ProductAttributeValue.objects.filter(
                        attribute_id=attr_id,
                        value_decimal__isnull=False
                    ).values_list('value_decimal', flat=True).distinct()
                elif attr_type == 'boolean':
                    values = [True, False]
                
                item['possible_values'] = list(values)
        
        return response

def home(request):
    category_id = request.GET.get('category')
    current_category = None
    
    if category_id:
        try:
            current_category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            pass
    
    return render(request, 'catalog/home.html', {'current_category': current_category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    from reviews.models import Review
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    return render(request, 'catalog/product.html', {
        'product_id': product_id,
        'product': product,
        'reviews': reviews
    })