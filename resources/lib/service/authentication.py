class Authentication:
    def __init__(self, bearerRepo):
        self.bearerRepo = bearerRepo

    def isAuthenticated(self):
        return self.bearerRepo.exists()

    def initialize(self):
        return self.bearerRepo.createDeviceToken()

    def finalize(self, device):
        return self.bearerRepo.createFromDevice(device)
