from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import IncomeForm, ExpenseForm
from .models import Income, Expense


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
        
class TransactionListView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        template_name = "transaction/transaction_list.html"
        income = Income.objects.all()
        expenses = Expense.objects.all()

        context = {
            "incomes": income,
            "expenses": expenses
        }
        return render(request, template_name, context)

class IncomeCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        template_name = "transaction/form.html"
        context = {
            "form": IncomeForm(),
            "button_label": "Add Income"
        }
        return render(request, template_name, context)

    def post(self, request):
        form = IncomeForm(request.POST, request.FILES)
        if form.is_valid():
            income = form.save(commit=False)
            income.added_by = request.user
            income.save()
            messages.success(request, "Income added successfully!")
            return redirect("transaction_list")
        else:
            messages.error(request, "Please correct the errors below.")
            template_name = "transaction/form.html"
            context = {"form": form}
            return render(request, template_name, context)

class ExpenseCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request):
        template_name = "transaction/form.html"
        context = {
            "form": ExpenseForm(),
            "button_label": "Add Expense"
        }
        return render(request, template_name, context)

    def post(self, request):
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.added_by = request.user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect("transaction_list")
        else:
            messages.error(request, "Please correct the errors below.")
            template_name = "transaction/form.html"
            context = {"form": form}
            return render(request, template_name, context)

class IncomeDeleteView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request, pk):
        income = Income.objects.get(pk=pk)
        name = income.project.name
        if request.user.is_staff or income.added_by == request.user:
            template_name = "transaction/delete.html"
            context = { "name": name}
            return render(request, template_name, context)
        else:
            messages.error(request, "You do not have permission to delete this income.")
            return redirect("transaction_list")

    def post(self, request, pk):
        income = Income.objects.get(pk=pk)
        if request.user.is_staff or income.added_by == request.user:
            income.delete()
            messages.success(request, "Income deleted successfully!")
        else:
            messages.error(request, "You do not have permission to delete this income.")
        return redirect("transaction_list")

class ExpenseDeleteView(LoginRequiredMixin, StaffRequiredMixin, View):  
    def get(self, request, pk):
        expense = Expense.objects.get(pk=pk)
        name = expense.project.name
        if request.user.is_staff or expense.added_by == request.user:
            template_name = "transaction/delete.html"
            context = { "name": name}
            return render(request, template_name, context)
        else:
            messages.error(request, "You do not have permission to delete this expense.")
            return redirect("transaction_list")

    def post(self, request, pk):
        expense = Expense.objects.get(pk=pk)
        if request.user.is_staff or expense.added_by == request.user:
            expense.delete()
            messages.success(request, "Expense deleted successfully!")
        else:
            messages.error(request, "You do not have permission to delete this expense.")
        return redirect("transaction_list")

class IncomeUpdateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request, pk):
        income = Income.objects.get(pk=pk)
        if request.user.is_staff or income.added_by == request.user:
            template_name = "transaction/form.html"
            context = {
                "form": IncomeForm(instance=income),
                "button_label": "Update Income"
            }
            return render(request, template_name, context)
        else:
            messages.error(request, "You do not have permission to edit this income.")
            return redirect("transaction_list")

    def post(self, request, pk):
        income = Income.objects.get(pk=pk)
        if request.user.is_staff or income.added_by == request.user:
            form = IncomeForm(request.POST, request.FILES, instance=income)
            if form.is_valid():
                form.save()
                messages.success(request, "Income updated successfully!")
                return redirect("transaction_list")
            else:
                messages.error(request, "Please correct the errors below.")
                template_name = "transaction/form.html"
                context = {
                    "form": form,
                    "button_label": "Update Income"
                }
                return render(request, template_name, context)
        else:
            messages.error(request, "You do not have permission to edit this income.")
            return redirect("transaction_list")


class ExpenseUpdateView(LoginRequiredMixin, StaffRequiredMixin, View):
    def get(self, request, pk):
        expense = Expense.objects.get(pk=pk)
        if request.user.is_staff or expense.added_by == request.user:
            template_name = "transaction/form.html"
            context = {
                "form": ExpenseForm(instance=expense),
                "button_label": "Update Expense"
            }
            return render(request, template_name, context)
        else:
            messages.error(request, "You do not have permission to edit this expense.")
            return redirect("transaction_list")

    def post(self, request, pk):
        expense = Expense.objects.get(pk=pk)
        if request.user.is_staff or expense.added_by == request.user:
            form = ExpenseForm(request.POST, request.FILES, instance=expense)
            if form.is_valid():
                form.save()
                messages.success(request, "Expense updated successfully!")
                return redirect("transaction_list")
            else:
                messages.error(request, "Please correct the errors below.")
                template_name = "transaction/form.html"
                context = {
                    "form": form,
                    "button_label": "Update Expense"
                }
                return render(request, template_name, context)
        else:
            messages.error(request, "You do not have permission to edit this expense.")
            return redirect("transaction_list")
