import pyotp


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()
    otp = otp[-4:]
    return otp