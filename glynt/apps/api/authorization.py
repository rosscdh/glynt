from tastypie.authorization import Authorization

class OAuthAuthorization(Authorization):
    def is_authorized(self, request, object=None):
        return True

    # Optional but useful for advanced limiting, such as per user.
    # def apply_limits(self, request, object_list):
    #     pass
