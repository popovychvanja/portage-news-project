from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from news.views import SignUpView

admin.site.site_header = "Portage la Prairie News Admin Portal"
admin.site.site_title = "P.L.P. News Reporter Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # <-- Directs root URL to news app
    path('accounts/', include('django.contrib.auth.urls')), # <-- Login/Logout URLs
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
]

# Required for serving media files (images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)