from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    (r'^table2sql/$', 'ds.views.table2sql'),

]


