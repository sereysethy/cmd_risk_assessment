import torch
import torch.nn as nn
from tqdm.notebook import tqdm

from transformers import AutoModel

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, model_ckpt):
        super(MLP, self).__init__()
        self.l1 = AutoModel.from_pretrained(model_ckpt)
        self.pre_classifier = torch.nn.Linear(input_size, hidden_size)
        self.dropout = torch.nn.Dropout(0.3)
        self.classifier = torch.nn.Linear(hidden_size, output_size)

    def forward(self, input_ids, attention_mask, token_type_ids):
        output_1 = self.l1(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        hidden_state = output_1[0]
        pooler = hidden_state[:, 0]
        pooler = self.pre_classifier(pooler)
        pooler = torch.nn.ReLU()(pooler)
        pooler = self.dropout(pooler)
        output = self.classifier(pooler)
        return output, output_1