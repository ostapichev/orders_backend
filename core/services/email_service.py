import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.dataclasses.user_dataclass import UserDataClass
from core.services.jwt_service import ActivateToken, JWTService


class EmailService:
    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        content = template.render(context)
        message = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_NAME'), to=[to])
        message.attach_alternative(content, 'text/html')
        message.send()

    @classmethod
    def test_email(cls):
        cls.__send_email('ytoxos@gmail.com', 'test_email.html', {}, 'Hello')

    @classmethod
    def register_email(cls, user: UserDataClass):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email(user.email, 'register.html', {'name': user.profile.name, 'url': url}, 'Register')
