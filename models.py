from flask_mongoengine import Document
from mongoengine import StringField, URLField, BooleanField, ListField, DateTimeField

class Webhook(Document):
    company_id = StringField(required=True)
    url = URLField(required=True)
    headers = StringField()  # Assuming headers as a JSON string
    events = ListField(StringField(), required=True)
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
