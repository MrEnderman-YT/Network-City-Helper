from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from base64 import urlsafe_b64encode
import os

# Ваше сообщение, которое вы хотите зашифровать
message = "Это секретное сообщение.".encode('utf-8')  # Сообщение должно быть в байтовом формате

# Конвертируем пароль в байты.
password = b"my_password"  # Пароль можно оставить в байтах, без необходимости повторной кодировки
# Соль, которую вы использовали для создания ключа. Настоятельно рекомендуется генерировать случайную соль.
salt = b'WladimirskiCenraler'  # Это должна быть та же соль, которая использовалась ранее

# Создаем ключ, используя PBKDF2HMAC.
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=480000,
    backend=default_backend()
)

# Генерируем urlsafe base64 ключ.
key = urlsafe_b64encode(kdf.derive(password))

# Создаем шифровальщик с использованием Fernet.
cipher_suite = Fernet(key)

# Зашифровываем сообщение
encrypted_message = cipher_suite.encrypt(message)
print("Зашифрованное сообщение:", encrypted_message)

sha = b'gAAAAABnLN8kZkZJQGAmUX-DS474rrgBJg21E1TxXafevN4bwxCFe6XFPdMjxU3XRbhyaQXfQK7cSQOKqGmtkqva4td5NFWqTUMde9vYBKDKjFSh7_Z9tMqOw1XpKTLvajwKjlEhhsPE'

decrypted_message = cipher_suite.decrypt(sha)
print("Расшифрованное сообщение:", decrypted_message.decode('utf-8'))