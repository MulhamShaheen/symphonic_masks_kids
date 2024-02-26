from pathlib import Path
from typing import Union, Optional

import pretty_midi
from basic_pitch.inference import predict


def trim(midi_data: pretty_midi.PrettyMIDI):
    first_note = midi_data.instruments[0].notes[0]
    start_time = first_note.start

    for instrument in midi_data.instruments:
        for i, note in enumerate(instrument.notes):
            note.start -= start_time
            note.end -= start_time

    return midi_data


class BasicPitcher:
    def __init__(self, default_path: Path, data_path: Optional[Path] = None):
        self.default_path = default_path
        self.data_path = data_path

    def __call__(self, audio_file_path: Union[Path, str],
                 output_path: Optional[Union[Path, str]]) -> pretty_midi.PrettyMIDI:
        model_output, midi_data, note_events = predict(audio_file_path,
                                                       onset_threshold=0.6,
                                                       minimum_frequency=130.813,
                                                       maximum_frequency=1278.75)

        if output_path is None:
            output_path = self.default_path
        midi_data = trim(midi_data)
        midi_data.write(output_path)

        return midi_data

    def save_to_data(self, midi_data: pretty_midi.PrettyMIDI, filename: str,
                     preprocess: bool = True) -> pretty_midi.PrettyMIDI:
        if preprocess:
            midi_data = trim(midi_data)
        midi_data.write(self.data_path / filename)
        return midi_data

    @staticmethod
    def from_file(midi_file_path: Path) -> pretty_midi.PrettyMIDI:
        midi_data = pretty_midi.PrettyMIDI(midi_file_path)

        return midi_data
