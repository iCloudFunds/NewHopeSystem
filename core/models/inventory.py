from django.db import models
from core.models.std import Student

class Asset(models.Model):
    item_name = models.CharField(max_length=200)
    total_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.item_name

class Issuance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_issued = models.DateField(auto_now_add=True)
    returned = models.BooleanField(default=False)