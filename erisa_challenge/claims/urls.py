from django.urls import path
from . import views

urlpatterns = [
    path("", views.claims_list, name='claims_list'),
    path("<int:claim_id>/", views.claim_detail, name='claim_detail'),
]