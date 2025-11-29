from .models import Category
from asgiref.sync import sync_to_async

def categories_processor(request):
    """
    """
    all_categories = Category.objects.prefetch_related('subcategory').all()
    return {'all_categories': all_categories}