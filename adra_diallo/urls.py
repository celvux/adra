from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from campaign.views import presign_upload, publications_json

urlpatterns = [
    path('admin/upload-presign/', presign_upload, name='presign_upload'),
    path('admin/', admin.site.urls),
    path('api/publications/', publications_json, name='publications_json'),
    path('', include('campaign.urls', namespace='campaign')),
] + static(settings.MEDIA_URL, document_root=getattr(settings, 'MEDIA_ROOT', ''))
