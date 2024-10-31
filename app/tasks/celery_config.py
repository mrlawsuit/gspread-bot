from celery.schedules import crontab
from ..database import get_admins_id
import redis

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'UTC'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']

redis_tool = redis.StrictRedis(host='localhost', port=6379, db=1)

beat_schedule = {
    'send_email_weekly_maintenance': {
        'task': 'notifications.send_email_message',
        'schedule': crontab(hour=1, minute=0, day_of_week='sunday'),
        'args': (
            await get_admins_id(),
            'Daily vehicles maintenance',
            f'We need to set maintenances for vehicles: {
                redis_tool.get("vehicles_for_maintenance").decode("utf-8")
            }'
        )
    },
    'check_vehicle_meintainance': {
        'task': 'planing_and_analitics.maintenance_needed',
        'schedule': crontab(hour=0, minute=0, day_of_week='sunday')
    },
    'generate_reports': {
        'task': 'planing_and_analitics.generate_reports',
        'schedule': crontab(hour=1, minute=0, day_of_month=1)
    }
}
