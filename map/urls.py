from django.urls import path
from map import views

urlpatterns = [
    path('business/', views.BusinessDetails.as_view(), name=''),
    path('user-create/', views.UserView.as_view(), name=''),
    path('score/', views.BroScrView.as_view()),
    path('loan/', views.LoanApplicationView.as_view())
]