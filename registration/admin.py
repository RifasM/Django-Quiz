from django.contrib import admin

# Register your models here.
from .models import Student, Instruction, Test

admin.site.register(Student)
admin.site.register(Instruction)

admin.site.register(Test)
