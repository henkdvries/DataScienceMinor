import pprint

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

from controller.datacontroller import DataController

from ml.models import Models
from ml.logisticregression import LogisticRegressionModel
from ml.svc import SVCModel


class config:
    debug = False
    tables = True
    pp = pprint.PrettyPrinter(indent=4)

    exercises = 5
    workers = 20
    max_chunck_size = 100

    test_size = 0.2
    test_random_state = 42

    if debug:
        basepath = "src/data/cleaned-regrouped-small"
    else:
        basepath = "src/data/cleaned-regrouped"

    model = Models.LOGISTIC_REGRESSION
    # model = Models.SVC


controller = DataController(config)
controller.run()

np_test_data, np_test_indicator = controller.testdata
np_train_data, np_train_indicator = controller.traindata


print('np_test_data', np_test_data.shape)
print('np_test_indicator', np_test_indicator.shape)
print('np_train_data', np_train_data.shape)
print('np_train_indicator', np_train_indicator.shape)

#np_data_scaled = preprocessing.scale(np_data)


# print("Splitting dataset: {min}/{max} randomstate: {random}".format(
#     min=config.test_size, max=1 - config.test_size,
#     random=config.test_random_state))

# data = train_test_split(
#     np_data_scaled, np_indicator, test_size=config.test_size,
#     random_state=config.test_random_state)

# self.X_train, self.X_test, self.y_train, self.y_test
data = [np_train_data, np_test_data, np_train_indicator, np_test_indicator]

print('Using model', config.model.name)

if config.model == Models.LOGISTIC_REGRESSION:
    model = LogisticRegressionModel(data, config,
                                    solver="lbfgs", multi_class="auto",
                                    max_iter=2000)
elif config.model == Models.SVC:
    model = SVCModel(data, config, gamma="auto")

model.train()
model.rapport()
