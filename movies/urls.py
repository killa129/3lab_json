from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("add_movies/", views.add_movies, name="add_movies"),
    path("import_json/", views.import_json, name="import_json"),
    path("export_json/", views.export_json, name="export_json"),
]
