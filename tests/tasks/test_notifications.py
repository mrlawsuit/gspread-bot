import sys
import os

module_path = os.path.abspath('/home/oleg/Рабочий стол/shering/shering')
if module_path not in sys.path:
    sys.path.append(module_path)

import pytest
from unittest.mock import AsyncMock, patch, Mock
from app.tasks.notifications import send_email_message
#from app.tasks.notifications import send_email_message
#from ...app.tasks.notifications import send_email_message
#from ...alembic.env import target_metadata


@pytest.mark.asyncio
@patch('app.tasks.notifications.config')
@patch('app.tasks.notifications.database.get_session')
@patch('app.tasks.notifications.database.get_user_by_id_db')
@patch('app.tasks.notifications.aiosmtplib.SMTP')
async def test_send_email_message_success(
    mock_smtp_client,
    mock_get_user_by_id_db,
    mock_get_session,
    mock_config
):
    # Configure mock config
    mock_config.SENDER_EMAIL = 'sender@example.com'
    mock_config.SMTP_HOST = 'smtp.example.com'
    mock_config.SMTP_PORT = 587
    mock_config.SMTP_PASS = 'password'

    # Mock user data
    mock_user = Mock()
    mock_user.email = 'user@example.com'
    mock_get_user_by_id_db.return_value = mock_user

    # Mock database session
    mock_session = AsyncMock()
    mock_get_session.return_value.__aenter__.return_value = mock_session

     # Mock SMTP client
    mock_smtp_instance = AsyncMock()
    mock_smtp_client.return_value = mock_smtp_instance

    # Call the task
    result = await send_email_message(user_id=1, subject='Subject', message='Message')

    # Assertions
    mock_get_user_by_id_db.assert_called_once_with(mock_session, 1)
    mock_smtp_instance.connect.assert_awaited_once()
    mock_smtp_instance.login.assert_awaited_once_with('sender@example.com', 'password')
    mock_smtp_instance.send_message.assert_awaited_once()
    mock_smtp_instance.quit.assert_awaited_once()
    assert result == 'Email sent successfully to receiver.'


@pytest.mark.asyncio
@patch('app.tasks.notifications.database.get_session')
@patch('app.tasks.notifications.database.get_user_by_id_db')
async def test_send_email_message_no_email(
    mock_get_user_by_id_db, 
    mock_get_session
):
    # Mock user without email
    mock_user = Mock()
    mock_user.email = None
    mock_get_user_by_id_db.return_value = mock_user

    # Mock database session
    mock_session = AsyncMock()
    mock_get_session.return_value.__aenter__.return_value = mock_session

    # Call the task and expect an exception (if your code handles this)
    with pytest.raises(Exception):
        await send_email_message(user_id=1, subject='Subject', message='Message')

if __name__ == '__main__':
    print('s')