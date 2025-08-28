from django.urls import path
from .views import TransactionListView, IncomeDeleteView , ExpenseDeleteView, IncomeCreateView, ExpenseCreateView, IncomeUpdateView, ExpenseUpdateView

urlpatterns = [
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('transactions/income/<int:pk>/delete/', IncomeDeleteView.as_view(), name='income_delete'),
    path('transactions/expense/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),
    path('transactions/income/add/', IncomeCreateView.as_view(), name='income_add'),
    path('transactions/expense/add/', ExpenseCreateView.as_view(), name='expense_add'),
    path('transactions/income/<int:pk>/update/', IncomeUpdateView.as_view(), name='income_update'),
    path('transactions/expense/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense_update'),
]