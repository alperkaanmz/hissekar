import csv
import json
from django.core.management.base import BaseCommand
from core.models import Company
import os

class Command(BaseCommand):
    help = 'Load company data from CSV file'

    def handle(self, *args, **options):
        # CSV dosyasının yolu - doğru lokasyon
        csv_file_path = r'C:\Users\mazin\Desktop\Stella\Playground\playground\capstone\hissekar\data\companies.csv'
        
        self.stdout.write(f"CSV dosyası yolu: {csv_file_path}")
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'CSV dosyası bulunamadı: {csv_file_path}'))
            return
        
        # Mevcut verileri temizle
        Company.objects.all().delete()
        self.stdout.write('Mevcut veriler temizlendi.')
        
        # CSV dosyasını oku
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                try:
                    # JSON verilerini parse et
                    cash_flow = json.loads(row['cash_flow'])
                    income_statement = json.loads(row['income_statement'])
                    balance_sheet = json.loads(row['balance_sheet'])
                    profitability = json.loads(row['profitability'])
                    
                    # Company objesi oluştur
                    company = Company.objects.create(
                        name=row['name'],
                        symbol=row['symbol'],
                        cash_flow=cash_flow,
                        income_statement=income_statement,
                        balance_sheet=balance_sheet,
                        profitability=profitability
                    )
                    
                    self.stdout.write(f'✓ {company.name} ({company.symbol}) başarıyla eklendi.')
                    
                except json.JSONDecodeError as e:
                    self.stdout.write(self.style.ERROR(f'JSON parse hatası {row["name"]}: {e}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Hata {row["name"]}: {e}'))
        
        total_companies = Company.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Toplam {total_companies} şirket başarıyla yüklendi!'))
