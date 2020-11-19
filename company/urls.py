from django.urls import path 
from.views       import CompaniesView

urlpatterns = [
    path('/company',CompaniesView.as_view()),
]