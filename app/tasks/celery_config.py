from celery.schedules import crontab

broker_url = 'redis://localhost:6379/0'

result_backend = 'redis://localhost:6379/0'

timezone = 'UTC'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

beat_schedule = {
    'check_vehicle_meintainance': {
        'task': 'maintaninance_and_analitics.check_vehicle_maintainance',
        'schedule': crontab(hour=0, minute=0)
    },
    'generate_reports': {
        'task': 'maintaninance_and_analitics.generate_reports',
        'schedule': crontab(hour=1, minute=0, day_of_month='1')
    }
}
