from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework import routers

from ahemap.main import views


admin.autodiscover()


auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))
if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))


router = routers.DefaultRouter()
router.register(r'institution', views.InstitutionViewSet, base_name='site')


urlpatterns = [
    auth_urls,
    url(r'^$', views.IndexView.as_view()),
    url(r'^map/$', views.MapView.as_view(), name='map-view'),
    url(r'^api/', include(router.urls)),
    url(r'^view/(?P<pk>\d+)/$', views.InstitutionDetailView.as_view(),
        name='institution-detail-view'),

    url(r'^admin/', admin.site.urls),
    url(r'^admin/import/institution/',
        views.InstitutionImportView.as_view(), name='institution-import-view'),
    url(r'^_impersonate/', include('impersonate.urls')),
    url(r'^stats/$$', TemplateView.as_view(template_name="stats.html")),
    url(r'smoketest/', include('smoketest.urls')),
    url(r'infranil/', include('infranil.urls')),
    url(r'^uploads/(?P<path>.*)$$',
        serve, {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
