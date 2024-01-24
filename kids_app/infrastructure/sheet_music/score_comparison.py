import copy
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass

import pretty_midi
from music21 import stream, chord
from music21.note import Note


@dataclass
class MusicSubmission:
    original_stream: stream.Stream
    user_notes: List[pretty_midi.Note]
    tempo: int
    viz_path: Path

    def create_skeleton(self) -> Tuple[List[str], List[float]]:
        stream_notes = self.original_stream.notes
        fractions = []
        original_notes = []
        for note in stream_notes:
            if note.isRest:
                continue
            original_notes.append(note.nameWithOctave)
            fractions.append(note.quarterLength)

        return original_notes, fractions

    def make_viz(self):
        original_notes, fractions = self.create_skeleton()
        stream_error = copy.deepcopy(self.original_stream)

        notes_in_one_sec = self.tempo / 60
        one_time = round(1 / notes_in_one_sec, 2)

        results = []

        for i, _note in enumerate(self.user_notes):
            if i >= len(original_notes):
                break

            error = None
            name = pretty_midi.note_number_to_name(_note.pitch)
            note_time = _note.end - _note.start
            note_fraction = note_time / one_time

            if name != original_notes[i]:
                if i + 1 < len(self.user_notes):
                    next_name = pretty_midi.note_number_to_name(self.user_notes[i + 1].pitch)
                    if next_name == original_notes[i]:
                        continue
                error = "NOTE"
                wrong_note = Note(name, quarterLength=fractions[i])
                wrong_note.style.color = "red"

                orig_note = stream_error.notes[i]
                orig_note.style.color = "green"

                chord_notes = [orig_note, wrong_note]
                chord_element = chord.Chord(chord_notes)

                stream_error.replace(stream_error.notes[i], chord_element)

            elif note_fraction != fractions[i]:
                error = f"DUR_{note_fraction != fractions[i]}"
                stream_error.notes[i].style.color = "yellow"

            results.append({"index": i, "note": name, "duration": note_fraction, "error": error})

        stream_error.write('musicxml', fp=self.viz_path)
        return results
