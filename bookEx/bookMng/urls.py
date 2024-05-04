from django.urls import path
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('mybooks', views.mybooks, name='mybooks'),

    path('favorite_books/', views.favorite_books, name='favorite_books'),
    path('toggle_favorite/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('book_search/', views.book_search, name='book_search'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path("save_rating/<int:book_id>", views.save_rating, name="save_rating"),


    path('book_comments/<int:book_id>', views.book_comments, name='book_comments'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    # Other URL patterns
]