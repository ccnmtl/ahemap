from ahemap.main import views
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve
from django_cas_ng import views as cas_views
from rest_framework import routers


admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'institution', views.InstitutionViewSet, basename='site')


urlpatterns = [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    url(r'^$', views.HomeView.as_view()),
    url(r'^map/$', views.MapView.as_view(), name='map-view'),
    url(r'^browse/$', views.BrowseView.as_view(), name='browse-view'),
    url(r'^save/$', views.SaveView.as_view(), name='save-view'),
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
