class ProcessorRules:
    """
    Verify the configuration doesn't contain any conflicts
    DOCS: `list of goals we have achieved.xlsx' on onedrive
    """
    def __init__(self, config):
        self.config = config
        self.resample_exercise()
        self.generate_frame()
        self.occupied_space()
        self.remove_idle()
        self.default()

    def resample_exercise(self):
        if self.config.resample_exercise:
            if self.config.frame_generator:
                raise ValueError("Cannot generate frames w/ resample exercise on")
            if self.config.occupied_space:
                raise ValueError("Cannot generate occupied space w/ resample exercise on")
            if self.config.default:  # 5 frames
                raise ValueError("Cannot generate 5 frames w/ resample exercise on")

    def generate_frame(self):
        if self.config.frame_generator:
            if self.config.resample_exercise:
                raise ValueError("Cannot resample exercise w/ generate frame on")
            if self.config.occupied_space:
                raise ValueError("Cannot generate occupied space w/ generate frame on")

    def occupied_space(self):
        if self.config.occupied_space:
            if self.config.resample_exercise:
                raise ValueError("Cannot resample exercise w/ occupied space on")
            if self.config.frame_generator:
                raise ValueError("Cannot generate frames w/ occupied space on")
            if self.config.remove_idle:
                raise ValueError("Cannot remove idle frames w/ occupied space on")
            if self.config.default:  # 5 frames
                raise ValueError("Cannot generate 5 frames w/ occupied space on")

    def remove_idle(self):
        if self.config.remove_idle:
            if self.config.occupied_space:
                raise ValueError("Cannot generate occupied space w/ remove idle on")

    def default(self):
        if self.config.default:
            if self.config.resample_exercise:
                raise ValueError("Cannot resample exercise w/ default on")
            if self.config.occupied_space:
                raise ValueError("Cannot generate occupied space w/ default on")
