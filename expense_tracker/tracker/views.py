from django.shortcuts import redirect, render
from .forms import ExpenseForm


# Create your views here.
def index(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")
    form = ExpenseForm()
    return render(request, "tracker/index.html", {"form": form})
