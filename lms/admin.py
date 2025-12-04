from django.contrib import admin
from .models import User, Course, Enrollment

admin.site.register([User, Course, Enrollment])
