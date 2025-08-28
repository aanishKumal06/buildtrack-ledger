from django.contrib import admin
from .models import Expense, Income
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'project')
    search_fields = ('project__name',)

admin.site.register(Expense, ExpenseAdmin)

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'date', 'project')
    search_fields = ('project__name',)

admin.site.register(Income, IncomeAdmin)

