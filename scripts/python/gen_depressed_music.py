from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name='Piano'))
track.append(MetaMessage('time_signature', numerator=4, denominator=4))
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(55)))
track.append(MetaMessage('key_signature', key='Am'))
track.append(Message('program_change', program=0, time=0))

NOTES = {
    'A2': 45, 'D2': 38, 'E2': 40, 'F2': 41, 'G2': 43,
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

def add_chord(chord, beats, vel=55):
    ticks = int(beats * TICKS_PER_BEAT)
    for i, n in enumerate(chord):
        track.append(note_on(n, vel, 0 if i == 0 else 0))
    for i, n in enumerate(chord):
        track.append(note_off(n, 50, ticks if i == 0 else 0))

def rest(beats):
    ticks = int(beats * TICKS_PER_BEAT)
    track.append(note_on(NOTES['C4'], 1, ticks))
    track.append(note_off(NOTES['C4'], 1, 0))

# Bass line — descending, heavy
BASS = [
    ('A2', 4), ('A2', 4),
    ('D2', 4), ('D2', 4),
    ('E2', 4), ('E2', 4),
    ('A2', 4), ('A2', 4),
    ('F2', 4), ('F2', 4),
    ('G2', 4), ('G2', 4),
    ('A2', 4), ('A2', 4),
    ('D2', 4), ('D2', 4),
    ('E2', 4), ('E2', 4),
    ('A2', 4), ('A2', 4),
]

for note_name, beats in BASS:
    n = NOTES[note_name]
    add_note(n, beats, 50)

# Chord progression — all minor, oppressive
CHORDS = [
    ('A3', 'C4', 'E4'),
    ('A3', 'C4', 'E4'),
    ('D3', 'F3', 'A3'),
    ('D3', 'F3', 'A3'),
    ('E3', 'G3', 'B3'),
    ('E3', 'G3', 'B3'),
    ('A3', 'C4', 'E4'),
    ('A3', 'C4', 'E4'),
    ('F3', 'A3', 'C4'),
    ('F3', 'A3', 'C4'),
    ('G3', 'B3', 'D4'),
    ('G3', 'B3', 'D4'),
    ('A3', 'C4', 'E4'),
    ('A3', 'C4', 'E4'),
    ('D3', 'F3', 'A3'),
    ('D3', 'F3', 'A3'),
    ('E3', 'G3', 'B3'),
    ('E3', 'G3', 'B3'),
    ('A3', 'C4', 'E4'),
    ('A3', 'C4', 'E4'),
]

for chord in CHORDS:
    chord_midi = [NOTES[n] for n in chord]
    add_chord(chord_midi, 4, 50)

# Melody — slow, descending, lots of rests, dark intervals
MELODY = [
    ('E4', 2, 68), ('D4', 1, 62), ('C4', 1, 62),
    ('B3', 2, 66), (None, 1), ('C4', 1, 60),
    ('A3', 3, 68), (None, 1),
    ('E4', 1, 62), ('D4', 1, 62), ('C4', 1, 62), ('B3', 1, 60),
    ('A3', 2, 66), (None, 2),
    ('G3', 2, 64), ('A3', 1, 60), ('B3', 1, 60),
    ('C4', 2, 66), ('D4', 1, 62), ('C4', 1, 60),
    ('B3', 2, 64), (None, 1), ('G3', 1, 58),
    ('A3', 3, 68), (None, 1),
    ('F4', 1, 62), ('E4', 1, 62), ('D4', 1, 60), ('C4', 1, 58),
    ('B3', 2, 64), (None, 1), ('G3', 1, 58),
    ('A3', 3, 66), (None, 1),
    ('E4', 2, 68), ('D4', 1, 62), ('C4', 1, 60),
    ('B3', 2, 64), ('C4', 1, 60), ('D4', 1, 60),
    ('C4', 2, 66), ('B3', 1, 58), ('A3', 1, 58),
    ('A3', 4, 70),
]

for item in MELODY:
    note_name = item[0]
    beats = item[1]
    if note_name is not None:
        n = NOTES[note_name]
        vel = item[2]
        add_note(n, beats, vel)
    else:
        rest(beats)

track.append(MetaMessage('end_of_track'))

filepath = '/mnt/d/me/music/depressed_piano.mid'
mid.save(filepath)
print(f'Done: {filepath}')
