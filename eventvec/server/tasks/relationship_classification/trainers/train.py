import numpy as np
import os
from torch import nn
import torch
from tqdm import tqdm
from torch.optim import Adam


from eventvec.server.model.bert_models.bert_relationship_model import BertRelationshipClassifier  # noqa
from eventvec.server.model.llm_tense_pretraining_model.llm_tense_pretrain_model import LLMTensePretrainer  # noqa
from eventvec.server.reporters.report_model.report_model import ReportModel
from eventvec.server.entry_points.train_config_loader.train_config_loader import TrainConfigsLoader
from eventvec.server.tasks.event_vectorization.datahandlers.data_handler_registry import DataHandlerRegistry



TRAIN_SAMPLE_SIZE = int(3000 / 5)
TEST_SAMPLE_SIZE = 100
EPOCHS = 40
LEARNING_RATE = 1e-3  # 1e-2
MOMENTUM = 0.9
WEIGHT_DECAY = 1e-5
CHECKPOINT_PATH = 'local/checkpoints/checkpoint.tar'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SAVE_EVERY = 10000000


class Trainer:
    def __init__(self):
        self._total_loss = 0
        self._all_losses = []
        self._report = ReportModel()
        self._data_handler_registry = DataHandlerRegistry()
        self._train_configs_loader = TrainConfigsLoader()
        self._iteration = 0
        self._last_iteration = 0
        self._loss = None
        self._train_configs = None

    def load(self):
        self._train_configs_loader.load()
        self._train_configs = self._train_configs_loader.train_configs()
        data_handler = 'bert_data_handler'
        self._data_handler = self._data_handler_registry.get_data_handler(data_handler)
        self._data_handler.load()
        self._input_data = self._data_handler.model_input_data()
        self._model = BertRelationshipClassifier(self._train_configs.train_configs()[0])
        self.load_model()
        self._model_optimizer = Adam(
            self._model.parameters(),
            lr=LEARNING_RATE,
        )
        self._criterion = nn.CrossEntropyLoss()
        self._report.set_labels(self._input_data.classes())

    def zero_grad(self):
        self._model.zero_grad()

    def optimizer_step(self):
        self._model_optimizer.step()

    def change_learning_rate(self, lr):
        for g in self._model_optimizer.param_groups:
            print('changing learning rate')
            g['lr'] = lr

    def train_step(self, datum):
        event_predicted_vector = self.classify(datum)
        relationship_target = self.relationship_target(datum)
        event_prediction_loss = self._criterion(
            event_predicted_vector, relationship_target
        )
        relationship_target = self.relationship_target(datum)
        predicted = event_predicted_vector.argmax(dim=1).item()
        current_epoch_stats = self._report.current_epoch()
        current_epoch_stats.record_train_iteration(
            predicted, datum.target(), event_prediction_loss.item()
        )
        if self._loss is None:
            self._loss = event_prediction_loss
        else:
            self._loss += event_prediction_loss
        return event_prediction_loss

    def relationship_target(self, datum):
        relationship_target = np.array([0 for i in range(len(self._input_data.classes()))]).astype(float)
        relationship_target[datum.target()] = 1
        relationship_target = torch.from_numpy(relationship_target).to(device)
        relationship_target = relationship_target.unsqueeze(0)
        return relationship_target

    def classify(self, datum):
        output = self._model(datum)
        return output

    def train_epoch(self):
        if self._iteration == 0:
            self.load_checkpoint()
        self._report.register_new_epoch()
        self.zero_grad()
        train_sample = self._input_data.sample_train_data(TRAIN_SAMPLE_SIZE)
        for datum in tqdm(train_sample):
            loss = self.train_step(datum)
            self._all_losses += [loss.item()]
            self._iteration += 1
            if (self._iteration - self._last_iteration) % SAVE_EVERY == 0:
                self.create_checkpoint()
                self._last_iteration = self._iteration
            if self._loss is not None and self._iteration % 10 == 0:
                self._loss.backward()
                self.optimizer_step()
                self.zero_grad()
                self._loss = None
        self.train_evaluate()
        self.save_model()
        self._report.current_epoch().generate_confusion_heatmaps()
        print(self._report.current_epoch().to_dict())

    def train(self):
        for epoch in range(EPOCHS):
            self._epoch = epoch
            self.train_epoch()

    def train_evaluate(self):
        with torch.no_grad():
            test_sample = self._input_data.sample_test_data(TEST_SAMPLE_SIZE)
            for datumi, datum in enumerate(test_sample):
                if datum.is_trainable():
                    event_predicted_vector = self.classify(datum)
                    relationship_target = self.relationship_target(datum)
                    batch_loss = self._criterion(
                        event_predicted_vector,
                        relationship_target
                    )
                    loss = batch_loss.item()
                    predicted = event_predicted_vector.argmax(dim=1).item()
                    if predicted == 4 and datum.target() == 0:
                        print(
                            ' '.join(datum.from_sentence()),
                            ' '.join(datum.to_sentence()),
                            'expected: {}'.format(datum.target()),
                            'got: {}'.format(predicted),
                        )

                    current_epoch_stats = self._report.current_epoch()
                    current_epoch_stats.record_test_iteration(
                        predicted, datum.target(), loss
                    )

    def save_model(self):
        self._model.save()

    def load_model(self):
        self._model.load()

    def create_checkpoint(self):
        torch.save({
            'iteration': self._iteration,
            'model_state_dict': self._model.state_dict(),
            'optimizer_state_dict': self._model_optimizer.state_dict(),
            'all_losses': self._all_losses,
            }, CHECKPOINT_PATH)
        print('Checkpoint created.')

    def load_checkpoint(self):
        if os.path.exists(CHECKPOINT_PATH):
            checkpoint = torch.load(CHECKPOINT_PATH)
            self._model.load_state_dict(checkpoint['model_state_dict'])

            self._optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

            self._iteration = checkpoint['iteration']
            self._all_losses = checkpoint['all_losses']
            self._model.train()


if __name__ == '__main__':
    trainer = Trainer()
    trainer.load()
    trainer.train()