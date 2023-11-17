"""
URL configuration for background project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from mybackground import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("login/", views.login),  # 登录页面
    path("logout/", views.logout),  # 注销功能

    path("admin/", views.admin),  # 管理员页面

    # 玩家类页面
    path("player/", views.player_message),  # 玩家信息展示
    path("player/<int:pid>/edit/", views.player_edit),  # 玩家信息编辑
    path("player/<int:pid>/delete/", views.player_delete),  # 玩家信息删除

    # 排行榜记录类页面
    path("record/", views.record_rank),#排行榜记录展示
    path("record/<int:rid>/edit", views.record_edit),#排行榜记录编辑
    path("record/<int:rid>/delete",views.record_delete), #排行榜记录删除
    path("record/analysis",views.record_analysis),#排行榜记录分析
]
