from django.contrib import admin
from .models import Doctor, Appointment, TriageForm, Profile

admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(TriageForm)
admin.site.register(Profile)
