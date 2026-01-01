from django.db import models
from core.models.std import Student

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=100, unique=True)
    date_paid = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.student_id} - {self.amount_paid}"

class PaymentMethodConfig(models.Model):
    name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)