"""
Advanced examples for the 19 TET Music System
Demonstrates various musical possibilities in 19-tone equal temperament
"""

from tet19_music import TET19System, NoteEvent, SCALE_PATTERNS
import time


def play_microtonal_intervals():
    """Demonstrate the unique microtonal intervals available in 19 TET."""
    print("Playing microtonal intervals unique to 19 TET...")
    
    tet = TET19System()
    
    try:
        # Play various intervals
        intervals = [
            (0, 1, "Minor semitone (~63 cents)"),
            (0, 2, "Major semitone (~126 cents)"),
            (0, 3, "Minor whole tone (~189 cents)"),
            (0, 4, "Major whole tone (~253 cents)"),
            (0, 6, "Minor third (~379 cents)"),
            (0, 7, "Major third (~442 cents)"),
            (0, 11, "Perfect fifth (~695 cents)"),
            (0, 12, "Minor sixth (~758 cents)"),
        ]
        
        for root, interval, name in intervals:
            print(f"  {name}")
            tet.play_note(root, 1.0, blocking=True)
            time.sleep(0.2)
            tet.play_chord([root, interval], 1.5, blocking=True)
            time.sleep(0.5)
    
    finally:
        tet.close()


def play_19tet_bach_style():
    """Play a Bach-style counterpoint example in 19 TET."""
    print("Playing Bach-style counterpoint in 19 TET...")
    
    tet = TET19System()
    
    try:
        # Create a simple two-voice invention-style piece
        # Voice 1 (right hand)
        voice1 = [
            # Measure 1
            NoteEvent(0, 0.25, 0.0, 0.8),     # C
            NoteEvent(3, 0.25, 0.25, 0.7),    # D
            NoteEvent(6, 0.25, 0.5, 0.8),     # E
            NoteEvent(9, 0.25, 0.75, 0.7),    # F#
            # Measure 2
            NoteEvent(12, 0.5, 1.0, 0.9),     # G
            NoteEvent(6, 0.25, 1.5, 0.7),     # E
            NoteEvent(9, 0.25, 1.75, 0.7),    # F#
            # Measure 3
            NoteEvent(12, 0.25, 2.0, 0.8),    # G
            NoteEvent(15, 0.25, 2.25, 0.7),   # A
            NoteEvent(18, 0.25, 2.5, 0.8),    # B
            NoteEvent(19, 0.25, 2.75, 0.7),   # C (next octave)
            # Measure 4
            NoteEvent(12, 1.0, 3.0, 0.9),     # G (resolution)
        ]
        
        # Voice 2 (left hand) - entering later with the same theme transposed
        voice2 = [
            # Measure 2 (entering)
            NoteEvent(-7, 0.25, 1.0, 0.8),    # F (one octave down)
            NoteEvent(-4, 0.25, 1.25, 0.7),   # G
            NoteEvent(-1, 0.25, 1.5, 0.8),    # A
            NoteEvent(2, 0.25, 1.75, 0.7),    # B
            # Measure 3
            NoteEvent(5, 0.5, 2.0, 0.9),      # C
            NoteEvent(-1, 0.25, 2.5, 0.7),    # A
            NoteEvent(2, 0.25, 2.75, 0.7),    # B
            # Measure 4
            NoteEvent(5, 0.25, 3.0, 0.8),     # C
            NoteEvent(8, 0.25, 3.25, 0.7),    # D
            NoteEvent(11, 0.25, 3.5, 0.8),    # E
            NoteEvent(12, 0.25, 3.75, 0.7),   # F
            # Measure 5
            NoteEvent(5, 1.0, 4.0, 0.9),      # C (resolution)
        ]
        
        tet.play_polyphonic([voice1, voice2], blocking=True)
        
    finally:
        tet.close()


