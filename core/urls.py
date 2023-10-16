from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import index, serve_file, create_token_url, file_not_access_url

media_url = settings.MEDIA_URL if not settings.MEDIA_URL[0] == '/' else settings.MEDIA_URL[1:]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('create/url/', create_token_url, name='create_token_url'),
    path('serve/<str:token>/', serve_file, name='serve_file'),
    path(f'{media_url}private/<str>', file_not_access_url, name='file_not_access_url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
