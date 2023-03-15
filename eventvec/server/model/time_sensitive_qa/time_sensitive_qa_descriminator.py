import os
import torch.nn as nn
from transformers import BigBirdTokenizer, BigBirdModel
import torch

from eventvec.server.config import Config


class QuestionDescriminatorModel(nn.Module):

    def __init__(self):
        super(QuestionDescriminatorModel, self).__init__()
        config = Config.instance()
        self._tokenizer = BigBirdTokenizer.from_pretrained('google/bigbird-roberta-base')
        self._model = BigBirdModel.from_pretrained('google/bigbird-roberta-base', block_size=16, num_random_blocks=2)
        self._start_classifier_weight = torch.nn.Parameter(torch.randn(768), requires_grad=True)
        self._end_classifier_weight = torch.nn.Parameter(torch.randn(768), requires_grad=True)
        self._discriminator_layer_1 = nn.Linear(768, 20)
        self._relu = nn.ReLU()
        self._discriminator_layer_2 = nn.Linear(20, 2)
        self._softmax = nn.Softmax


    def forward(self, question, paragraph):
        inputs = self._tokenizer([question], [paragraph], return_tensors="pt", padding='longest', max_length=1000)
        print(inputs)
        print(self._tokenizer.convert_ids_to_tokens(inputs.input_ids[0]))
        #labels = torch.tensor([label]).unsqueeze(0)  # Batch size 1
        outputs = self._model(**inputs)
        hidden_states = outputs.last_hidden_state
        start_logits = torch.matmul(hidden_states, self._start_classifier_weight)
        end_logits = torch.matmul(hidden_states, self._end_classifier_weight)
        pooler_output = outputs.pooler_output[0]
        discriminator_layer_output_1 = self._discriminator_layer_1(pooler_output)
        discriminator_layer_output_2 = self._discriminator_layer_2(discriminator_layer_output_1)
        discriminator_output = self._softmax(discriminator_layer_output_2)
        start_output = self._softmax(start_logits)
        end_output = self._softmax(end_logits)
        print(start_output)
        print(dir(self._tokenizer))


if __name__ == '__main__':
    qdm = QuestionDescriminatorModel()
    qdm.forward("batman and veerapanmugalidosan?", 'are the best')