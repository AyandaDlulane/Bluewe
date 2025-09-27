import os
from dotenv import load_dotenv

load_dotenv()

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

# CORS
ALLOWED_ORIGINS = ["*"]  # In production: ["chrome-extension://your-extension-id"]

# Internationalization
MESSAGES = {
    "en": {
        "login_success": "Login successful!",
        "register_success": "Registration successful!",
        "user_exists": "User already exists",
        "invalid_credentials": "Invalid credentials",
        "invalid_token": "Invalid token",
        "welcome": "Welcome",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "register": "Register"
    },
    "es": {
        "login_success": "¡Inicio de sesión exitoso!",
        "register_success": "¡Registro exitoso!",
        "user_exists": "El usuario ya existe",
        "invalid_credentials": "Credenciales inválidas",
        "invalid_token": "Token inválido",
        "welcome": "Bienvenido",
        "username": "Usuario",
        "password": "Contraseña",
        "login": "Iniciar sesión",
        "register": "Registrarse"
    },
    "fr": {
        "login_success": "Connexion réussie!",
        "register_success": "Inscription réussie!",
        "user_exists": "L'utilisateur existe déjà",
        "invalid_credentials": "Identifiants invalides",
        "invalid_token": "Jeton invalide",
        "welcome": "Bienvenue",
        "username": "Nom d'utilisateur",
        "password": "Mot de passe",
        "login": "Connexion",
        "register": "Inscription"
    },
    "zh": {
        "login_success": "登录成功！",
        "register_success": "注册成功！",
        "user_exists": "用户已存在",
        "invalid_credentials": "无效凭证",
        "invalid_token": "无效令牌",
        "welcome": "欢迎",
        "username": "用户名",
        "password": "密码",
        "login": "登录",
        "register": "注册"
    },
    "ar": {
        "login_success": "تم تسجيل الدخول بنجاح!",
        "register_success": "تم التسجيل بنجاح!",
        "user_exists": "المستخدم موجود بالفعل",
        "invalid_credentials": "بيانات الاعتماد غير صالحة",
        "invalid_token": "رمز غير صالح",
        "welcome": "مرحبا",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "register": "تسجيل"
    }
}