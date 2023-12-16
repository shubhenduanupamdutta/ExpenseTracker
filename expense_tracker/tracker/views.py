from django.shortcuts import redirect, render
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm
import datetime


# Create your views here.
def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")

    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum("amount"))
    form = ExpenseForm()

    # Logic to calculate the total expenses for the year (last 365 days)
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data_last_year = Expense.objects.filter(date__gt=last_year)
    total_last_year = data_last_year.aggregate(Sum("amount"))

    # Logic to calculate the total expenses for the month (last 30 days)
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data_last_month = Expense.objects.filter(date__gt=last_month)
    total_last_month = data_last_month.aggregate(Sum("amount"))

    # Logic to calculate the total expenses for the week (last 7 days)
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data_last_week = Expense.objects.filter(date__gt=last_week)
    total_last_week = data_last_week.aggregate(Sum("amount"))

    # Logic to calculate daily expenses for last 30 days
    daily_expenses = Expense.objects\
        .filter(date__gt=last_month)\
        .values('date')\
        .order_by('date')\
        .annotate(sum=Sum('amount'))

    categorical_expenses = Expense.objects\
        .filter(date__gt=last_month)\
        .values('category')\
        .order_by('category')\
        .annotate(sum=Sum('amount'))

    print(daily_expenses)

    context = {
        "expenses": expenses,
        "form": form,
        "total_expenses": total_expenses,
        "yearly_sum": total_last_year,
        "monthly_sum": total_last_month,
        "weekly_sum": total_last_week,
        "daily_expenses": daily_expenses,
        "categorical_expenses": categorical_expenses,
    }
    return render(request, "tracker/index.html", context)


def edit(request, id):
    if request.method == "POST":
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
        return redirect("index")

    expense = Expense.objects.get(id=id)
    form = ExpenseForm(instance=expense)  # pre-populate form with expense data
    return render(request, "tracker/edit.html", {"form": form})


def delete(request, id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
        return redirect("index")
