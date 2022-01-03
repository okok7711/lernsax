class ConsequentialError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class NotLoggedIn(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class AccessDenied(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class InvalidSession(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class MailError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class FolderNotFound(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class EntryNotFound(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class UnkownError(Exception):
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


def error_handler(errno: str) -> Exception:
    """
    returns an Exception for the given error code
    """
    err_dict = {
        "107": AccessDenied,
        "103": AccessDenied,
        "106": InvalidSession,
        "111": MailError,
        "247": FolderNotFound,
        "117": EntryNotFound,
        "9999": ConsequentialError
    }
    if errno in err_dict:
        return err_dict[errno]
    else:
        return UnkownError
