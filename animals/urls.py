from django.urls import path, include

from animals import views


urlpatterns = [
    path('refresh_from_csv/', views.refresh_from_csv)
]
