from django.urls import path

from .views import expenseApprovalRequest, indexRedirect, expenseApprovalView, allExpensesView

urlpatterns = [
    path('', indexRedirect, name='iredirect'),
    path('expense', expenseApprovalRequest, name='expenseApprovalRequest'),
    path('approve-expenses/<id>', expenseApprovalView, name='expenseApprovalView'),
    path('all-expenses/<id>', allExpensesView, name='allExpensesView'),
]
