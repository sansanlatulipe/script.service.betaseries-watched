class Authentication:
    def __init__(self, credentials, bearerRepo):
        self.credentials = credentials
        self.bearerRepo = bearerRepo

    def isAuthenticated(self):
        return self.bearerRepo.exists()

    def authenticate(self):
        if self.bearerRepo.exists():
            return True
        if self.credentials:
            return self.bearerRepo.createFromCredentials(
                self.credentials['login'],
                self.credentials['password']
            )
        return False

    def initialize(self):
        return self.bearerRepo.createDeviceToken()

    def finalize(self, device):
        return self.bearerRepo.createFromDevice(device)
