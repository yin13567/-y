from django.contrib import admin
from . import models


# Register your models here.
class stationAdmin(admin.ModelAdmin):
    list_display = ("name",)

class trainlineAdmin(admin.ModelAdmin):
    list_display = ("trainnum","startplace","starttime","endplace","endtime",)

class singlelineAdmin(admin.ModelAdmin):
    list_display = ("startplace","starttime","endplace","endtime","trainline","seq")

class ticketkindAdmin(admin.ModelAdmin):
    list_display = ("name","num","price","startplace","startplaceseq","endplace","endplaceseq",)


admin.site.register(models.Station, stationAdmin)
admin.site.register(models.TrainLine,trainlineAdmin)
admin.site.register(models.SingleLine,singlelineAdmin)
admin.site.register(models.TicketKind,ticketkindAdmin)
