from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .forms import expenseApprovalForm

from .models import Expenses, Department, Budget


def indexRedirect(request):
    if request.user.is_authenticated:
        if request.user.head:
            return redirect('expenseApprovalView',request.user.department.id)
        else:
            return redirect('expenseApprovalRequest')
    else:
        return redirect('expenseApprovalRequest')


@login_required
def expenseApprovalRequest(request):
    employeesExpenses = Expenses.objects.filter(employee=request.user).order_by('-id')
    form = expenseApprovalForm(request.POST or None)
    budget = Budget.objects.get(department=request.user.department)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.employee = request.user
        total = int(form.cleaned_data['hotel_rent']) + int(form.cleaned_data['transport']) + int(
            form.cleaned_data['meal']) + int(form.cleaned_data['others'])
        expense.total_amount = total
        expense.department = request.user.department
        expense.save()
        if budget.expense_approval(expense.id):
            pass
        else:
            expense.form_status = False
            expense.save()
        return redirect('expenseApprovalRequest')
    context = {
        'form': form,
        'expenses': employeesExpenses,
    }
    return render(request, 'expense_approval/form.html', context)


def expenseApprovalView(request, id):
    department = Department.objects.get(id=id)
    if request.user.head and request.user.department == department:
        budget = Budget.objects.get(department=department)
        expenses = Expenses.objects.filter(form_status=None, department=department)
        if request.method == 'POST':
            print(request.POST)
            expense = Expenses.objects.get(id=int(request.POST.get('id')))
            status = request.POST.get('switch')
            if status == 'on':
                expense.form_status = True
                expense.save()
            else:
                expense.form_status = False
                expense.save()
            return redirect('expenseApprovalView', request.user.department.id)
        context = {
            'expenses': expenses,
            'department': department,
            'budget': budget,
        }
        return render(request, 'expense_requests/head.html', context)
    else:
        return HttpResponse('<h1>You need to be a department head to access this view. <a href="/expense">Go to expense page</a></h1>')


def allExpensesView(request, id):
    department = Department.objects.get(id=id)
    if request.user.head and request.user.department == department:
        expenses = Expenses.objects.filter(department=department)
        context = {
            'expenses': expenses,
            'department': department,
        }
        return render(request, 'expense_requests/all.html', context)
    else:
        return HttpResponse("<h1>You need to be this department's head to access this view. <a href='/expense'>Go to expense page</a></h1>")
