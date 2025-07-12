# biller/exceptions.py
class BillerAPIError(Exception):
    def __init__(self, status_code, message):
        super().__init__(f"Biller API Error {status_code}: {message}")
        self.status_code = status_code
        self.message = message
