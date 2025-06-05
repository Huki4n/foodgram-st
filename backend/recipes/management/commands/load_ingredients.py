import json
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient  # замените на имя вашего приложения


class Command(BaseCommand):
    help = 'Импортирует ингредиенты из JSON и CSV файлов, указанных в settings'

    def handle(self, *args, **kwargs):
        json_path = getattr(settings, 'JSON_FILE_PATH', None)
        csv_path = getattr(settings, 'CSV_FILE_PATH', None)

        if not json_path and not csv_path:
            self.stdout.write(self.style.ERROR('Ни один файл не указан в settings'))
            return

        if json_path:
            self.import_json(json_path)
        if csv_path:
            self.import_csv(csv_path)

        self.stdout.write(self.style.SUCCESS('✅ Импорт успешно завершён'))

    def import_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    Ingredient.objects.get_or_create(
                        name=item['name'],
                        measurement_unit=item['measurement_unit']
                    )
            self.stdout.write(self.style.SUCCESS(f'JSON данные загружены: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка с JSON: {e}'))

    def import_csv(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 2:
                        continue
                    name, unit = row[0].strip(), row[1].strip()
                    Ingredient.objects.get_or_create(
                        name=name,
                        measurement_unit=unit
                    )
            self.stdout.write(self.style.SUCCESS(f'CSV данные загружены: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка с CSV: {e}'))