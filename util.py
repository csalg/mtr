import pickle

from sklearn.model_selection import train_test_split

from wrangling.DatapointBuilder import DatapointBuilder
from wrangling.DatasetFactory import DatasetFactory


def load_data():
    factory = DatasetFactory(builder_constructor=DatapointBuilder)
    logs    = load_logs()
    factory.add_logs(logs)
    df = factory.create_dataframe_with_all_data_sequence()
    y  = df["inferred_retention_rate"]
    previous_recall_score  = df["previous_recall_score"]

    X  = df.drop(['inferred_retention_rate', "previous_recall_score"], axis=1)
    return X, y, previous_recall_score

def load_data_split(seed=10, test_size=0.1):
    X,y,previous_recall_score = load_data()
    return train_test_split(X, y, previous_recall_score, random_state=seed, test_size=test_size)

def load_logs():
    with open('data/logs.pkl', 'rb') as file:
        logs = pickle.load(file)
    return logs

def swap_columns(df, c1, c2):
    # Swap names
    df.rename({
        c1: c2,
        c2: c1
    }, axis=1, inplace=True)

    # Swap contents
    df['temp'] = df[c1]
    df[c1] = df[c2]
    df[c2] = df['temp']
    df.drop(columns=['temp'], inplace=True)


