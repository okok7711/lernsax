class LoginError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccessDenied(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)