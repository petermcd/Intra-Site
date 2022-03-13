from django.urls import path

from finance import views

app_name = "finance"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("loan/<int:pk>/", views.LoanDetailView.as_view(), name="loan_details"),
    path("bill/<int:pk>/", views.BillDetailView.as_view(), name="bill_details"),
    path("investments/", views.InvestmentView.as_view(), name="investment_list"),
]
