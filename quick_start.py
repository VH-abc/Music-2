"""
Quick Start Guide for 19 TET Music System
Run this file to hear basic examples of 19 TET music
"""

from tet19_music import TET19System, NoteEvent
import time

def quick_demo():
    """A quick demonstration to get you started with 19 TET"""
    print("19 TET Music System - Quick Start Demo")
    print("=" * 40)
    
    # Initialize the system
    tet = TET19System()
    
    try:
        # 1. Play individual notes
        print("1. Playing some 19 TET notes...")
        notes_to_play = [0, 3, 6, 9, 12, 15, 18]  # Ascending pattern
        for note in notes_to_play:
            freq = tet.tet_to_frequency(note)
            print(f"   Degree {note}: {freq:.1f} Hz")
            tet.play_note(note, 0.6, blocking=True)
        
        time.sleep(0.5)
        
        # 2. Play a chord
        print("\n2. Playing a 19 TET chord...")
        chord = [0, 6, 11]  # Root, major third, perfect fifth
        print(f"   Chord degrees: {chord}")
        tet.play_chord(chord, 2.0, blocking=True)
        
        time.sleep(0.5)
        
        # 3. Play a simple melody
        print("\n3. Playing a simple melody...")
        melody = [
            NoteEvent(0, 0.5, 0.0),    # Root
            NoteEvent(3, 0.5, 0.5),    # 
            NoteEvent(6, 0.5, 1.0),    # Third
            NoteEvent(11, 0.5, 1.5),   # Fifth
            NoteEvent(19, 1.0, 2.0),   # Octave
            NoteEvent(11, 0.5, 3.0),   # Fifth
            NoteEvent(0, 1.0, 3.5),    # Back to root
        ]
        tet.play_melody(melody, blocking=True)
        
        time.sleep(0.5)
        
        # 4. Two-voice polyphony
        print("\n4. Playing two voices together...")
        
        # Simple bass line
        bass = [
            NoteEvent(-19, 1.0, 0.0),  # Low root
            NoteEvent(-8, 1.0, 1.0),   # Low fifth
            NoteEvent(-12, 1.0, 2.0),  # Low third
            NoteEvent(-19, 1.0, 3.0),  # Back to low root
        ]
        
        # Simple melody over the bass
        melody = [
            NoteEvent(12, 0.5, 0.0),   # High fifth
            NoteEvent(15, 0.5, 0.5),   
            NoteEvent(18, 0.5, 1.0),   
            NoteEvent(19, 0.5, 1.5),   # Octave
            NoteEvent(15, 0.5, 2.0),   
            NoteEvent(12, 0.5, 2.5),   
            NoteEvent(6, 0.5, 3.0),    # Third
            NoteEvent(0, 0.5, 3.5),    # Root
        ]
        
        tet.play_polyphonic([bass, melody], blocking=True)
        
        print("\n✨ Demo complete! You can now:")
        print("   - Edit this file to try your own melodies")
        print("   - Run 'python examples.py' for advanced examples")
        print("   - Check the README.md for full documentation")
        
    finally:
        tet.close()

def create_your_own():
    """Template for creating your own 19 TET music"""
    print("\nCreating your own 19 TET music:")
    print("-" * 35)
    
    tet = TET19System()
    
    try:
        # TODO: Replace this with your own musical ideas!
        
        # Example: Create a chord progression
        chords = [
            [0, 6, 11],      # I chord
            [5, 11, 16],     # IV chord (approximately)
            [11, 17, 22],    # V chord (approximately)
            [0, 6, 11, 19],  # I chord with octave
        ]
        
        print("Playing your chord progression...")
        for i, chord in enumerate(chords):
            print(f"  Chord {i+1}: degrees {chord}")
            tet.play_chord(chord, 1.5, blocking=True)
            time.sleep(0.2)
        
        # Example: Create your own melody
        your_melody = [
            # Edit these to create your own melody!
            NoteEvent(0, 0.4, 0.0),    # Start note
            NoteEvent(2, 0.4, 0.4),    # Small step up
            NoteEvent(6, 0.8, 0.8),    # Bigger jump
            NoteEvent(3, 0.4, 1.6),    # Step down
            NoteEvent(0, 1.2, 2.0),    # Back to start
        ]
        
        print("Playing your melody...")
        tet.play_melody(your_melody, blocking=True)
        
    finally:
        tet.close()

if __name__ == "__main__":
    # Run the quick demo
    quick_demo()
    
    # Uncomment the next line to try creating your own music
    # create_your_own()
