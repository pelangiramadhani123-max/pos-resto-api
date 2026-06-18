from django.contrib import admin
from pos_app.models import TableResto, StatusModel, Category, MenuResto
from import_export.admin import ImportExportModelAdmin

# Register your models here.

# admin.site.register(TableResto)
admin.site.register(StatusModel)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
  pass

@admin.register(MenuResto)
class MenuRestoAdmin(ImportExportModelAdmin):
  pass

@admin.register(TableResto)
class TableRestoAdmin(ImportExportModelAdmin):
  pass