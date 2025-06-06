import re
import phonenumbers


REGEX_PASSWORD = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!%*#?&_]{8,}$"

def validate_password_strength(password: str) -> str:
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ValueError('Пароль должен содержать минимум 1 букву, 1 цифру и 1 специальный символ и быть не менее 8 символов!')
    
        return password

def validate_phone_number_format(phone_number: str) -> str:
        try:
            parsed_phone_number = phonenumbers.parse(phone_number, 'RU')
            if not phonenumbers.is_valid_number(parsed_phone_number):
                raise ValueError('Неверный номер телефона!')
            return phonenumbers.format_number(parsed_phone_number, phonenumbers.PhoneNumberFormat.E164)
        except phonenumbers.NumberParseException:
            raise ValueError('Некорректный формат номера телефона!')