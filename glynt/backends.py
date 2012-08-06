from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import email_re

class EmailOrUsernameBackend(ModelBackend):
    """Allows a user to login using their email address, and not just their
    username. This is a lot more common than a new username. Some things that
    it takes care of for you are:

    - Allow _either_ username or email to be used
    - Allow anyone marked as staff in the database to mascquerade as another
      user by using the user they want to masquerade as as the username and
      using <username>/<password> in the password field, where <username>
      is _their_ username."""

    def _lookup_user(self, username):
        try:
            if email_re.search(username):
                # Looks like an email. Since emails are not case sensitive
                # and many users have a habit of typing them in mixed
                # cases, we will normalize them to lower case. This assumes
                # that the database has done the same thing.
                user = User.objects.get(email=username.lower())
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
                return None

        return user
            
    def authenticate(self, username=None, password=None):
        user = self._lookup_user(username)

        if user:
            if user.check_password(password):
                return user
            elif '/' in password:
                proposed_user = user    # Who we want to be
                (username, password) = password.split('/', 1)
                user = self._lookup_user(username)
                if user and user.is_staff:
                    if user.check_password(password):
                        return proposed_user
        return None

