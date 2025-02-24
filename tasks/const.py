CANCELED = 'canceled'
EXPIRED = 'expired'
ACTIVE = 'active'
HIGH = 'high'
MEDIUM = 'medium'
LOW = 'low'

STATUS_CHOICES = [
    (CANCELED, 'Canceled'),
    (EXPIRED, 'Expired'),
    (ACTIVE, 'Active'),
]

PRIORITY_CHOICES = [
    (HIGH, 'High'),
    (MEDIUM, 'Medium'),
    (LOW, 'Low'),
]

MSG = "Истекшие задачи:\n{}"
