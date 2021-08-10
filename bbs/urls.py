
from django.urls import path
from django.conf.urls import url
from . import views
# from bbs import views
# import bbs.views as views

app_name = 'bbs'

# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
#     url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
#     url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
#
#     # path('', views.index, name='index')
# ]

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # path('', views.IndexView.as_view(), name='index'),
    # url(r'^$', views.index, name='index'),
    # path('', views.index, name='index'),

    path('parent', views.parent, name='parent'),
    path('child', views.child, name='child'),

    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),

    # path('', views.index, name='index')
]
