from flask import Flask, request
from flask_restful import Api, Resource
from flask_pymongo import PyMongo
from celery import Celery
from tasks import execute_webhook
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://0.0.0.0:27017/webhook'
mongo = PyMongo(app)

api = Api(app)

class WebhookResource(Resource):
    def post(self):
        data = request.get_json()
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        mongo.db.webhooks.insert_one(data)
        return {"message": "Webhook created successfully"}, 201

    def patch(self, id):
        data = request.get_json()
        data['updated_at'] = datetime.utcnow()
        mongo.db.webhooks.update_one({"_id": id}, {"$set": data})
        return {"message": "Webhook updated successfully"}

    def delete(self, id):
        mongo.db.webhooks.delete_one({"_id": id})
        return {"message": "Webhook deleted successfully"}

    def get(self):
        webhooks = mongo.db.webhooks.find()
        return {"webhooks": list(webhooks)}

class WebhookDetailResource(Resource):
    def get(self, id):
        webhook = mongo.db.webhooks.find_one({"_id": id})
        return {"webhook": webhook}

class EventResource(Resource):
    def post(self):
        company_id = "your_demo_company_id"  # Hardcoded for demo
        webhooks = mongo.db.webhooks.find({"company_id": company_id, "is_active": True})
        for webhook in webhooks:
            execute_webhook.apply_async(args=[webhook['url'], webhook.get('headers', {})])
        return {"message": "Event fired successfully"}

api.add_resource(WebhookResource, '/webhooks/')
api.add_resource(WebhookDetailResource, '/webhooks/<string:id>')
api.add_resource(EventResource, '/fire-event/')

if __name__ == '__main__':
    app.run(debug=True)
