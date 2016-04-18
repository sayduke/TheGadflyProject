from .q_generator_base import QGenerator
import logging
import pickle

logger = logging.getLogger("v.he")
_us_state_dict = pickle.load(open(
    "gadfly/reference_data/_us_state_abbreviations_dict.p", "rb"))
_gpe_dict = pickle.load(open("gadfly/reference_data/_gpe_dict.p", "rb"))


class HeuristicEvaluator:

    def check_titles(answer_span, question, answer_choices):
        if answer_span.label_ == "PERSON":
            logger.debug("check_titles...")
            # print("PERSON", q.answer)
            titles = ["Mr.", "Ms.", "Mrs."]
            words = question.split()
            index = words.index(QGenerator._GAP.strip())-1
            if index >= 0 and words[index] in titles:
                # print("BOOYAH")
                answer_choices = [name.split()[-1] for name
                                  in answer_choices]
        return list(set(answer_choices))

    def remove_apos_s_ans(ent, parsed_sentence):
        if ent.text_with_ws.strip().endswith("'s"):
            logger.debug("remove_apos_s_ans...")
            # we need to change the end pos
            # we need to change the entity
            return ent.end-1, \
                parsed_sentence[ent.start:ent.end-1].text_with_ws.strip()
        return ent.end, ent.text_with_ws.strip()

    def remove_apos_s_choices(other_choices):
        return [choice.replace("'s", "") if choice.endswith("'s") else choice
                for choice in other_choices]

    def gpe_evaluator(other_choices, ent_text):
        # Issue #40
        other_choices = [_us_state_dict[gpe] if gpe in _us_state_dict.keys()
                         else gpe for gpe in other_choices]
        if ent_text in _us_state_dict.keys():
            ent_text = _us_state_dict[ent_text]

        # Issue #41
        if ent_text in _gpe_dict.keys():
            new_choices = []
            alt_type, alts = _gpe_dict[ent_text]
            alt_choices = alts[:]
            for choice in other_choices:
                if choice in _gpe_dict.keys():
                    if _gpe_dict[choice][0] != alt_type:
                        new_choices.append(alt_choices.
                                           pop(0))
                    else:
                        if choice not in new_choices:
                            new_choices.append(choice)
                        else:
                            new_choices.append(
                                    alt_choices.pop(0))
                else:
                    logger.warn("GPE choice not in _gpe_dict: {}"
                                .format(choice))
                    new_choices.append(alt_choices.pop(0))
            other_choices = new_choices
        else:
            logger.warn("GPE not in _gpe_dict: {}".format(ent_text))

        return ent_text, other_choices
