from celery import Celery


celery_app = Celery('car_shering')

# загрузка конфигурации селери из модуля
celery_app.config_from_object('celery_config')

# Автоматическая регистрация задач из модуля
celery_app.autodiscover_tasks(['notifications'])
