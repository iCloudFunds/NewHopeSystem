from django.db import models

class ModuleControl(models.Model):
    module_name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.module_name}: {'Active' if self.is_active else 'Inactive'}"