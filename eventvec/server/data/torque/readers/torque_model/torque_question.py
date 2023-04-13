from eventvec.server.data.torque.readers.torque_model.torque_events_answer import TorqueEventsAnswer

class TorqueQuestion:
    def __init__(self):
        self._question = None
        self._answer = None

    def answer(self):
        return self._answer

    def question(self):
        return self._question

    def set_answer(self, answer):
        self._answer = answer

    def set_question(self, question):
        self._question = question

    @staticmethod
    def from_dict(val):
        question = TorqueQuestion()
        question.set_answer(TorqueEventsAnswer.from_dict(val['answer']))
        question.set_question(val['question'])
        return question
    
    @staticmethod
    def from_eval_dict(k, v):
        question = TorqueQuestion()
        question.set_answer(TorqueEventsAnswer.from_dict(v['answer']))
        question.set_question(k)
        return question

    def to_dict(self):
        return {
            "answer": self.answer().to_dict(),
            "question": self.questions(),
        }
