from django.contrib import admin

# Register your models here.
from .models import Register, Instruction, Test

admin.site.register(Register)
admin.site.register(Instruction)

admin.site.test(Test)
