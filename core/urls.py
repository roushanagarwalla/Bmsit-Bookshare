from django.urls import path
from core import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', view=views.index, name="index"),
    path('add-book', view=views.add_book, name="add_book"),
    path('my_book', view=views.my_book, name="my_book"),
    
    path('search', view=views.search, name="search"),
    
    path('signup', view=views.handle_signup, name="signup"),
    path('login', view=views.handle_login, name="login"),
    path('logout', view=views.handle_logout, name="logout"),
    
    path('update_book/<int:id>', view=views.update_book, name="update_book"),
    path('delete_book/<int:id>', view=views.delete_book, name="delete_book"),
    
    path('add_contact', view=views.add_contact, name="add_contact"),
    path('view_contact/<int:user>', view=views.view_contact, name="view_contact"),
    path('update_contact/<int:user>', view=views.update_contact, name="update_contact"),
    
    path('category', view=views.categories, name="category"),
    path('add_category', view=views.add_category, name="add_category"),
    path('category/<int:id>', view=views.categories_post, name="categories_post"),
    
    path('book_request/<int:id>', view=views.book_request, name="book_request"),
    path('accept/<int:id>', view=views.accept_request, name="accept_request"),
    path('reject/<int:id>', view=views.reject_request, name="reject_request"),
    
]

handler404 = "core.views.custom_404"

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
