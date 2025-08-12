"""
A simple piece in 19 TET using the specified chord progression
Chord progression: 0-6-11, 0-5-11, 0-5-13, 0-8-13, 0-5-13, 5-13-18, 4-12-18, 1-6-12
"""

from tet19_music import TET19System, NoteEvent, LegatoSequence
import time

def create_chord_progression_piece():
    """Create and play a piece with the specified chord progression and melody"""
    
    # Define the chord progression
    chord_progression = [
        ([0, 6, 11], 1),   
        ([0, 5, 11], 1),  
        ([0, 5, 13], 1),   
        ([0, 6, 11], 1),

        ([0, 8, 13], 1),   
        ([0, 5, 13], 1),   
        ([2, 8, 16], 1),
        ([0, 6, 11], 1),

        ([0, 8, 13], 1),   
        ([0, 5, 13], 1),   
        ([2, 8, 16], 1),
        ([0, 6, 11], 1),

        ([0, 8, 13], 1),
        ([3, 11, 16], 0.25),
        ([2, 10, 15], 0.25),
        ([1, 9, 14], 0.25),
        ([0, 8, 13], 0.25),
        ([-3, 2, 8], 1),
        ([0, 5, 13], 1),

        ([2, 13], 1),
        ([-1, 13], 1),
        ([-1, 5], 1),
        ([0, 11], 1),

        ([0, 8, 13], 1),
        ([0, 5, 13], 1),
        ([5, 13, 18], 1),
        ([5, 13, 19], 1),

        ([5, 13, 18], 1),
        ([4, 12, 18], 1),
        ([1, 6, 12], 1),
        ([0, 6, 11], 1),
        
        ([0, 6, 19, 6+19], 1),
        ([6, 12, 6+19, 12+19], 1),
        ([12, 18, 12+19, 18+19], 1),
        ([12, 12+19, 18+19, 23+19], 1),

        ([13, 13+19, 19+19, 13+19], 1),
        ([12, 12+19, 18+19, 12+19], 1),
        ([11, 11+19, 19+19, 11+19], 2),


        # ([5, 13, 18], 1),  
        # ([4, 12, 18], 1),  
        # ([1, 6, 12], 1),   

        # ([0, 8, 13], 1),
        # ([0, 5, 13], 1),
        # ([5, 13, 18], 1),
        # ([4, 12, 18], 1),
    ]
    
    # Timing: each chord lasts 3 seconds
    measure_duration = 2
    initial_delay = 0.5

    print("19 TET Chord Progression Piece")
    print("=" * 35)
    print("Chord progression:")
    for i, chord in enumerate(chord_progression, 1):
        print(f"  {i}. {chord}")
    print()
    
    tet = TET19System()
    
    try:
        # Convert chord progression into four legato voice lines
        def create_voice_lines(chord_progression, measure_duration, initial_delay):
            """Convert chord progression into four separate legato voice lines"""
            bass_line = []      # Lowest voice
            tenor_line = []     # Second lowest
            alto_line = []      # Second highest  
            soprano_line = []   # Highest voice
            
            current_time = 0.0
            
            for (chord, d) in chord_progression:
                chord_duration = d * measure_duration
                
                # Sort chord notes and assign to voices
                sorted_chord = sorted(chord)
                
                if len(sorted_chord) >= 4:
                    # Four or more notes: assign to all four voices
                    bass_note = sorted_chord[0] - 19      # Lower octave
                    tenor_note = sorted_chord[1] - 19     # Lower octave
                    alto_note = sorted_chord[2] - 19      # Lower octave
                    soprano_note = sorted_chord[3] - 19   # Lower octave
                elif len(sorted_chord) == 3:
                    # Three notes: bass gets bottom, others distributed
                    bass_note = sorted_chord[0] - 19
                    tenor_note = sorted_chord[1] - 19
                    alto_note = sorted_chord[2] - 19
                    soprano_note = sorted_chord[2] - 19   # Double the top note
                elif len(sorted_chord) == 2:
                    # Two notes: bass gets bottom, others get top
                    bass_note = sorted_chord[0] - 19
                    tenor_note = sorted_chord[0] - 19     # Double the bass
                    alto_note = sorted_chord[1] - 19
                    soprano_note = sorted_chord[1] - 19   # Double the top
                else:
                    # One note: all voices play same note in different octaves
                    bass_note = sorted_chord[0] - 19
                    tenor_note = sorted_chord[0] - 19
                    alto_note = sorted_chord[0] - 19
                    soprano_note = sorted_chord[0] - 19
                
                # Add to voice lines
                bass_line.append((bass_note, chord_duration))
                tenor_line.append((tenor_note, chord_duration))
                alto_line.append((alto_note, chord_duration))
                soprano_line.append((soprano_note, chord_duration))
                
                current_time += chord_duration
            
            return bass_line, tenor_line, alto_line, soprano_line
        
        # Create the four voice lines
        bass_line, tenor_line, alto_line, soprano_line = create_voice_lines(chord_progression, measure_duration, initial_delay)
        
        # Create legato sequences for each voice
        bass_sequence = LegatoSequence(
            notes_and_durations=bass_line,
            start_time=initial_delay,
            volume=0.8, #1.2,
            glide_time=0.005  # Quick transitions for bass
        )
        
        tenor_sequence = LegatoSequence(
            notes_and_durations=tenor_line,
            start_time=initial_delay,
            volume=0.8, #1,
            glide_time=0.007  # Medium-quick transitions for tenor
        )
        
        alto_sequence = LegatoSequence(
            notes_and_durations=alto_line,
            start_time=initial_delay,
            volume=0.5,
            glide_time=0.010  # Medium transitions for alto
        )
        
        soprano_sequence = LegatoSequence(
            notes_and_durations=soprano_line,
            start_time=initial_delay,
            volume=0.3,
            glide_time=0.015  # Slowest transitions for soprano (most expressive)
        )
        
        # Melody in quarter notes, as a simple list
        # melody = [0,3,6,11,16,11,5,0,13,19,16,8,13,18,3,0]
        
        # Melody as a list of (note, duration-in-quarter-notes) pairs
        melody = \
        [
        (11, 1), (8, 1), (6, 1), (3, 0.25), (5, 0.25), (3, 0.25), (0, 0.25),
        (5, 2), (11, 1), (16, 1),
        
        (19, 3/4), (19+3, 1/8), (19, 1/8), 
        (16, 3/4), (19, 1/8), (16, 1/8),
        (11, 3/4), (16, 1/8), (11, 1/8), 
        (8, 1),
        
        (11, 4),

        (13, 2), (8, 1/2), (11, 1/2), (13, 1/2), (16, 1/2), 
        
        (19, 1), (3+19, 1), 
        (5+19, 3/4), (8+19, 1/8), (5+19, 1/8),
        (3+19, 1/2), (19, 1/2), 
        
        (16, 1), (19, 1),
        (2+19, 3/4), (5+19, 1/8), (2+19, 1/8),
        (19, 1/4), (21, 1/8), (19, 1/8), (16, 1/2), 

        (11, 2), (19, 2),

        (13, 2), (8, 1/2), (11, 1/2), (13, 1/2), (16, 1/2), 
        
        (19, 1), (2+19, 1), 
        (5+19, 3/4), (6+19, 1/8), (5+19, 1/8),
        (2+19, 1/2), (19, 1/2), 
        
        (16, 1), (19, 1),
        (2+19, 3/4), (5+19, 1/8), (2+19, 1/8),
        (19, 1/4), (20, 1/8), (19, 1/8), (18, 1/2), 

        (19, 4),

        (8, 1), (0, 1), (8, 1/2), (5, 1/2), (3, 1/6), (5, 1/6), (3, 1/6), (0, 1/2),
        (3, 4),
        (5, 1), (-3, 1), (5, 1/2), (2, 1/2), (0, 1/6), (1, 1/6), (0, 1/6), (-1, 1/2),
        (0, 1/4), (2, 1/4), (0, 1/6), (1, 1/6), (2, 1/6), 
        (5, 1/4), (6, 1/8), (5, 1/8), (4, 1/6), (5, 1/6), (8, 1/6),
        (5, 1/6), (2, 1/6), (5, 1/6), (5, 3/2),

        (2, 1), (13-19, 1), (2, 1/2), (0, 1/2), (-1, 1/6), (0, 1/6), (-1, 1/6), (13-19, 1/2),
        (-1, 4),
        (10-19, 1), (13-19, 1), (10-19, 1/2), (13-19, 1/2), (18-19, 1/2), (2, 1/2),
        (0, 4),

        (5, 1/8), (0, 7/8), (5, 1), (8, 1), (13, 1),
        (8, 1/8), (5, 7/8), (8, 1), (13, 1), (19, 1/8), (18, 3/4), (19, 1/8),
        (13, 1/8), (8, 7/8), (13, 1), (18, 1), (5+19, 1),
        (19, 3/2), (18, 1/4), (19, 1/4), (18, 1/12), (19, 1/12), (18, 1/12), (13, 1/4), (8, 1/4), (5, 1/4), (8, 1/4), (5, 1/4), (0, 1/4), (-1, 1/8), (0, 1/8)


        # (13, 3/2), (11, 1/6), (13, 1/6), (11, 1/6), (8, 1), (13, 1),
        # (19, 3/4), (2+19, 1/8), (5+19, 1/8), (6+19, 1/3), (5+19, 1/3), (2+19, 1/3), (19, 1), (13, 1)

        ]

        # Create melody using LegatoSequence for true phase continuity
        quarter_note_duration = measure_duration / 4
        
        # Convert melody to format needed for LegatoSequence
        legato_notes = []
        for note, d in melody:
            duration = d * quarter_note_duration
            legato_notes.append((note, duration))
        
        # Create legato sequence with smooth pitch transitions
        melody_sequence = LegatoSequence(
            notes_and_durations=legato_notes,
            start_time=initial_delay,
            volume=0.45,#0.35,
            glide_time=0.01  # 10ms smooth pitch transitions
        )
        
        print("Pre-computing all legato sequences for optimal performance...")
        tet.precompute_legato_sequence(bass_sequence)
        tet.precompute_legato_sequence(tenor_sequence)
        tet.precompute_legato_sequence(alto_sequence)
        tet.precompute_legato_sequence(soprano_sequence)
        tet.precompute_legato_sequence(melody_sequence)
        
        print("Playing the piece...")
        print("- Five-voice legato polyphony:")
        print("  • Bass line with quick transitions")
        print("  • Tenor voice with medium-quick transitions")
        print("  • Alto voice with medium transitions")
        print("  • Soprano voice with expressive transitions")
        print("  • Melody line with portamento")
        print(f"- Each chord section lasts {measure_duration} seconds")
        print()
        
        # Play all five legato voices together
        tet.play_polyphonic([
        bass_sequence, 
        tenor_sequence, 
        alto_sequence, 
        soprano_sequence, 
        melody_sequence
        ], blocking=True)
        
        print("✨ Piece complete!")
        
    finally:
        tet.close()

def play_chords_only():
    """Play just the chord progression without melody for comparison"""
    chord_progression = [
        [0, 6, 11], [0, 5, 11], [0, 5, 13], [0, 8, 13],
        [0, 5, 13], [5, 13, 18], [4, 12, 18], [1, 6, 12]
    ]
    
    print("Playing chords only for reference...")
    tet = TET19System()
    
    try:
        for i, chord in enumerate(chord_progression, 1):
            print(f"Chord {i}: {chord}")
            tet.play_chord(chord, 2.0, velocity=0.7, blocking=True)
            time.sleep(0.5)
    finally:
        tet.close()

def main():
    """Main function to run the composition"""
    print("19 TET Composition")
    print("=" * 20)
    print()
    
    # Option 1: Play the full piece
    create_chord_progression_piece()
    
    print("\n" + "="*50 + "\n")
    
    # Option 2: Play just chords for reference
    # play_chords_only()

if __name__ == "__main__":
    main()
