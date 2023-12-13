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
