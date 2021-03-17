from django.contrib import admin
from django.urls import path, include
from users import views as view_user
from django.contrib.auth import views as view_auth
from django.conf import settings
from django.conf.urls.static import static
from users.views import AuthorDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('register/', view_user.register, name='registration'),
    path('profile/', view_user.profile, name='profile'),
    path('update/', view_user.profile_update, name='update'),
    path('login/', view_auth.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', view_auth.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('author/<int:pk>/', AuthorDetailView.as_view(template_name='users/author_view.html'), name='author-detailed'),
    path('post/author/<int:pk>/', AuthorDetailView.as_view(template_name='users/author_view.html'), name='post-author-detailed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)