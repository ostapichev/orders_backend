from core.exception.token_exception import CreateTokenException
from core.services.jwt_service import JWTService, ActivateToken


class CreateTokenService:
    @staticmethod
    def create_token(user):
        try:
            token = str(JWTService.create_token(user, ActivateToken))
            msg = (
                f'Link for activate user {user.profile.surname} created!. '
                f'Push on the button "copy to clipboard", user id: {user.id}.')
        except (Exception,):
            raise CreateTokenException
        data = {
            'token': token,
            'msg': msg
        }
        return data
