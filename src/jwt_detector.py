import base64

def is_jwt(token):

    parts = token.split(".")

    if len(parts) != 3:
        return False

    try:

        base64.urlsafe_b64decode(parts[0] + "==")

        base64.urlsafe_b64decode(parts[1] + "==")

        return True

    except:

        return False