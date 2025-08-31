from django.db import models

# Claim DB Model
class Claims(models.Model):
    claim_id = models.IntegerField(primary_key=True)
    patient_name = models.CharField(max_length=255)
    billed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    insurer_name = models.CharField(max_length=255)
    discharge_date = models.DateField()

    def __str__(self):
        return f"Claim {self.claim_id} - {self.patient_name}"
    
# Claim Detail DB Model
class ClaimDetail(models.Model):
    detail_id = models.IntegerField(primary_key=True)
    claim_id = models.ForeignKey(Claims, on_delete=models.CASCADE, related_name="details")
    cpt_codes = models.TextField()
    denial_reason = models.TextField()

    def __str__(self):
        return f"Claim Detail {self.detail_id} - {self.claim_id.claim_id}"
