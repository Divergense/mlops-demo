import mlflow


class Model:
    def __init__(self, model_name, model_stage):
        # load model from registry
        self.model = mlflow.pyfunc.load_model(f'models:/{model_name}/{model_stage}')

    def predict(self, data):
        return self.model.predict(data)
