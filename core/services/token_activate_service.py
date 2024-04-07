from core.services.jwt_service import JWTService, ActivateToken


class CreateTokenService:
    @staticmethod
    def create_token(user):
        return {'token': str(JWTService.create_token(user, ActivateToken))}
