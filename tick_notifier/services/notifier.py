"""Notification service implementations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
import json

from ..db.models import NotificationType

logger = logging.getLogger(__name__)


class NotificationService(ABC):
    """Abstract base class for notification services."""
    
    @abstractmethod
    def send(
        self,
        notification_type: NotificationType,
        recipients: List[str],
        subject: str,
        message: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Send a notification.
        
        Args:
            notification_type: Type of notification (email, sms, etc.)
            recipients: List of recipients
            subject: Notification subject
            message: Notification message body
            metadata: Additional metadata for the notification
        
        Returns:
            True if notification was sent successfully
        """
        pass


class ConsoleNotifier(NotificationService):
    """
    Console-based notification service for development/testing.
    
    Simply logs notifications to console. Replace with real
    implementations (SMTP, Twilio, etc.) in production.
    """
    
    def send(
        self,
        notification_type: NotificationType,
        recipients: List[str],
        subject: str,
        message: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Send notification to console (for testing)."""
        separator = "=" * 60
        
        output = f"""
{separator}
📬 NOTIFICATION SENT
{separator}
Type:       {notification_type.value.upper()}
Recipients: {', '.join(recipients)}
Subject:    {subject or '(no subject)'}
Message:    {message}
Metadata:   {json.dumps(metadata, indent=2) if metadata else '{}'}
{separator}
"""
        print(output)
        logger.info(f"Notification sent: {notification_type.value} to {recipients}")
        return True


class EmailNotifier(NotificationService):
    """
    Email notification service.
    
    This is a placeholder implementation. In production, integrate with:
    - SMTP (smtplib)
    - SendGrid
    - AWS SES
    - Mailgun
    - etc.
    """
    
    def __init__(self, smtp_host: str, smtp_port: int, username: str, password: str):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send(
        self,
        notification_type: NotificationType,
        recipients: List[str],
        subject: str,
        message: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Send email notification."""
        if notification_type != NotificationType.EMAIL:
            raise ValueError(f"EmailNotifier only handles EMAIL, got {notification_type}")
        
        # Placeholder - implement actual SMTP sending here
        logger.info(f"[EMAIL] Would send to {recipients}: {subject}")
        
        # Example implementation with smtplib:
        # import smtplib
        # from email.mime.text import MIMEText
        # 
        # msg = MIMEText(message)
        # msg['Subject'] = subject
        # msg['From'] = self.username
        # msg['To'] = ', '.join(recipients)
        # 
        # with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
        #     server.starttls()
        #     server.login(self.username, self.password)
        #     server.sendmail(self.username, recipients, msg.as_string())
        
        return True


class WebhookNotifier(NotificationService):
    """
    Webhook notification service.
    
    Sends notifications via HTTP POST to configured endpoints.
    """
    
    def send(
        self,
        notification_type: NotificationType,
        recipients: List[str],
        subject: str,
        message: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Send webhook notification."""
        if notification_type != NotificationType.WEBHOOK:
            raise ValueError(f"WebhookNotifier only handles WEBHOOK, got {notification_type}")
        
        # recipients = list of webhook URLs
        payload = {
            "subject": subject,
            "message": message,
            "metadata": metadata,
        }
        
        # Placeholder - implement actual HTTP POST here
        logger.info(f"[WEBHOOK] Would POST to {recipients}: {json.dumps(payload)}")
        
        # Example implementation with requests:
        # import requests
        # 
        # for url in recipients:
        #     response = requests.post(url, json=payload, timeout=30)
        #     response.raise_for_status()
        
        return True


class CompositeNotifier(NotificationService):
    """
    Composite notifier that routes to appropriate service based on type.
    """
    
    def __init__(self):
        self._notifiers: Dict[NotificationType, NotificationService] = {}
        self._fallback = ConsoleNotifier()
    
    def register(self, notification_type: NotificationType, notifier: NotificationService):
        """Register a notifier for a specific type."""
        self._notifiers[notification_type] = notifier
    
    def send(
        self,
        notification_type: NotificationType,
        recipients: List[str],
        subject: str,
        message: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """Route notification to appropriate service."""
        notifier = self._notifiers.get(notification_type, self._fallback)
        return notifier.send(notification_type, recipients, subject, message, metadata)

