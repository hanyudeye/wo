from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name='Piano'))
track.append(MetaMessage('time_signature', numerator=4, denominator=4))
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(65)))
track.append(MetaMessage('key_signature', key='C'))
track.append(Message('program_change', program=0, time=0))

NOTES = {
    'C3': 48, 'D3': 50, 'E3': 52, 'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59,
    'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
    'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79, 'A5': 81, 'B5': 83,
}

TICKS_PER_BEAT = 480

def note_on(note, vel=72, time=0):
    return Message('note_on', note=note, velocity=vel, time=time)

def note_off(note, vel=64, time=TICKS_PER_BEAT):
    return Message('note_off', note=note, velocity=vel, time=time)

def add_note(n, beats, vel=72):
    ticks = int(beats * TICKS_PER_BEAT)
    track.append(note_on(n, vel, 0))
    track.append(note_off(n, 64, ticks))

def add_chord(chord, beats, vel=60):
    ticks = int(beats * TICKS_PER_BEAT)
    for i, n in enumerate(chord):
        track.append(note_on(n, vel, 0 if i == 0 else 0))
    for i, n in enumerate(chord):
        track.append(note_off(n, 50, ticks if i == 0 else 0))

CHORDS = [
    ('C3', 'E3', 'G3'),
    ('A3', 'C4', 'E4'),
    ('F3', 'A3', 'C4'),
    ('G3', 'B3', 'D4'),
    ('E3', 'G3', 'B3'),
    ('A3', 'C4', 'E4'),
    ('D4', 'F4', 'A4'),
    ('G3', 'B3', 'D4'),
    ('C4', 'E4', 'G4'),
]

for chord in CHORDS:
    chord_midi = [NOTES[n] for n in chord]
    add_chord(chord_midi, 4, 58)

MELODY = [
    ('E4', 2), ('C4', 1), ('G3', 1),
    ('A3', 2), ('C4', 1), ('E4', 1),
    ('G3', 1), ('B3', 1), ('E4', 1), ('G4', 1),
    ('F4', 2), ('D4', 1), ('B3', 1),
    ('C4', 2), ('E4', 2),
    ('D4', 1), ('B3', 1), ('G3', 1), ('B3', 1),
    ('A3', 2), ('C4', 1), ('E4', 1),
    ('G4', 2), ('F4', 1), ('E4', 1),
    ('C4', 1), ('G3', 1), ('A3', 1), ('B3', 1),
    ('C4', 3), (None, 1),
    ('E4', 2), ('C4', 1), ('G3', 1),
    ('F4', 1), ('E4', 1), ('C4', 1), ('A3', 1),
    ('G3', 2), ('B3', 1), ('D4', 1),
    ('C4', 3), ('G3', 1),
    ('A3', 1), ('C4', 1), ('E4', 1), ('A4', 1),
    ('G4', 2), ('F4', 1), ('D4', 1),
    ('E4', 3), (None, 1),
]

for note_name, beats in MELODY:
    if note_name is not None:
        n = NOTES[note_name]
        vel = 74 if beats >= 2 else 68
        add_note(n, beats, vel)
    else:
        ticks = int(beats * TICKS_PER_BEAT)
        track.append(note_on(NOTES['C4'], 1, ticks))
        track.append(note_off(NOTES['C4'], 1, 0))

track.append(MetaMessage('end_of_track'))

filepath = '/mnt/d/me/music/sad_piano.mid'
mid.save(filepath)
print(f'Done: {filepath}')
