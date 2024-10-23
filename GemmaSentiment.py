import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig,TrainingArguments
import numpy as np
from tqdm import tqdm
from sklearn.metrics import accuracy_score, precision_score, recall_score
from trl import SFTTrainer
from datasets import Dataset
import os
from peft import LoraConfig
os.environ["WANDB_DISABLED"] = "true"

class GemmaSentiment:
    def __init__(self, path_to_model, device="cuda"):
        self._path_to_model = path_to_model
        self._bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
            )
        
        self._lora_config = LoraConfig(
            r=8,
            target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
            task_type="CAUSAL_LM",
        )

        self._tokenizer = AutoTokenizer.from_pretrained(self._path_to_model)
        self._model = AutoModelForCausalLM.from_pretrained(self._path_to_model, quantization_config=self._bnb_config, device_map="auto")

        self._target_tokens = {
                " Positive": 40695,
                " Negative": 48314,
                " positive": 6222,
                " negative": 8322,
                "Positive": 35202,
                "Negative": 39654,
                "Neutral": 70874,
                " Neutral": 62407,
                "neutral": 56347,
                " neutral": 17120
            }

    @staticmethod
    def _make_prompt(query):
        return f"""### REVIEW:
                {query}

                ### SENTIMENT:
                """
    
    def _prompt_formatter(self, data):
        res = []
        for text, label in zip(data['content'], data['label']):
            content = self._make_prompt(text)
            if label == 1:
                content += "Positive"
            elif label == -1:
                content += "Negative"
            elif label == 0:
                content += "Neutral"
            res.append(content)
        return res

    def infer(self, query):
        prompt = self._make_prompt(query)

        inputs = self._tokenizer.encode(prompt, add_special_tokens=True, return_tensors="pt")
        outputs = self._model.generate(input_ids=inputs.to(self._model.device), max_new_tokens=1, output_scores=True, return_dict_in_generate=True)

        positive_pred = outputs.scores[0][0][self._target_tokens['Positive']]
        negative_pred = outputs.scores[0][0][self._target_tokens['Negative']]
        neutral_pred = outputs.scores[0][0][self._target_tokens['Neutral']]

        positive_pred = positive_pred.cpu()
        negative_pred = negative_pred.cpu()
        neutral_pred = neutral_pred.cpu()

        scores = np.array([positive_pred, negative_pred, neutral_pred])
        probs = np.exp(scores) / np.sum(np.exp(scores))
        
        positive_prob = probs[0]
        negative_prob = probs[1]
        neutral_prob = probs[2]

        if positive_prob >= max(negative_prob, neutral_prob):
            return 1
        if negative_prob >= max(neutral_prob, positive_prob):
            return -1
        if neutral_prob >= max(negative_prob, positive_prob):
            return 0
        else:
            print(positive_prob, negative_prob, neutral_prob)
            return None

    def train(self, train_df):
        train_ds = Dataset.from_pandas(train_df)
        trainer = SFTTrainer(
                    model=self._model,
                    train_dataset=train_ds,
                    args=TrainingArguments(
                        per_device_train_batch_size=4,
                        gradient_accumulation_steps=4,
                        warmup_steps=2,
                        learning_rate=2e-5,
                        num_train_epochs=2,
                        fp16=True,
                        logging_steps=20,
                        output_dir="outputs",
                        optim="paged_adamw_8bit",
                        report_to="none"
                    ),
                    peft_config=self._lora_config,
                    formatting_func=self._prompt_formatter,
                )

        trainer.train()

    def evaluate(self, data):
        contents = data["contents"]
        labels = data["labels"]

        y_pred = []
        y_gt = []

        
        for c,l in tqdm(zip(contents, labels), total=len(contents)):
            predicted_label = self.infer(c)
            if predicted_label is None:
                print("WTF!!!!")
                continue
            y_pred.append(int(predicted_label))
            y_gt.append(int(l))

        accuracy = accuracy_score(y_gt, y_pred)
        precision = precision_score(y_gt, y_pred, average='macro')
        recall = recall_score(y_gt, y_pred, average='macro')

        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
            



if __name__ == "__main__":

    # eval
    print("before finetuning")
    path_to_model = r"C:\Users\ASUS\Desktop\github_projects\gemma-sent-analysis\weights"
    model = GemmaSentiment(path_to_model=path_to_model, device="cuda")
    import pandas as pd
    eval_df = pd.read_csv(r"C:\Users\ASUS\Desktop\github_projects\gemma-sent-analysis\SYNTH_TEST_SENT_DATA_3_CLASSES.csv")
    eval_data = {
        "contents": eval_df["content"].tolist(),
        "labels": eval_df["label"].tolist()
    }
    model.evaluate(eval_data)


    print("after finetuning")
    path_to_model = r"C:\Users\ASUS\Desktop\github_projects\gemma-sent-analysis\outputs\checkpoint-224"
    model = GemmaSentiment(path_to_model=path_to_model, device="cuda")
    import pandas as pd
    eval_df = pd.read_csv(r"C:\Users\ASUS\Desktop\github_projects\gemma-sent-analysis\SYNTH_TEST_SENT_DATA_3_CLASSES.csv")
    eval_data = {
        "contents": eval_df["content"].tolist(),
        "labels": eval_df["label"].tolist()
    }
    model.evaluate(eval_data)



    # fine-tune
    # import pandas as pd
    # train_df = pd.read_csv(r"C:\Users\ASUS\Desktop\github_projects\gemma-sent-analysis\SYNTH_TRAIN_SENT_DATA_3_CLASSES.csv")
    # model.train(train_df)




