from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
    path("countries/", views.ListCreateCountry.as_view(), name="list_create_country"),
    path(
        "countries/bulk-update/",
        views.BulkUpdateCountry.as_view(),
        name="bulk_update_country",
    ),
    path("states/", views.ListCreateState.as_view(), name="list_create_state"),
    path(
        "states/bulk-update/", views.BulkUpdateState.as_view(), name="bulk_update_state"
    ),
    path("cities/", views.ListCreateCity.as_view(), name="list_create_city"),
    path(
        "cities/bulk-update/", views.BulkUpdateCity.as_view(), name="bulk_update_city"
    ),
    path("all-data/", views.AllDataView.as_view(), name="all_data"),
    path(
        "states/<str:state_id>/cities/",
        views.CitiesOfState.as_view(),
        name="cities_of_state",
    ),
    path(
        "countries/<str:country_name>/cities/",
        views.CitiesOfCountryName.as_view(),
        name="cities_of_country_name",
    ),
    path(
        "cities/minmax-population/",
        views.MinMaxPopulationView.as_view(),
        name="minmax_population",
    ),
    
    
    
    path('api/token/signup/', views.SignUpView.as_view(), name='user_signup'),
    path('api/token/signin/', views.SignInView.as_view(), name='user_signin'),
    path('api/token/signout/', views.SignOutUserView.as_view(), name='user_signout'),
    
]
