from django.shortcuts import render
from results.models import Result
from laba_3.models import Laba3Result

def index(request):
    results = Result.objects.filter(user=request.user).order_by('-id')
    laba_3 = Laba3Result.objects.filter(user=request.user).order_by('-id')
    return render(request, 'results/index.html', {'results': results, 'laba_3': laba_3})

# Create your views here.
