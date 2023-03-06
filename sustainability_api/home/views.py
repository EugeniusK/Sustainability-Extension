from django.shortcuts import render
from django.http import HttpResponse
from api.models import Cart
from django.db.models import Sum
def home_page(request):
    total_co2_added = Cart.objects.aggregate(Sum('co2e'))['co2e__sum']
    if total_co2_added == None:
        total_co2_added = 0
    context = {
        'total_co2_added': round(total_co2_added, 2),
        'total_number_added': round(int(Cart.objects.count()),2)
    }
    return render(request, 'home/index.html', context)
