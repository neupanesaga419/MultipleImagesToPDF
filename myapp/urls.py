from django.urls import path
import myapp.views as myview

urlpatterns = [
    path('',myview.index,name="index"),
]
