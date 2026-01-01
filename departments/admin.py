from django.contrib import admin
from .models import Stream, UserProfile, Floor, Message, UserStatus

admin.site.register(Stream)
admin.site.register(UserProfile)
admin.site.register(Floor)
admin.site.register(Message)
admin.site.register(UserStatus)
# Note: Department is now registered in core.admin, so we removed it from here