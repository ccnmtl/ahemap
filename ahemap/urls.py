from ahemap.main import views
from django.conf import settings
from django.urls import re_path
from django.conf.urls import include
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
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    path('cas/login', cas_views.LoginView.as_view(),
         name='cas_ng_login'),
    path('cas/logout', cas_views.LogoutView.as_view(),
         name='cas_ng_logout'),
    re_path(r'^$', views.HomeView.as_view()),
    re_path(r'^map/$', views.MapView.as_view(), name='map-view'),
    re_path(r'^browse/$', views.BrowseView.as_view(), name='browse-view'),
    re_path(r'^save/$', views.SaveView.as_view(), name='save-view'),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^view/(?P<pk>\d+)/$', views.InstitutionDetailView.as_view(),
            name='institution-detail-view'),

    re_path(r'^admin/import/institution/',
            views.InstitutionImportView.as_view(),
            name='institution-import-view'),
    re_path(r'^admin/', admin.site.urls),

    re_path(r'^_impersonate/', include('impersonate.urls')),
    re_path(r'^stats/$$', TemplateView.as_view(template_name="stats.html")),
    re_path(r'smoketest/', include('smoketest.urls')),
    re_path(r'^uploads/(?P<path>.*)$$',
            serve, {'document_root': settings.MEDIA_ROOT}),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
