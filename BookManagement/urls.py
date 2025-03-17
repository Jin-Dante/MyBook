"""
URL configuration for BookManagement project.

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book_list', views.book_list, name='book_list'),
    path('', views.login_view, name='login'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/create/', views.book_create, name='book_create'),   
    path('book/<int:pk>/update/', views.book_update, name='book_update'), 
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'), 
    path('signup/', views.signup, name='signup'),
    # path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.book_search, name='book_search'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('book/<int:pk>/like/', views.like_book, name='like_book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
