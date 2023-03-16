from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        try:
            print(type(user), user)
            attributes = dir(user)
            print(attributes)
            return (
                six.text_type(user) + six.text_type(timestamp)
            )
        except Exception as e:
            print("Exception ", e)
            obj = user.objects.first()
            public_id = getattr(obj, 'public_id')
            username = getattr(obj, 'username')
            print(public_id, username)

            attributes = dir(user)
            print(attributes)
            return (
                six.text_type(public_id) + six.text_type(timestamp) +
                six.text_type(username)
            )
            pass
account_activation_token = TokenGenerator()
