from celery.schedules import crontab


broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'UTC'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']


beat_schedule = {
    'weekly_send_email_maintenance': {
        'task': 'notifications.send_maintenance_to_admins',
        'schedule': crontab(hour=1, minute=0, day_of_week='sunday')
    },
    'weekly_check_vehicle_meintainance': {
        'task': 'planing_and_analitics.maintenance_needed',
        'schedule': crontab(hour=0, minute=0, day_of_week='sunday')
    },
    'mounthly_generate_reports': {
        'task': 'planing_and_analitics.generate_reports',
        'schedule': crontab(hour=1, minute=0, day_of_month=1)
    }
}
