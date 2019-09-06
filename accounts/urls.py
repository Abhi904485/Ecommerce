from django.conf.urls import url

from .views import (login_page, register_page, logout_page, )

app_name = 'accounts'
urlpatterns = [
        url(r'^login/$', login_page, name='login'),
        url(r'^logout/$', logout_page, name='logout'),
        url(r'^register/$', register_page, name='register'),

]
