from GemmaSentiment import GemmaSentiment

if __name__ == "__main__":
    path_to_model = "path/to/gemma"
    device = "cuda"
    model = GemmaSentiment(path_to_model, device)
    res = model.infer(query="We are so happy that you were able to come to the party. I could hear the children's happy laughter in the other room.")
    print(res)