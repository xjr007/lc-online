def password_valid(password_info):
    if 3 < len(password_info) < 11:
        return True
    else:
        return False


def username_valid(username_info):
    if 1 < len(str(username_info)) < 6:
        return True
    else:
        return False
