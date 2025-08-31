from datetime import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand
import csv, json, os
from claims.models import Claims, ClaimDetail

class Command(BaseCommand):
    help = "Import claims and claim details from a CSV or JSON file"

    def add_arguments(self, parser):
        parser.add_argument('--claims', type=str, help="Path to claims CSV or JSON")
        parser.add_argument('--details', type=str, help="Path to claim details CSV or JSON")

    def handle(self, *args, **options):
        claims_path = options['claims']
        details_path = options['details']

        for f in [claims_path, details_path]:
            if not os.path.exists(f):
                self.stdout.write(self.style.ERROR(f"File {f} does not exist"))
                return

        self.stdout.write(f"Importing claims from {claims_path}")
        self.import_claims(claims_path)

        self.stdout.write(f"Importing claim details from {details_path}")
        self.import_details(details_path)

        self.stdout.write(self.style.SUCCESS("Import completed"))

    def import_claims(self, claims_path):
        data = self.load_file(claims_path)
        for row in data:
            try:
                claim, created = Claims.objects.get_or_create(
                    claim_id=row['id'],
                    defaults={
                        "patient_name": row['patient_name'],
                        "billed_amount": Decimal(row.get('billed_amount')),
                        "paid_amount": Decimal(row.get('paid_amount')),
                        "status": row['status'],
                        "insurer_name": row['insurer_name'],
                        "discharge_date": datetime.strptime(row.get('discharge_date'), '%Y-%m-%d').date()
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created claim {claim.claim_id}"))
                else:
                    self.stdout.write(f"Claim {claim.claim_id} already exists")
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error importing claim {row['id']}: {e}"))

    def import_details(self, details_path):
        data = self.load_file(details_path)
        for row in data:
            try:
                claim = Claims.objects.get(claim_id=row['claim_id'])
                ClaimDetail.objects.get_or_create(
                    detail_id=row['id'],
                    defaults={
                        "claim_id": claim,
                        "cpt_codes": row['cpt_codes'],
                        "denial_reason": row['denial_reason']
                    }
                )
                self.stdout.write(f"Added detail {row['id']} for claim {row['claim_id']}")
            except Claims.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Claim {row['claim_id']} does not exist"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error importing claim detail {row['id']}: {e}"))
        

    def load_file(self, file_path):
        if file_path.endswith('.csv'):
            with open(file_path, 'r') as file:
                return list(csv.DictReader(file, delimiter='|'))
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as file:
                return json.load(file)
        return []