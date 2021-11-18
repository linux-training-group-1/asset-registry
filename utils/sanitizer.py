from cerberus import Validator

username_schema = {'type': 'string', 'maxlength': 255}
password_schema = {'type': 'string', 'maxlength': 255}


def validate_user_pass(body):
    schema = {'username': username_schema,
              "password": password_schema}
    validator = Validator(schema)
    return validator.validate(body)
