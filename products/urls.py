from django.urls import path
from .views import home, product_detail, toggle_wishlist, wishlist_page
from .views import add_review
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),

    path('wishlist/<int:product_id>/', toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/', wishlist_page, name='wishlist_page'),
    path("add-review/<int:product_id>/", add_review, name="add_review"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)