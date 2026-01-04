def categories_processor(request):
    from .models import Category
    return {
        'categories': Category.objects.all()
    }
