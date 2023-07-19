from note import Note, NOTE_MAX
from enum import Enum
from cn2an import an2cn
from typing import Union


class DenoteRelation(Enum):
    doubleSharp = "倍增"
    sharp = "增"
    major = "大"
    harmonic = "纯"
    minor = "小"
    diminished = "减"
    doubleDiminished = "倍减"
    unknown = "未知"


ORDERED_RELATION_DENOTES = ["", "增", "倍增", "倍减", "减", "小"]  # sep：3/4
HARMONIC_DIFFERENCE = [1, 4, 5]
CRITERION_LIST = [0, 0, 2, 4, 5, 7, 9, 11]  # num of half stages for criterion judge


# Define various chords
class Harmonic(object):
    def __init__(self, A: Note, B: Note) -> None:
        super().__init__()
        if A > B:
            A, B = B, A
        self.firstNote = A
        self.secondNote = B
        self.prompt, self.relation_type, self.deg_diff = self.__computeRelation()

    def __computeRelation(self):
        deg_diff_ = self.firstNote - self.secondNote
        deg_diff = (deg_diff_ - 1) % 7 + 1
        incrementer = int(self.secondNote) - int(self.firstNote)

        if (
            incrementer < 0
        ):  # This kind of harmonics is something in reversed type, and we should take them as <unk>
            denote_relation = "未知"
        else:
            incrementer = incrementer % NOTE_MAX

            criteria_index = incrementer - CRITERION_LIST[deg_diff]
            if deg_diff == 7 and criteria_index <= -10:  # special for aug7 and doubleaug7
                criteria_index += NOTE_MAX
            if deg_diff in HARMONIC_DIFFERENCE:
                # harmonic chords and variances
                if criteria_index == 0:
                    denote_relation = "纯"
                elif abs(criteria_index) < 3:
                    denote_relation = ORDERED_RELATION_DENOTES[:-1][criteria_index]
                else:
                    denote_relation = "未知"
            else:
                # non-harmonic chords and variances
                if criteria_index == 0:
                    denote_relation = "大"
                elif abs(criteria_index) < 3 or criteria_index == -3:
                    denote_relation = ORDERED_RELATION_DENOTES[criteria_index]
                else:
                    denote_relation = "未知"

        relation_type = DenoteRelation(denote_relation)

        return f"{relation_type.value}{an2cn(deg_diff_)}度", relation_type, deg_diff_

    def __str__(self):
        return self.prompt

    @staticmethod
    def computeRelationBetween(A: Union[Note, str], B: Union[Note, str]):
        if isinstance(A, str):
            A = Note.note(A)
        if isinstance(B, str):
            B = Note.note(B)
        return str(Harmonic(A, B))


if __name__ == "__main__":
    Test_cases = [("c1", "#b1"), ("c1", "md1"), ("c1", "b1")]
    for test in Test_cases:
        ret = Harmonic.computeRelationBetween(*test)
        print(ret)
