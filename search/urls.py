from django.conf.urls import url

from .views import SearchProductListView

app_name = 'search'
urlpatterns = [url(r'^$', SearchProductListView.as_view(), name='search_query'), ]


