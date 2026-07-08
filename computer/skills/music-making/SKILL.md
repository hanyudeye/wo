---
name: music-making
description: Use when the user requests creating, generating, or composing music, audio, melodies, ringtones, or sound effects — especially instrumental, piano, or ambient pieces
---

# Music Making

## Overview

**Core principle: Always generate MIDI, never synthesize raw WAV/audio with Python.**

Raw audio synthesis with sine waves (even with harmonics) sounds artificial, hollow, and unsettling — users consistently report it as "creepy" or "terrifying." MIDI files use the system's built-in sound fonts and produce real instrument quality.

| Method | User Reaction | File Size | Quality |
|--------|--------------|-----------|---------|
| Raw WAV (pure sine) | "太恐怖了" / "魂都吓没了" | ~6 MB | Terrible, horror-game |
| Raw WAV (harmonics) | Still bad | ~6 MB | Slightly less terrible |
| **MIDI** | "不错" | ~700 bytes | Real piano, device-dependent |

## When to Use

**Use when** user asks for:
- "生成一首音乐" / "create music"
- "写一段旋律" / "write a melody"
- "做个铃声" / "make a ringtone"
- "纯音乐" / "instrumental music"
- Any music/audio generation request, regardless of genre or instrument

**Do NOT use when:**
- User explicitly asks for a specific audio format (MP3, WAV) — still use MIDI and explain why, unless they insist
- User wants sound effects (SFX) rather than music — evaluate case by case
- Task is purely about audio processing/editing of existing files

## Required Tools

```bash
pip install mido
```

Python's standard library `wave` and `array` modules are also used, but these are built-in.

## Core Workflow

### Step 1: Design the Music

Define key elements before writing code:

| Element | Sad Piano Example |
|---------|-------------------|
| Key | C major / A minor |
| Tempo | 60-65 BPM |
| Instrument | Piano (MIDI program 0) |
| Structure | Chords (4 beats each) + Melody on top |
| Mood markers | Minor chords (Am, Em, Dm), slow arpeggios, rests |

### Step 2: Write MIDI Generation Script

Use `mido` with this template structure:

```python
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('track_name', name='Piano'))
track.append(MetaMessage('time_signature', numerator=4, denominator=4))
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(65)))
track.append(MetaMessage('key_signature', key='C'))
track.append(Message('program_change', program=0, time=0))
```

**Note mapping:**
```python
NOTES = {
    'C3': 48, 'D3': 50, 'E3': 52, 'F3': 53, 'G3': 55, 'A3': 57, 'B3': 59,
    'C4': 60, 'D4': 62, 'E4': 64, 'F4': 65, 'G4': 67, 'A4': 69, 'B4': 71,
    'C5': 72, 'D5': 74, 'E5': 76, 'F5': 77, 'G5': 79, 'A5': 81, 'B5': 83,
}
```

**Helper functions:**
```python
TICKS_PER_BEAT = 480

def add_note(track, midi_note, beats, vel=72):
    ticks = int(beats * TICKS_PER_BEAT)
    track.append(Message('note_on', note=midi_note, velocity=vel, time=0))
    track.append(Message('note_off', note=midi_note, velocity=64, time=ticks))

def add_chord(track, notes, beats, vel=60):
    ticks = int(beats * TICKS_PER_BEAT)
    for i, n in enumerate(notes):
        track.append(Message('note_on', note=n, velocity=vel, time=0 if i == 0 else 0))
    for i, n in enumerate(notes):
        track.append(Message('note_off', note=n, velocity=50, time=ticks if i == 0 else 0))
```

**Rest handling:**
```python
# Use a silent note at minimum velocity for rests
ticks = int(beats * TICKS_PER_BEAT)
track.append(Message('note_on', note=60, velocity=1, time=ticks))
track.append(Message('note_off', note=60, velocity=1, time=0))
```

### Step 3: Save and Inform

```python
track.append(MetaMessage('end_of_track'))
mid.save('path/to/output.mid')
```

Tell the user:
- The file location
- That MIDI uses their system's built-in instrument sounds
- They can double-click to play, or open in any music software (VLC, DAW, etc.)

## Sad Piano Recipe (已验证)

| Parameter | Value |
|-----------|-------|
| Key | C major (with minor chord progression) |
| Tempo | 65 BPM |
| Chord progression | C → Am → F → G → Em → Am → Dm → G → C |
| Melody style | Slow, with rests, descending phrases |
| Dynamics | Vel=74 for long notes, 68 for short notes |
| Instrument | Piano (program=0) |

The full working script is at `scripts/gen_sad_music.py`.

## Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Using `wave` module for synthesis | Creepy, hollow sound, user complaints | Use `mido` + MIDI instead |
| Over-complicating the script | Long generation time, bugs | Keep it simple: chords + melody |
| Forgetting `end_of_track` | Corrupted MIDI file | Always append before saving |
| Wrong note mapping | Wrong key, wrong mood | Double-check MIDI note numbers |
| No rest handling | Rushed, no breathing room | Use silent notes for rests |
| Pure sine waves with harmonics | Still sounds artificial | Don't try; MIDI sounds real |

## Red Flags

| Rationalization | Reality |
|----------------|---------|
| "I can make it sound good with enough harmonics" | You can't. Pure sine waves always sound hollow. Use MIDI. |
| "WAV is more portable than MIDI" | MIDI plays on any device. WAV from raw synthesis is unlistenable. |
| "Let me try a different waveform (triangle, square)" | The problem isn't the waveform shape. It's the lack of a real instrument body. MIDI. |
| "I'll spend more time on the envelope" | The envelope is not the main problem. The timbre is. MIDI. |

## Related Skills

- `writing-plans` — for structuring multi-movement pieces
