class Authentication:
    def __init__(self, logger, bearerRepo):
        self.logger = logger
        self.bearerRepo = bearerRepo

    def isAuthenticated(self):
        isBearerActive = self.bearerRepo.isActive()

        if isBearerActive is None:
            self.logger.yellError('No BetaSeries authentication', 20002)
            self.bearerRepo.reset()
            return False

        return isBearerActive

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
