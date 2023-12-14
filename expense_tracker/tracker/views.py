from django.shortcuts import redirect, render

from .models import Expense
from .forms import ExpenseForm


# Create your views here.
def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")

    expenses = Expense.objects.all()
    form = ExpenseForm()
    context = {"expenses": expenses, "form": form}
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
