from django.contrib import admin
# from dbUsersModel.models import userInfo, Contact, Tag

from dbUsersModel.models import userInfo

# Register your models here.

# admin.site.register([userInfo, Contact, Tag])
admin.site.register([userInfo])


# class ContactAdmin(admin.ModelAdmin):
#     fields = ('name', 'email')

# admin.site.register(Contact, ContactAdmin)
# admin.site.register([userInfo, Tag])