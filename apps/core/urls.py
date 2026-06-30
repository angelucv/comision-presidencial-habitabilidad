from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("comision/", views.comision, name="comision"),
    path("como-funciona/", views.como_funciona, name="como_funciona"),
]
