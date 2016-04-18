class Question:
    """ Understands: question generated by vandalizer algorithm
    """
    def __init__(self, source_sentence, question, answer, answer_span,
                 question_type, subtype="default",  answer_choices=None):
        self.source_sentence = source_sentence
        self.question = question
        self.answer = answer
        self._type = question_type
        self._subtype = subtype
        self.answer_choices = answer_choices

    def __eq__(self, other):
        if not isinstance(other, Question):
            return False

        if self._type != other._type:
            return False

        return (self.source_sentence == other.source_sentence and
                self.question == other.question and
                self.answer == other.answer)

    def __hash__(self):
        return hash((self.source_sentence, self.question, self._type,
                     self.answer))