def play_microtonal_chord_progression():
    """Demonstrate a chord progression using 19 TET's unique harmonic possibilities."""
    print("Playing microtonal chord progression...")
    
    tet = TET19System()
    
    try:
        # Define chords using 19 TET degrees
        # Each chord is played for 1.5 seconds
        chord_progression = [
            # I chord (root position)
            ([0, 6, 11], "19-TET Major Triad (0-6-11)"),
            
            # ii chord with microtonal third
            ([3, 8, 14], "Minor-ish chord (3-8-14)"),
            
            # V chord with different tuning
            ([11, 17, 22], "Dominant-ish chord (11-17-22)"),
            
            # I chord (different voicing)
            ([0, 11, 19], "Root chord octave spread"),
            
            # Unique 19-TET chord
            ([0, 4, 8, 12], "Quartal harmony"),
            
            # Resolution
            ([0, 6, 11, 19], "Final major chord with octave"),
        ]
        
        for chord_degrees, description in chord_progression:
            print(f"  Playing: {description}")
            tet.play_chord(chord_degrees, 1.5, velocity=0.8, blocking=True)
            time.sleep(0.3)  # Brief pause between chords
    
    finally:
        tet.close()


def play_polyrhythmic_example():
    """Demonstrate polyrhythmic capabilities with different voices in different rhythms."""
    print("Playing polyrhythmic example...")
    
    tet = TET19System()
    
    try:
        # Voice 1: Quarter notes (4/4 time)
        voice1 = []
        for i in range(8):
            degree = [0, 6, 12, 6][i % 4]  # Simple pattern
            voice1.append(NoteEvent(degree, 0.8, i * 1.0, 0.7))
        
        # Voice 2: Triplets (3 against 4)
        voice2 = []
        triplet_duration = 4.0 / 3.0 / 3.0  # 3 triplets per 4/4 measure
        for i in range(12):  # 12 triplets over 4 measures
            degree = [3, 9, 15][i % 3]  # Different pattern
            voice2.append(NoteEvent(degree + 19, triplet_duration * 0.8, i * triplet_duration, 0.6))
        
        # Voice 3: Syncopated bass line
        voice3 = [
            NoteEvent(-19, 1.5, 0.0, 0.8),
            NoteEvent(-12, 0.5, 1.5, 0.6),
            NoteEvent(-8, 1.0, 2.0, 0.7),
            NoteEvent(-19, 1.0, 3.0, 0.8),
            NoteEvent(-15, 2.0, 4.0, 0.8),
            NoteEvent(-19, 2.0, 6.0, 0.9),
        ]
        
        tet.play_polyphonic([voice1, voice2, voice3], blocking=True)
        
    finally:
        tet.close()


def explore_19tet_scales():
    """Explore different scale possibilities in 19 TET."""
    print("Exploring 19 TET scales...")
    
    tet = TET19System()
    
    try:
        scales_to_try = [
            ('major_diatonic', 'Traditional Major Scale Approximation'),
            ('minor_diatonic', 'Traditional Minor Scale Approximation'),
            ('pentatonic', 'Pentatonic Scale'),
            ('whole_tone', 'Whole Tone Scale'),
        ]
        
        for scale_name, description in scales_to_try:
            print(f"  Playing: {description}")
            scale_degrees = tet.get_scale_degrees(SCALE_PATTERNS[scale_name], root_degree=0)
            
            # Play scale ascending
            for degree in scale_degrees:
                tet.play_note(degree, 0.4, velocity=0.7, blocking=True)
            
            # Play scale descending
            for degree in reversed(scale_degrees):
                tet.play_note(degree, 0.4, velocity=0.7, blocking=True)
            
            time.sleep(0.5)
        
        # Custom 19-TET scale that uses unique intervals
        print("  Playing: Custom 19-TET scale with unique intervals")
        custom_scale = [0, 2, 5, 7, 10, 13, 16, 18]  # Uses both semitone types and other intervals
        
        for degree in custom_scale:
            tet.play_note(degree, 0.5, velocity=0.8, blocking=True)
        
    finally:
        tet.close()


def main():
    """Run all examples."""
    print("19 TET Music System - Advanced Examples")
    print("=" * 50)
    print()
    
    examples = [
        ("Microtonal Intervals", play_microtonal_intervals),
        ("Bach-style Counterpoint", play_19tet_bach_style),
        ("Chord Progression", play_microtonal_chord_progression),
        ("Polyrhythmic Music", play_polyrhythmic_example),
        ("Scale Exploration", explore_19tet_scales),
    ]
    
    for name, example_func in examples:
        print(f"Running: {name}")
        print("-" * 30)
        try:
            example_func()
        except Exception as e:
            print(f"Error in {name}: {e}")
        print()
        time.sleep(1)
    
    print("All examples completed!")


if __name__ == "__main__":
    main()
