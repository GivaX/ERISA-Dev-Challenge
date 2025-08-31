from django.shortcuts import render
from .models import Claims

# Create your views here.
def claims_list(request):
    claims = Claims.objects.all()
    return render(request, 'claims/claims_list.html', {'claims': claims})

def claim_detail(request, claim_id):
    return render(request, 'claims/claim_detail.html', {'claim_id': claim_id})
