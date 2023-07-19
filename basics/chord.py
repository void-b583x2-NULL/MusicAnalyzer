from note import Note
from harmonics import Harmonic
from enum import Enum
from copy import deepcopy
from typing import Union, List


class Denote3Chord(Enum):
    aug = "增"
    major = "大"
    minor = "小"
    diminished = "减"
    unknown = "无定义"


class Denote7Chord(Enum):
    aug = "增大"
    major = "大"
    minor = "小"
    majorMinor = "大小"
    minorMajor = "小大"
    m7b5 = "半减"
    diminished = "减"
    unknown = "无定义"


class Denote7ChordType(Enum):
    base = "七"
    firstLift = "五六"
    secondLift = "三四"
    thirdLift = "二"


class Denote3ChordType(Enum):
    base = "三"
    firstLift = "六"
    secondLift = "四六"


GLOBAL_MAJOR3 = "大三度"
GLOBAL_MINOR3 = "小三度"


class Chord(object):
    def __init__(self, *notes: Note) -> None:
        super().__init__()
        assert len(notes) in (3, 4), "Only 3 and 7 chords are accpeted"
        self.notes = deepcopy(list(notes))
        self.notes.sort()
        # text,([],[])-chord
        self.prompt, self.relation_type, self.chord_type = self.__computeRelation()

    def __computeRelation(self):
        notes = deepcopy(self.notes)
        lift_idx = 0
        i = 3 if len(notes) == 3 else 7
        judger = (
            Chord.__compute_ordered3_relation
            if i == 3
            else Chord.__compute_ordered7_relation
        )
        while lift_idx < len(notes):
            # test if it can be
            ret_type = judger(*notes)
            if ret_type.name != "unknown":
                break
            # lift
            lift_idx += 1
            notes.insert(0, notes[-1].shift_octave(-1))
            notes.pop()
        if ret_type.name == "unknown":
            return ret_type.value, ret_type, None
        else:
            # true notes
            lift_prompts = ("base", "firstLift", "secondLift", "thirdLift")
            ChordType = Denote3ChordType if i == 3 else Denote7ChordType
            ctype_ret = ChordType[lift_prompts[lift_idx]]
            return f"{ret_type.value}{ctype_ret.value}和弦", ret_type, ctype_ret

    @staticmethod
    def __compute_ordered3_relation(
        A: Union[Note, str], B: Union[Note, str], C: Union[Note, str]
    ):
        # A<B<C
        low, high = (
            Harmonic.computeRelationBetween(A, B),
            Harmonic.computeRelationBetween(B, C),
        )
        denote = Denote3Chord.unknown
        if low == GLOBAL_MAJOR3:
            if high == GLOBAL_MAJOR3:
                denote = Denote3Chord.aug
            elif high == GLOBAL_MINOR3:
                denote = Denote3Chord.major
        elif low == GLOBAL_MINOR3:
            if high == GLOBAL_MAJOR3:
                denote = Denote3Chord.minor
            elif high == GLOBAL_MINOR3:
                denote = Denote3Chord.diminished
        return denote

    @staticmethod
    def __compute_ordered7_relation(
        A: Union[Note, str],
        B: Union[Note, str],
        C: Union[Note, str],
        D: Union[Note, str],
    ):
        # A<B<C
        low, mid, high = (
            Harmonic.computeRelationBetween(A, B),
            Harmonic.computeRelationBetween(B, C),
            Harmonic.computeRelationBetween(C, D),
        )
        denote = Denote7Chord.unknown
        if low == GLOBAL_MAJOR3:
            if mid == GLOBAL_MAJOR3:
                if high == GLOBAL_MINOR3:
                    denote = Denote7Chord.aug
            elif mid == GLOBAL_MINOR3:
                if high == GLOBAL_MAJOR3:
                    denote = Denote7Chord.major
                elif high == GLOBAL_MINOR3:
                    denote = Denote7Chord.majorMinor
        elif low == GLOBAL_MINOR3:
            if mid == GLOBAL_MAJOR3:
                if high == GLOBAL_MAJOR3:
                    denote = Denote7Chord.minorMajor
                elif high == GLOBAL_MINOR3:
                    denote = Denote7Chord.minor
            elif mid == GLOBAL_MINOR3:
                if high == GLOBAL_MAJOR3:
                    denote = Denote7Chord.m7b5
                elif high == GLOBAL_MINOR3:
                    denote = Denote7Chord.diminished
        return denote

    @staticmethod
    def computeRelationAmong(*notes: Union[Note, str]):
        notes = [(n if isinstance(n, Note) else Note.note(n)) for n in notes]
        return Chord(*notes).prompt


if __name__ == "__main__":
    print(Chord.computeRelationAmong('c1','e1','g1'))
