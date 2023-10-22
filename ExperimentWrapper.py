from ExperimentArguments import ExperimentArguments
        
class ExperimentWrapper():
    def __init__(self, raw_arguments):
        """Construtor do ExperimentWrapper"""
        self.experiment_arguments = ExperimentArguments(raw_arguments)
        print(self.experiment_arguments)