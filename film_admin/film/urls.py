from django.urls import path
from . import views

# 必须添加，否则会报错
app_name = 'film'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path(r'^film/(\d+)/$', views.pye, name='detail'),
    path('<int:pk>/', views.result, name='result'),
    # path(r'^film/(\d+)/$', views.add2, name='add2')

    # path('pye', views.pye, name='index'),
]
