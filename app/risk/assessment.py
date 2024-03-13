import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from transformers import AutoTokenizer

from .model import MLP


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
cpu = torch.device("cpu")

class RiskAssessment():
    """
    This class will load a trained risk assessment model which will assess
    a risk associated to a command.
    """

    def __init__(self, config:dict)->None:
        self.max_len = config["token_max_length"]
        self.bert_model = config["pre_trained_model_checkpoint"]
        self.model_path = config["risk_model_path"]
        self.input_size = config["input_size"]
        self.hidden_size = config["hidden_size"]
        self.output_size = config["output_size"]

        # create a model
        self.model = self.make_model(self.input_size, self.hidden_size, \
                                    self.output_size, self.bert_model)

        # initialized from a trained model
        self.load_trained_model(self.model_path)

        self.tokenizer = self.get_tokenizer(self.bert_model)

    def make_model(self, input_size: int, hidden_size:int, output_size:int,\
                    bert_model: str):
        model = MLP(input_size, hidden_size, output_size, bert_model)

        return model

    def get_tokenizer(self, model_ckpt):
        tokenizer = AutoTokenizer.from_pretrained(model_ckpt)

        return tokenizer

    def tokenize(self, text):
        inputs = self.tokenizer(text,
                    add_special_tokens=True,
                    truncation=True,
                    max_length=self.max_len,
                    padding='max_length',
                    return_token_type_ids=True)

        ids = inputs['input_ids']
        mask = inputs['attention_mask']
        token_type_ids = inputs["token_type_ids"]

        return {
            'ids': torch.tensor(ids, dtype=torch.long),
            'mask': torch.tensor(mask, dtype=torch.long),
            'token_type_ids': torch.tensor(token_type_ids, dtype=torch.long)
        }

    def load_trained_model(self, model_path)->None:
        if torch.cuda.is_available():
            checkpoint = torch.load(model_path)
        else:
            checkpoint = torch.load(model_path, map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['model_state_dict'])

    def get_risk(self, cmd: list)->dict[list[float], float, list[float]]:
        risk_level = 0.
        prob = 0.
        pooler = None

        self.model.eval()

        with torch.no_grad():
            data = self.tokenize(cmd)
            ids = data['ids'].to(device, dtype = torch.long)
            mask = data['mask'].to(device, dtype = torch.long)
            token_type_ids = data['token_type_ids'].to(device, dtype = torch.long)

            # Forward pass
            outputs, output_1 = self.model(ids, mask, token_type_ids)
            # output_1 = encoder(**inputs)

            predicted_probs = F.softmax(outputs, dim=1)
            top_probs, top_classes = predicted_probs.topk(1, dim=1)

            hidden_state = output_1[0]
            pooler = hidden_state[:, 0].numpy().tolist()

            risk_level = outputs.argmax(1).cpu()
            risk_level = F.one_hot(risk_level,
                                  num_classes=self.output_size).numpy().tolist()

            prob = top_probs.squeeze().cpu().numpy().tolist()

        return {
            "risk_level": risk_level[0],
            "probability": prob,
            "embedding": pooler[0]
        }