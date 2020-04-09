from django.contrib import admin
from job_seeker.models import JobSeeker, Resumes, Address, JobApplication
from django.contrib.auth.admin import UserAdmin
from job_seeker.forms import SignUpForm, CustomUserChangeForm
from django.contrib.auth.models import Group

admin.site.register(Resumes)
admin.site.register(Address)
admin.site.register(JobApplication)

class CustomAdmin(UserAdmin):
    add_form = SignUpForm
    form = CustomUserChangeForm
    model = JobSeeker

    list_display = ('email', 'first_name', 'phone', 'is_staff', 'is_active',)
    list_filter  = ('email','is_staff', 'is_active')
    fieldsets = (
        ('Basic info', {'fields': ('email','first_name', 'last_name', 'profession', 'phone', 'dob', 'password') } ),
        ('About', {'fields': ('about',) }),
        ('permissions', {'fields': ('is_staff','is_active','groups', 'user_permissions') } )
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('email', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(JobSeeker, CustomAdmin)
