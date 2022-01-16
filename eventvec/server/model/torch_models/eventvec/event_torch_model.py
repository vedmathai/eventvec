import torch.nn as nn 
import torch


class EventModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, device):
        super(EventModel, self).__init__()
        self.i2o = nn.Linear(input_size * 3, output_size, device=device)
        self.dropout = nn.Dropout(0.1)

    def forward(self, verb_vector, subject_vector, object_verb):
        input_combined = torch.cat((verb_vector, subject_vector, object_verb), 1)
        output = self.i2o(input_combined)
        output = self.dropout(output)
        return output