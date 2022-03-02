from django.urls import path

from . import views

urlpatterns = [
    path('portfolio/', views.index, name='user-portfolio'),
    path('portfolio/holdings/', views.holdings, name='holdings'),
    path('portfolio/delete', views.delete_holding, name='delete-holding'),
    path('portfolio/previous_holdings/', views.previous_holdings, name='previous-holdings'),
    path('portfolio/delete_previous_holdings/<holding_id>', views.delete_previous_holding, name='delete-previous-holding')
]