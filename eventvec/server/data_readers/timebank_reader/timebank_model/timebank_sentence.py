
from eventvec.server.data_readers.timebank_reader.timebank_model.timebank_enamex import TimebankEnamex  # noqa
from eventvec.server.data_readers.timebank_reader.timebank_model.timebank_event import TimebankEvent  # noqa
from eventvec.server.data_readers.timebank_reader.timebank_model.timebank_numex import TimebankNumex  # noqa
from eventvec.server.data_readers.timebank_reader.timebank_model.timebank_signal import TimebankSignal  # noqa 
from eventvec.server.data_readers.timebank_reader.timebank_model.timebank_text_segment import TimebankTextSegment  # noqa
from eventvec.server.data_readers.timebank_reader.timebank_model.timebank_timex import TimebankTimex  # noqa


class TimebankSentence:
    def __init__(self):
        self._sequence = []

    def sequence(self):
        return self._sequence

    def append(self, item):
        self._sequence.append(item)

    @staticmethod
    def from_bs_obj(sentence, timebank_document):
        timebank_sentence = TimebankSentence()
        children = list(sentence.children)
        creators = {
            'event': TimebankEvent,
            'enamex': TimebankEnamex,
            'numex': TimebankNumex,
            'signal': TimebankSignal,
            'timex3': TimebankTimex,
            'text_segment': TimebankTextSegment,
        }
        for c in children:
            creator = creators.get(c.name, creators['text_segment'])
            obj = creator.from_bs_obj(c)
            timebank_sentence.append(obj)
            if c.name == 'event':
                timebank_document.add_eid2event(obj.eid(), obj)
        return timebank_sentence

    def to_dict(self):
        return [
            i.to_dict() for i in self.sequence()
        ]
