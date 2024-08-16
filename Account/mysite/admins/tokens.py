from rest_framework_simplejwt.tokens import RefreshToken

class AdminsRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = cls()
        token['admin_id'] = getattr(user, 'admin_id')
        return token
