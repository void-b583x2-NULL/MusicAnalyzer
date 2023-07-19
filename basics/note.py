# a file for basic music elements
from enum import Enum, IntEnum

A4_FREQ = 440.0  # extend for future frequency related things


class EnumNote(Enum):
    A = 9
    B = 11
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7


NOTE_MAX = 12
FREQ_RATIO = 2 ** (1 / NOTE_MAX)


class EnumPos(Enum):
    A = 5
    B = 6
    C = 0
    D = 1
    E = 2
    F = 3
    G = 4


NOTE_FULL_ORDER = 7


class EnumVariableOfNote(IntEnum):
    unchanged = 0
    sharp = 1
    doubleSharp = 2
    minor = -1
    doubleMinor = -2


SP_CHARS = ["", "#", "x", "m", "u"]  # Corresponding

OFFSET = 0  # TODO: compatible with music21


class Note(object):
    def __init__(
        self,
        note_name: EnumNote,
        octave_group: int,
        varied_denote: EnumVariableOfNote = EnumVariableOfNote.unchanged,
    ) -> None:
        super().__init__()
        self.note_name = note_name
        self.octave_group = octave_group
        self.varied_denote = varied_denote
        self.true_stage = (
            octave_group * NOTE_MAX + note_name.value + varied_denote.value + OFFSET
        )
        self.masked_pos = octave_group * NOTE_FULL_ORDER + EnumPos[note_name.name].value

    @staticmethod
    def __simple_note(u: str, varied_denote=EnumVariableOfNote.unchanged):
        assert len(u) in (1, 2), "Invalid string length for constructing a note"
        if len(u) == 2:
            assert u[1].isdigit(), "Digit is required for denoting a note"
            # Dismiss irrational notes with extreme high/low freq
        note_name = u[0]
        if note_name.lower() == note_name:  # non-captital notes, higher pitch
            octave_group = 3 if len(u) == 1 else int(u[1]) + 3
        else:
            octave_group = 2 if len(u) == 1 else 3 - int(u[1])
        return Note(EnumNote[note_name.upper()], octave_group, varied_denote)

    @staticmethod
    def note(u: str):
        assert len(u) > 0, "Must not be an empty string"
        if u[0] not in SP_CHARS:
            return Note.__simple_note(u)
        else:
            sp_index = SP_CHARS.index(u[0])
            return Note.__simple_note(
                u[1:], EnumVariableOfNote(sp_index if sp_index < 3 else 2 - sp_index)
            )

    def shift_octave(self, shift_octave: int):
        return Note(self.note_name, self.octave_group + shift_octave, self.varied_denote)

    @staticmethod
    def compare(a, b):
        if a.masked_pos == b.masked_pos:
            return 0
        else:
            return -1 if a.masked_pos < b.masked_pos else 1

    # relation ops are regarded as comparing positions on the score
    def __eq__(self, __value) -> bool:
        return Note.compare(self, __value) == 0

    def __sub__(self, __value) -> int:
        return abs(self.masked_pos - __value.masked_pos) + 1

    def __lt__(self, __value) -> bool:
        return Note.compare(self, __value) < 0

    def __gt__(self, __value) -> bool:
        return Note.compare(self, __value) > 0

    def __le__(self, __value) -> bool:
        return Note.compare(self, __value) <= 0

    def __ge__(self, __value) -> bool:
        return Note.compare(self, __value) >= 0

    def __ne__(self, __value) -> bool:
        return not (self == __value)

    def __int__(self) -> int:
        return self.true_stage


if __name__ == "__main__":
    for j in range(6):
        for i_ in "cdefgab":
            if j < 3:
                i = i_.upper()
            else:
                i = i_
            if j in (2, 3):
                res = i
            elif j < 2:
                res = f"{i}{3-j}"
            else:
                res = f"{i}{j-3}"
            n = Note.note(res)
            print(
                f"Construct Note {res}, result in {n.note_name.name}, {n.octave_group}"
            )
