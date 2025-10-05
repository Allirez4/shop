from .models import Category
def categories_processor(request):
    all_categories = Category.objects.prefetch_related('subcategory').all()
    return {'all_categories': all_categories}