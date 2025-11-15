import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

# Теперь можно импортировать модели
from events.models import NameEvents

# Ваш тестовый код здесь