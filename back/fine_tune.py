from GemmaSentiment import GemmaSentiment
import pandas as pd

if __name__ == "__main__":
    path_to_model = "path/to/gemma"
    device = "cuda"
    model = GemmaSentiment(path_to_model, device)
    train_df = pd.read_csv(r"./data/SYNTH_TRAIN_SENT_DATA_3_CLASSES.csv")
    model.train(train_df=train_df)