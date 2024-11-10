class Authentication:
    def __init__(self, logger, bearerRepo):
        self.logger = logger
        self.bearerRepo = bearerRepo

    def isAuthenticated(self):
        return self.bearerRepo.exists()

    def initialize(self):
        self.logger.info('Initializing BetaSeries authentication')
        return self.bearerRepo.createDeviceToken()

    def finalize(self, device):
        self.logger.info('Waiting for BetaSeries authentication...')

        authenticated = self.bearerRepo.createFromDevice(device)
        if authenticated:
            self.logger.info('BetaSeries authentication completed')
        else:
            self.logger.error('BetaSeries authentication failed')

        return authenticated
