from django.contrib import admin

from insurance.models import Branch, LifeInsurance


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(LifeInsurance)
class LifeInsuranceAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'branch')
