from django.contrib import admin
from .models import Course, Enrollment, Assessment, Grade


# Register your models here.
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assessment)
admin.site.register(Grade)
