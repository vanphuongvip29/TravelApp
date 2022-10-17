from datetime import date

from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import mark_safe
from .models import *
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.template.response import TemplateResponse

# Register your models here.

class TourForm(forms.ModelForm):
    note = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Tour
        fields = '__all__'

class ImageTourInline(admin.StackedInline):
    model = ImageTour
    pk_name = 'tour'

class TourAdmin(admin.ModelAdmin):
    model = Tour
    readonly_fields = ['avatar']
    inlines = (ImageTourInline,)
    forms = TourForm

    def avatar(self, obj):
        if obj:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=obj.image.name)
            )

class MyAdminSite(admin.AdminSite):
    site_header = 'TRAVEL APP MANAGEMENT'

    def get_urls(self):
        return [
            path('tour-stats/', self.tour_stats)
        ] + super().get_urls()

    def tour_stats(self,request):
        tour_count = Tour.objects.count()
        booking_total = BookTour.objects.count()
        turnover = Bill.objects.aggregate(
            total_price=Sum('total_price'))['total_price']

        bill_paid_total = Bill.objects.filter(created_date__year=date.today().year).count()


        tour = Tour.objects.all().annotate(t=Count('booktour'))

        labels =[]
        data = []
        for name in tour:
            labels.append(name.name)
            data.append(name.t)



        return TemplateResponse(request,'admin/tour-stats.html',{
            'tour_count':tour_count,
            'booking_total':booking_total,
            'turnover':turnover,
            'bill_paid_total': bill_paid_total,
            'tour' : tour,

            'labels': labels,
            'data': data,


        })

admin_site = MyAdminSite('travel')



admin_site.register(Tour, TourAdmin)
admin_site.register(ImageTour)
admin_site.register(User)
admin_site.register(BookTour)