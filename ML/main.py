from cleaner import CleanedDF
from pikl_maker import IsolationForestModel

if __name__ == "__main__":
    cleaned_data = CleanedDF('test.csv')
    cleaned_data.preprocessing()
    cleaned_data.printInfo()

    newModel = IsolationForestModel(cleaned_data.df)
    newModel.train()

    newModel.save_model()
