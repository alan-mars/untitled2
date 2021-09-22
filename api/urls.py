from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import routers

from api import views


router = routers.DefaultRouter()
router.register(r'xxx', views.View2View)
router.register(r'rt', views.View2View)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('users/', views.UsersView.as_view()),

    re_path(r'^(?P<version>[v1|v5]+)/version/$', views.VersionView.as_view(), name='uu'),
    re_path(r'^(?P<version>[v1|v5]+)/parser/$', views.ParserView.as_view()),
    re_path(r'^(?P<version>[v1|v5]+)/roles/$', views.RolesView.as_view()),
    re_path(r'^(?P<version>[v1|v5]+)/userinfo/$', views.UserInfoView.as_view()),
    re_path(r'^(?P<version>[v1|v5]+)/userinfo1/$', views.UserInfoView1.as_view()),
    re_path(r'^(?P<version>[v1|v5]+)/usergroup/$', views.UserGroupView.as_view()),
    re_path(r'^(?P<version>[v1|v5]+)/pager1/$', views.Pager1View.as_view()),

    re_path(r'^(?P<version>[v1|v5]+)/v2/$', views.View2View.as_view({"get": 'list', "post": 'create'})),
    re_path(r'^(?P<version>[v1|v5]+)/v2/(?P<pk>\d*)/$', views.View2View.as_view({"get": 'retrieve', "post": 'create', "delete": 'destroy', "put": 'update', "patch": 'partial_update'})),
    re_path(r'^(?P<version>[v1|v5]+)/', include(router.urls)),

    re_path(r'^(?P<version>[v1|v5]+)/test/$', views.TestView.as_view()),
]
