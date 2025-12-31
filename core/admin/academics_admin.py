from django.contrib import admin
from core.models.academics import Subject, Classroom

class SubjectInline(admin.TabularInline):
    """
    This allows you to add subjects line-by-line 
    directly on the Classroom creation page.
    """
    model = Subject
    extra = 5  # Number of empty rows to show by default
    fields = ('name', 'code')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'department', 'stream', 'capacity')
    list_filter = ('level', 'department', 'stream')
    search_fields = ('name',)
    
    # This puts the Subject rows inside the Classroom form
    inlines = [SubjectInline]

    fieldsets = (
        ('Class Information', {
            'fields': ('name', 'capacity')
        }),
        ('Classification', {
            'fields': ('level', 'department', 'stream'),
        }),
    )

# Optional: Register Subject separately just in case you want to view all subjects globally
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'classroom')
    list_filter = ('classroom__level', 'classroom__department')