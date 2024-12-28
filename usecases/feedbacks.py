from core.email import client as email_client
from models.requests_model import FeedbackRequest
from models.user_model import Users
from database import db_dependency


def send_feedback_usecase(db: db_dependency, user: dict, content: FeedbackRequest):
    user = db.query(Users).filter(Users.id == user.get('id')).first()
    email_client.send_feedback_email(user_info=user, feedback_content=content.feedback)