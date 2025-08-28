import os
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import date
from base.models import AbstractBaseModel
from decimal import Decimal
from project.models import Project  

class ExpenseCategory(models.TextChoices):
    MATERIAL = "MATERIAL", "Material Purchase"
    LABOR = "LABOR", "Labor Cost"
    EQUIPMENT = "EQUIPMENT", "Equipment Rental"
    OTHER = "OTHER", "Other"

class Expense(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateField(default=date.today)
    category = models.CharField(max_length=20, choices=ExpenseCategory.choices, default=ExpenseCategory.OTHER)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    description = models.TextField(blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.category} - {self.amount}"

class PaymentMethod(models.TextChoices):
    CASH = "CASH", "Cash"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    CHEQUE = "CHEQUE", "Cheque"
    ONLINE = "ONLINE", "Online Payment"

class Income(AbstractBaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="incomes")
    date = models.DateField(default=date.today)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    description = models.TextField(blank=True)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.project.name} - {self.amount} ({self.payment_method})"


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if ext not in valid_extensions:
        raise ValidationError('Unsupported file extension. Only JPG, PNG, and PDF are allowed.')

class ExpenseDocument(models.Model):
    expense = models.ForeignKey(
        "Expense", on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(
        upload_to="expense",
        validators=[validate_file_extension]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.file and not self.pk:
            ext = os.path.splitext(self.file.name)[1]  # Keep original extension
            new_name = f"{uuid.uuid4()}{ext}"
            self.file.name = os.path.join("expense", new_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ExpenseDoc: {self.expense.project.name} ({self.file.name})"


class IncomeDocument(models.Model):
    income = models.ForeignKey(
        "Income", on_delete=models.CASCADE, related_name="documents"
    )
    file = models.FileField(
        upload_to="income",
        validators=[validate_file_extension]
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if self.file and not self.pk:
            ext = os.path.splitext(self.file.name)[1]
            new_name = f"{uuid.uuid4()}{ext}"
            self.file.name = os.path.join("income", new_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"IncomeDoc: {self.income.project.name} ({self.file.name})"