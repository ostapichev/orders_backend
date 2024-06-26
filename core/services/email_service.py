import os

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.dataclasses.user_dataclass import UserDataClass
from core.exception.email_exception import EmailException
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken


class EmailService:
    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject=''):
        template = get_template(template_name)
        content = template.render(context)
        try:
            message = EmailMultiAlternatives(subject, from_email=os.environ.get('EMAIL_HOST_NAME'), to=[to])
            message.attach_alternative(content, 'text/html')
            message.send()
        except (Exception,):
            raise EmailException

    @staticmethod
    def __create_context(user, token_class, link):
        token = JWTService.create_token(user, token_class)
        url = f'http://localhost:3000/{link}/{token}'
        return {
            'name': user.profile.name,
            'url': url
        }

    @classmethod
    def register_email(cls, user: UserDataClass):
        context = cls.__create_context(user, ActivateToken, 'activate')
        cls.__send_email(user.email, 'register.html', context, 'Register')

    @classmethod
    def recovery_email(cls, user: UserDataClass):
        context = cls.__create_context(user, RecoveryToken, 'recovery')
        cls.__send_email(user.email, 'recovery_password.html', context, 'Recovery password')
