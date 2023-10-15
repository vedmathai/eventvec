import json
import os
from jadelogs import JadeLogger


class Config:
    _instance = None

    def __init__(self):
        self._pythonpath = None
        self._matres_data_location = None
        self._experiment_type = None
        self._book_corpus_data_location = None
        self._heatmaps_location = None
        self._timebank_dense_data_location = None
        self._te3_silver_data_location = None
        self._te3_gold_data_location = None
        self._te3_platinum_data_location = None
        self._aquaint_data_location = None
        self._tsqa_data_location = None
        self._tsqa_file_names = None
        self._tsqa_file2annotation_map = {}
        self._torque_data_location = None
        self._torque_data_file_names = None
        self._wiki_data_location = None
        self._nyt_data_location = None
        self._hansard_data_location = None
        self._politosphere_data_location = None
        self._mnli_data_location = None
        self._jade_logger = JadeLogger()


    @staticmethod
    def instance():
        if Config._instance is None:
            pythonpath = os.environ['PYTHONPATH']
            config_filepath = os.path.join(pythonpath, 'eventvec/server/config.json')
            with open(config_filepath) as f:
                Config._instance = Config.from_dict(json.load(f))
            Config._instance.set_pythonpath(pythonpath)
        return Config._instance
    
    def pythonpath(self):
        return self._pythonpath

    def matres_data_location(self):
        location = self._jade_logger.file_manager.data_filepath(self._matres_data_location)
        return location

    def set_matres_data_location(self, matres_data_location):
        self._matres_data_location = matres_data_location

    def timebank_data_location(self):
        return self._timebank_data_location

    def run_configs_file(self):
        return self._run_configs_file
    
    def run_configs_abs_filepath(self):
        filepath = os.path.join(self.pythonpath(), self.run_configs_file())
        return filepath

    def experiment_type(self):
        return self._experiment_type

    def book_corpus_data_location(self):
        return self._book_corpus_data_location
    
    def wiki_data_location(self):
        return self._wiki_data_location
    
    def nyt_data_location(self):
        return self._nyt_data_location
    
    def hansard_data_location(self):
        return self._hansard_data_location
    
    def maec_data_location(self):
        return self._maec_data_location
    
    def politosphere_data_location(self):
        return self._politosphere_data_location

    def mnli_data_location(self):
        return self._mnli_data_location

    def model_save_location(self):
        return self._model_save_location

    def heatmaps_location(self):
        return self._heatmaps_location

    def tsqa_data_location(self):
        return self._tsqa_data_location

    def tsqa_file_names(self):
        return self._tsqa_file_names

    def tsqa_file2annotation_map(self):
        return self._tsqa_file2annotation_map

    def torque_abs_data_location(self):
        location = self._jade_logger.file_manager.data_filepath(self._torque_data_location)
        return location

    def torque_data_file_names(self):
        return self._torque_data_file_names
    
    def set_pythonpath(self, pythonpath):
        self._pythonpath = pythonpath

    def set_timebank_data_location(self, timebank_data_location):
        self._timebank_data_location = timebank_data_location

    def timebank_dense_data_location(self):
        if os.environ.get('ENV') == 'JADE':
            location = self._jade_logger.file_manager.data_filepath(self._timebank_dense_data_location)
        else:
            location = self._timebank_dense_data_location
        return location

    def set_timebank_dense_data_location(self, timebank_dense_data_location):
        self._timebank_dense_data_location = timebank_dense_data_location

    def aquaint_data_location(self):
        location = self._jade_logger.file_manager.data_filepath(self._aquaint_data_location)
        return location
    
    def set_aquaint_data_location(self, aquaint_data_location):
        self._aquaint_data_location = aquaint_data_location

    def te3_silver_data_location(self):
        location = self._jade_logger.file_manager.data_filepath(self._te3_silver_data_location)
        return location
    
    def set_te3_silver_data_location(self, te3_silver_data_location):
        self._te3_silver_data_location = te3_silver_data_location

    def te3_platinum_data_location(self):
        location = self._jade_logger.file_manager.data_filepath(self._te3_platinum_data_location)
        return location
    
    def set_te3_platinum_data_location(self, te3_platinum_data_location):
        self._te3_platinum_data_location = te3_platinum_data_location

    def te3_gold_data_location(self):
        location = self._jade_logger.file_manager.data_filepath(self._te3_gold_data_location)
        return location
    
    def set_te3_gold_data_location(self, te3_gold_data_location):
        self._te3_gold_data_location = te3_gold_data_location

    def set_run_configs_file(self, run_configs_file):
        self._run_configs_file = run_configs_file

    def set_experiment_type(self, experiment_type):
        self._experiment_type = experiment_type

    def set_book_corpus_data_location(self, book_corpus_data_location):
        self._book_corpus_data_location = book_corpus_data_location

    def set_wiki_data_location(self, wiki_data_location):
        self._wiki_data_location = wiki_data_location

    def set_nyt_data_location(self, nyt_data_location):
        self._nyt_data_location = nyt_data_location

    def set_hansard_data_location(self, hansard_data_location):
        self._hansard_data_location = hansard_data_location

    def set_maec_data_location(self, maec_data_location):
        self._maec_data_location = maec_data_location

    def set_politosphere_data_location(self, politosphere_data_location):
        self._politosphere_data_location = politosphere_data_location

    def set_mnli_data_location(self, mnli_data_location):
        self._mnli_data_location = mnli_data_location

    def set_model_save_location(self, model_save_location):
        self._model_save_location = model_save_location

    def set_heatmaps_location(self, heatmaps_location):
        self._heatmaps_location = heatmaps_location

    def set_tsqa_data_location(self, tsqa_data_location):
        self._tsqa_data_location = tsqa_data_location

    def set_tsqa_file_names(self, tsqa_file_names):
        self._tsqa_file_names = tsqa_file_names

    def set_tsqa_file2annotation_map(self, tsqa_file2annotation_map):
        self._tsqa_file2annotation_map = tsqa_file2annotation_map

    def set_torque_data_location(self, torque_data_location):
        self._torque_data_location = torque_data_location

    def set_torque_data_file_names(self, torque_data_file_names):
        self._torque_data_file_names = torque_data_file_names

    @staticmethod
    def from_dict(val):
        config = Config()
        config.set_matres_data_location(val.get('matres_data_location'))
        config.set_timebank_data_location(val.get('timebank_data_location'))
        config.set_timebank_dense_data_location(val.get('timebank_dense_data_location'))
        config.set_te3_silver_data_location(val.get('te3_silver_data_location'))
        config.set_te3_gold_data_location(val.get('te3_gold_data_location'))
        config.set_te3_platinum_data_location(val.get('te3_platinum_data_location'))
        config.set_aquaint_data_location(val.get('te3_aquaint_location'))
        config.set_book_corpus_data_location(val.get('book_corpus_data_location'))
        config.set_experiment_type(val.get('experiment_type'))
        config.set_run_configs_file(val.get('run_configs_file'))
        config.set_model_save_location(val.get('model_save_location'))
        config.set_heatmaps_location(val.get('heatmaps_location'))
        config.set_tsqa_data_location(val.get('tsqa_data_location'))
        config.set_tsqa_file_names(val.get('tsqa_file_names'))
        config.set_tsqa_file2annotation_map(val.get('tsqa_file2annotation_map'))
        config.set_torque_data_location(val.get('torque_data_location'))
        config.set_torque_data_file_names(val.get('torque_data_file_names'))
        config.set_wiki_data_location(val.get('wiki_data_location'))
        config.set_nyt_data_location(val.get('nyt_data_location'))
        config.set_hansard_data_location(val.get('hansard_data_location'))
        config.set_maec_data_location(val.get('maec_data_location'))
        config.set_politosphere_data_location(val.get('politosphere_data_location'))
        config.set_mnli_data_location(val.get('mnli_data_location'))
        return config
