"""
	User Defined ERROR RElated to token
"""

class BaseError(Exception):
	pass

class RevokedTokenError(BaseError):
	pass

class EmptyPayloadError(BaseError):
	pass

class SignatureExpiredError(BaseError):
	pass

class InvalidTokenError(BaseError):
	pass