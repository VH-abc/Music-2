# 19 TET Music System

A Python system for composing and playing music in **19-tone equal temperament (19 TET)**, a microtonal tuning system that divides the octave into 19 equal steps of approximately 63.16 cents each.

## Features

- **Frequency Calculation**: Accurate 19 TET frequency generation from any reference pitch
- **Real-time Audio**: Uses pygame for low-latency audio playback
- **Chord Support**: Play arbitrary chords with any combination of 19 TET degrees
- **Melodic Lines**: Create melodies with precise timing and rhythm
- **Polyphony**: Stack multiple melodic voices with different rhythms
- **ADSR Envelopes**: Configurable attack, decay, sustain, and release for natural-sounding notes
- **Scale Generation**: Built-in patterns for common scales adapted to 19 TET

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the basic demo:
```bash
python tet19_music.py
```

3. Try the advanced examples:
```bash
python examples.py
```

## Basic Usage

### Playing Single Notes

```python
from tet19_music import TET19System

# Initialize the system
tet = TET19System()

# Play degree 0 (reference pitch, default 440 Hz) for 1 second
tet.play_note(0, 1.0)

# Play degree 6 (roughly a major third) for 0.5 seconds
tet.play_note(6, 0.5)

# Clean up
tet.close()
```

### Playing Chords

```python
# Play a triad using degrees 0, 6, and 11
chord_degrees = [0, 6, 11]
tet.play_chord(chord_degrees, 2.0)  # 2 second duration
```

### Creating Melodies with Rhythm

```python
from tet19_music import NoteEvent

# Create a melody with specific timing
melody = [
    NoteEvent(0, 0.5, 0.0),    # Degree 0, 0.5s duration, starts at 0.0s
    NoteEvent(3, 0.5, 0.5),    # Degree 3, 0.5s duration, starts at 0.5s
    NoteEvent(6, 1.0, 1.0),    # Degree 6, 1.0s duration, starts at 1.0s
    NoteEvent(0, 1.0, 2.0),    # Back to degree 0, starts at 2.0s
]

tet.play_melody(melody)
```

### Polyphonic Music

```python
# Create multiple voices
bass_line = [
    NoteEvent(-19, 1.0, 0.0),  # One octave below
    NoteEvent(-12, 1.0, 1.0),
    NoteEvent(-7, 1.0, 2.0),
]

melody_line = [
    NoteEvent(0, 0.5, 0.0),
    NoteEvent(3, 0.5, 0.5),
    NoteEvent(6, 0.5, 1.0),
    NoteEvent(9, 0.5, 1.5),
    NoteEvent(12, 0.5, 2.0),
]

# Play both voices simultaneously
tet.play_polyphonic([bass_line, melody_line])
```

## Understanding 19 TET

19-tone equal temperament divides the octave into 19 equal steps:
- Each step = 1200 cents ÷ 19 ≈ 63.16 cents
- Degree 0 = Reference pitch (default 440 Hz)
- Degree 19 = One octave above the reference
- Negative degrees = Lower octaves
- Degrees > 19 = Higher octaves

### Common Intervals (approximate)
- Degree 1 ≈ Minor semitone (63 cents)
- Degree 2 ≈ Major semitone (126 cents) 
- Degree 3 ≈ Minor whole tone (189 cents)
- Degree 6 ≈ Major third (379 cents)
- Degree 11 ≈ Perfect fifth (695 cents)
- Degree 19 ≈ Octave (1200 cents)

## Advanced Features

### Custom Scales

```python
# Define a custom scale pattern (steps between degrees)
custom_pattern = [3, 2, 3, 3, 2, 3, 3]  # Example pattern
scale_degrees = tet.get_scale_degrees(custom_pattern, root_degree=0)
```

### ADSR Control

```python
# Generate a tone with custom envelope
frequency = tet.tet_to_frequency(6)
wave = tet.generate_tone(
    frequency, 
    duration=2.0,
    attack=0.1,    # 0.1 second attack
    decay=0.2,     # 0.2 second decay  
    sustain=0.6,   # 60% sustain level
    release=0.5    # 0.5 second release
)
```

### Frequency Conversion

```python
# Get the frequency for any 19 TET degree
freq_0 = tet.tet_to_frequency(0)    # Reference frequency
freq_6 = tet.tet_to_frequency(6)    # Major third above
freq_neg12 = tet.tet_to_frequency(-12)  # Below reference
```

## Examples

The `examples.py` file demonstrates:
- Microtonal intervals unique to 19 TET
- Bach-style counterpoint adaptation
- Microtonal chord progressions
- Polyrhythmic compositions
- Various scale explorations

## Theory Background

19 TET is particularly interesting because:
- It provides excellent approximations of just intonation intervals
- The perfect fifth (degree 11) is very close to just (701.96 cents vs 700 cents)
- It offers both major and minor semitones
- Unique intervals not available in 12 TET create new harmonic possibilities
- It's been used by composers like Joel Mandelbaum and Easley Blackwood Jr.

## Requirements

- Python 3.7+
- NumPy (for audio synthesis)
- Pygame (for audio playback)

## License

This project is open source and available under the MIT License.
