from django.shortcuts import render

# Create your views here.
def claims_list(request):
    return render(request, 'claims/claims_list.html')

def claim_detail(request, claim_id):
    return render(request, 'claims/claim_detail.html', {'claim_id': claim_id})
