from django.urls import path

from . import views

app_name = "poster"

# first argument is relative URL; second is the view it corresponds to in
# views.py; third is the name of the view (necessary for the reverse() function,
# which is explained in views.py)
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('new', views.new, name='new'),
    path('detail/<int:pk>', views.PostView.as_view(), name='detail'),
    path('delete/<int:pk>', views.delete, name='delete')
]
