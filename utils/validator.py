from cerberus import Validator

username_schema = {'type': 'string', 'maxlength': 255}
password_schema = {'type': 'string', 'maxlength': 255}


def validate_user_pass(username, password):
    user_validator = Validator(username_schema)
    pass_validator = Validator(password_schema)
    return user_validator.validate(username) and pass_validator.validate(password)
