from django.contrib import admin
from .models import WorkOrder, Quote


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'quote', 'status', 'opened_at', 'completed_at')
    list_filter = ('status',)
    search_fields = ('quote__id',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "quote":
            kwargs["queryset"] = Quote.objects.filter(status="aprovado")

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
