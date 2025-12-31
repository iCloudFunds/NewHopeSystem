from django.contrib import admin
from core.models.std import Student, DisciplineRecord

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'enrollment_date')
    search_fields = ('student_id', 'user__username', 'user__first_name')

@admin.register(DisciplineRecord)
class DisciplineRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'incident_date', 'action_taken')