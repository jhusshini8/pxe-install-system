"""InstallSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from SystemProject.pxeviews import BeganSystem,FetchDetail,RecordStag,ipmioperation,NewLogin,LoginInfo,logout,passwdedit,UserList,linechart,breadchart

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/beganinstall/', BeganSystem.InstallSystem),
    url(r'^api/getdetail/', FetchDetail.FetchList),
    url(r'^api/statustag/', RecordStag.RecordStag_install),
    url(r'^api/stagssuc/', RecordStag.RecordStag_sucess),
    url(r'^api/getgateway/', ipmioperation.getgateway),
    url(r'^api/login/', NewLogin.UserLogin),
    url(r'^api/userinfo/', LoginInfo.UserInfo),
    url(r'^api/logout/', logout.UserLogout),
    url(r'^api/usereditpass/', passwdedit.repassedit),
    url(r'^api/userlist/', UserList.UserListPage),
    url(r'^api/userlistall/', UserList.UserListPageAll),
    url(r'^api/linechart/', linechart.GetLine),
    url(r'^api/breadchart/', breadchart.GetBreadChart),

    # url(r'^api/operidrac/', ipmioperation.idracinstall),
    # url(r'^api/getsystemdetail/', FetchDetail.FetchSystemList),
]
