from django.urls import path
from . import views

# Define the application namespace for URL reversing
# This helps distinguish URLs between different apps when using 'url' template tag
app_name = 'certificate'

# URL patterns for the Certificate CRUD (Create, Read, Update, Delete) operations.
urlpatterns = [
    # Home/List view: Displays all records
    # URL: /
    path('', views.home, name='home'),
]