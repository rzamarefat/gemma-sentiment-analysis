from GemmaSentiment import GemmaSentiment
import pandas as pd

if __name__ == "__main__":
    path_to_model = "path/to/gemma"
    device = "cuda"
    model = GemmaSentiment(path_to_model, device)
    test_df = pd.read_csv(r"./data/SYNTH_TEST_SENT_DATA_3_CLASSES.csv")
    model.evaluate(test_df)