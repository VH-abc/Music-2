"""
19 TET (19-tone equal temperament) Music System
Allows playing arbitrary chords and melodies in 19 TET tuning.
Each step is 1200/19 ≈ 63.16 cents.
"""

import numpy as np
import pygame
import threading
import time
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum


class NoteEvent:
    """Represents a musical event with timing"""
    def __init__(self, tet_degree: int, duration: float, start_time: float = 0.0, velocity: float = 1.0, legato: bool = False):
        self.tet_degree = tet_degree  # 0-18 within an octave, can be negative or > 18 for other octaves
        self.duration = duration      # Duration in seconds
        self.start_time = start_time  # Start time in seconds
        self.velocity = velocity      # Volume (0.0 to 1.0)
        self.legato = legato          # If True, use legato envelope


class LegatoSequence:
    """Represents a sequence of notes played with true phase continuity"""
    def __init__(self, notes_and_durations: List[Tuple[int, float]], start_time: float = 0.0, 
                 volume: float = 1.0, glide_time: float = 0.02):
        """
        Create a legato sequence with smooth pitch transitions.
        
        Args:
            notes_and_durations: List of (tet_degree, duration) tuples
            start_time: When to start the sequence
            velocity: Volume (0.0 to 1.0)
            glide_time: Time to smoothly transition between pitches (seconds)
        """
        self.notes_and_durations = notes_and_durations
        self.start_time = start_time
        self.velocity = volume
        self.glide_time = glide_time
        
        # Calculate total duration
        self.duration = sum(duration for _, duration in notes_and_durations)
        
        # Cache for pre-computed waveform
        self._cached_waveform = None
        self._cache_params = None
    
    def get_cache_key(self):
        """Generate a cache key based on sequence parameters"""
        return (
            tuple(self.notes_and_durations),
            self.velocity,
            self.glide_time,
            self.duration
        )


class TET19System:
    """19-tone equal temperament system for generating frequencies and playing music"""
    
    def __init__(self, sample_rate: int = 44100, base_freq: float = 220.0, 
    base_degree: int = 0):
        """
        Initialize the 19 TET system.
        
        Args:
            sample_rate: Audio sample rate
            base_freq: Base frequency (default 440 Hz for A4)
            base_degree: Which 19 TET degree corresponds to base_freq (0-18)
        """
        self.sample_rate = sample_rate
        self.base_freq = base_freq
        self.base_degree = base_degree
        self.cents_per_step = 1200.0 / 19.0  # ~63.16 cents
        
        # Initialize pygame mixer for audio
        pygame.mixer.pre_init(frequency=sample_rate, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        # Store active sounds for polyphony
        self.active_sounds = {}
        self.sound_id_counter = 0
    
    def tet_to_frequency(self, tet_degree: int) -> float:
        """
        Convert a 19 TET degree to frequency in Hz.
        
        Args:
            tet_degree: The degree in 19 TET (can be negative or > 18 for other octaves)
            
        Returns:
            Frequency in Hz
        """
        # Calculate cents from base degree
        cents_offset = (tet_degree - self.base_degree) * self.cents_per_step
        
        # Convert cents to frequency ratio (2^(cents/1200))
        frequency_ratio = 2.0 ** (cents_offset / 1200.0)
        
        return self.base_freq * frequency_ratio
    
    def generate_tone(self, frequency: float, duration: float, velocity: float = 1.0, 
                     attack: float = 0.05, decay: float = 0.15, sustain: float = 0.8, 
                     release: float = 0.3, legato: bool = False) -> np.ndarray:
        """
        Generate a tone with ADSR envelope.
        
        Args:
            frequency: Frequency in Hz
            duration: Duration in seconds
            velocity: Volume (0.0 to 1.0)
            attack, decay, sustain, release: ADSR envelope parameters
            legato: If True, use minimal attack and release for smooth note connections
        
        Returns:
            Numpy array of audio samples
        """
        # 0.05, 0.15, 0.8, 0.3

        # Adjust ADSR for legato playing
        if legato:
            attack = 0.001                      # Nearly instant attack - no audible attack transient
            release = 0.001                     # Nearly instant release - no gaps between notes
            decay = 0.02                       # Very short decay to sustain quickly
            sustain = 0.95                     # Very high sustain level for smooth connection
        
        # Generate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Generate basic waveform with 1/i² harmonic series for softer timbre
        wave = np.sin(2 * np.pi * frequency * t)  # Fundamental
        
        # Add harmonics with 1/i² amplitude decay for very soft, flute-like timbre
        for harmonic in range(2, 17):  # Add harmonics 2-16
            amplitude = 1.0 / (harmonic ** 3)  # 1/i³ decay
            wave += amplitude * np.sin(2 * np.pi * frequency * harmonic * t)
        
        # Normalize to prevent clipping due to harmonic addition
        # The sum of 1/i² series converges, but we normalize for safety
        normalization_factor = 0.2 / 1.645  # Approximate sum of 1/i² for i=1 to 7
        wave *= normalization_factor
        
        # Apply ADSR envelope
        envelope = self._generate_adsr_envelope(len(t), attack, decay, sustain, release, duration)
        wave *= envelope * velocity
        
        # Convert to 16-bit integers for pygame
        wave = np.clip(wave * 32767, -32768, 32767).astype(np.int16)
        
        # Make stereo
        stereo_wave = np.column_stack((wave, wave))
        
        return stereo_wave
    
    def generate_legato_sequence(self, sequence: LegatoSequence) -> np.ndarray:
        """
        Generate a continuous legato sequence with phase continuity and smooth pitch transitions.
        Optimized version using vectorized operations and caching.
        
        Args:
            sequence: LegatoSequence object containing notes and timing
            
        Returns:
            Numpy array of audio samples
        """
        # Check cache first
        cache_key = sequence.get_cache_key()
        if sequence._cached_waveform is not None and sequence._cache_params == cache_key:
            return sequence._cached_waveform
        
        # Create time array for the entire sequence
        total_samples = int(self.sample_rate * sequence.duration)
        
        # Pre-compute frequency envelope efficiently
        frequencies = self._create_frequency_envelope(sequence, total_samples)
        
        # Generate phase array with vectorized cumulative sum
        dt = 1.0 / self.sample_rate
        phase_increments = 2 * np.pi * frequencies * dt
        phases = np.cumsum(phase_increments)
        
        # Generate fundamental wave efficiently
        wave = np.sin(phases)
        
        # Add harmonics vectorized (only compute a few for efficiency)
        for harmonic in range(2, 9):  # Reduced from 17 to 9 harmonics for speed
            amplitude = 1.0 / (harmonic ** 3)
            wave += amplitude * np.sin(phases * harmonic)
        
        # Normalize
        normalization_factor = 0.2 / 1.202  # Adjusted for fewer harmonics
        wave *= normalization_factor
        
        # Apply single ADSR envelope to entire sequence
        envelope = self._generate_adsr_envelope(
            total_samples, 
            attack=0.05,      # Gentle attack at start
            decay=0.1, 
            sustain=0.9, 
            release=0.2,      # Gentle release at end
            total_duration=sequence.duration
        )
        
        wave *= envelope * sequence.velocity
        
        # Convert to 16-bit integers for pygame
        wave = np.clip(wave * 32767, -32768, 32767).astype(np.int16)
        
        # Make stereo
        stereo_wave = np.column_stack((wave, wave))
        
        # Cache the result
        sequence._cached_waveform = stereo_wave
        sequence._cache_params = cache_key
        
        return stereo_wave
    
    def _create_frequency_envelope(self, sequence: LegatoSequence, total_samples: int) -> np.ndarray:
        """
        Efficiently create the frequency envelope for a legato sequence.
        
        Args:
            sequence: LegatoSequence object
            total_samples: Total number of audio samples
            
        Returns:
            Array of frequencies for each sample
        """
        frequencies = np.zeros(total_samples)
        current_time = 0.0
        
        for i, (tet_degree, duration) in enumerate(sequence.notes_and_durations):
            target_freq = self.tet_to_frequency(tet_degree)
            
            # Calculate sample indices for this note
            start_sample = int(current_time * self.sample_rate)
            end_sample = int((current_time + duration) * self.sample_rate)
            end_sample = min(end_sample, total_samples)
            
            if i == 0:
                # First note: start at target frequency
                frequencies[start_sample:end_sample] = target_freq
            else:
                # Subsequent notes: smooth transition from previous frequency
                glide_samples = int(sequence.glide_time * self.sample_rate)
                glide_samples = min(glide_samples, end_sample - start_sample)
                
                if glide_samples > 0:
                    # Smooth transition over glide_time using vectorized linspace
                    prev_freq = frequencies[start_sample - 1] if start_sample > 0 else target_freq
                    frequencies[start_sample:start_sample + glide_samples] = np.linspace(
                        prev_freq, target_freq, glide_samples
                    )
                    
                    # Constant frequency for remainder
                    frequencies[start_sample + glide_samples:end_sample] = target_freq
                else:
                    frequencies[start_sample:end_sample] = target_freq
            
            current_time += duration
        
        return frequencies
    
    def precompute_legato_sequence(self, sequence: LegatoSequence):
        """
        Pre-compute a legato sequence to avoid lag during playback.
        
        Args:
            sequence: LegatoSequence to precompute
        """
        # This will generate and cache the waveform
        self.generate_legato_sequence(sequence)
    
    def _generate_adsr_envelope(self, length: int, attack: float, decay: float, 
                               sustain: float, release: float, total_duration: float) -> np.ndarray:
        """Generate ADSR envelope for a given length with smooth curves."""
        envelope = np.zeros(length)
        
        # Convert time to samples
        attack_samples = int(attack * self.sample_rate)
        decay_samples = int(decay * self.sample_rate)
        release_samples = int(release * self.sample_rate)
        
        # Ensure we don't exceed the total length
        attack_samples = min(attack_samples, length // 3)
        decay_samples = min(decay_samples, length // 4)
        release_samples = min(release_samples, length // 3)
        
        sustain_samples = length - attack_samples - decay_samples - release_samples
        
        idx = 0
        
        # Attack - use a smooth exponential curve for very gentle attack
        if attack_samples > 0:
            attack_curve = np.linspace(0, 1, attack_samples)
            # Apply exponential smoothing for softer attack
            attack_curve = 1 - np.exp(-4 * attack_curve)  # Exponential rise
            envelope[idx:idx + attack_samples] = attack_curve
            idx += attack_samples
        
        # Decay - use smooth curve
        if decay_samples > 0:
            decay_curve = np.linspace(1, sustain, decay_samples)
            # Apply slight exponential decay for smoothness
            decay_curve = sustain + (1 - sustain) * np.exp(-3 * np.linspace(0, 1, decay_samples))
            envelope[idx:idx + decay_samples] = decay_curve
            idx += decay_samples
        
        # Sustain
        if sustain_samples > 0:
            envelope[idx:idx + sustain_samples] = sustain
            idx += sustain_samples
        
        # Release - smooth exponential decay
        if release_samples > 0:
            release_curve = np.linspace(0, 1, release_samples)
            # Exponential decay for smooth release
            envelope[idx:idx + release_samples] = sustain * np.exp(-4 * release_curve)
        
        return envelope
    
    def play_note(self, tet_degree: int, duration: float, velocity: float = 1.0, 
                  blocking: bool = False, legato: bool = False) -> int:
        """
        Play a single note in 19 TET.
        
        Args:
            tet_degree: The degree in 19 TET
            duration: Duration in seconds
            velocity: Volume (0.0 to 1.0)
            blocking: If True, wait for the note to finish
            legato: If True, use legato envelope for smooth connection
            
        Returns:
            Sound ID for tracking
        """
        frequency = self.tet_to_frequency(tet_degree)
        wave = self.generate_tone(frequency, duration, velocity, legato=legato)
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(wave)
        sound_id = self.sound_id_counter
        self.sound_id_counter += 1
        
        # Store and play
        self.active_sounds[sound_id] = sound
        sound.play()
        
        if blocking:
            time.sleep(duration)
            if sound_id in self.active_sounds:
                del self.active_sounds[sound_id]
        else:
            # Clean up after duration
            def cleanup():
                time.sleep(duration + 0.1)  # Small buffer
                if sound_id in self.active_sounds:
                    del self.active_sounds[sound_id]
            threading.Thread(target=cleanup, daemon=True).start()
        
        return sound_id
    
    def play_chord(self, tet_degrees: List[int], duration: float, velocity: float = 1.0, 
                   blocking: bool = False) -> List[int]:
        """
        Play a chord (multiple notes simultaneously).
        
        Args:
            tet_degrees: List of 19 TET degrees
            duration: Duration in seconds
            velocity: Volume (0.0 to 1.0)
            blocking: If True, wait for the chord to finish
            
        Returns:
            List of sound IDs
        """
        sound_ids = []
        for degree in tet_degrees:
            sound_id = self.play_note(degree, duration, velocity, blocking=False)
            sound_ids.append(sound_id)
        
        if blocking:
            time.sleep(duration)
        
        return sound_ids
    
    def play_melody(self, notes: List[NoteEvent], blocking: bool = False) -> List[int]:
        """
        Play a melodic line with specific timing.
        
        Args:
            notes: List of NoteEvent objects
            blocking: If True, wait for the entire melody to finish
            
        Returns:
            List of sound IDs
        """
        sound_ids = []
        
        def play_scheduled_notes():
            start_time = time.time()
            for note in sorted(notes, key=lambda n: n.start_time):
                # Wait until it's time to play this note
                wait_time = note.start_time - (time.time() - start_time)
                if wait_time > 0:
                    time.sleep(wait_time)
                
                sound_id = self.play_note(note.tet_degree, note.duration, note.velocity, blocking=False, legato=note.legato)
                sound_ids.append(sound_id)
        
        if blocking:
            play_scheduled_notes()
        else:
            threading.Thread(target=play_scheduled_notes, daemon=True).start()
        
        return sound_ids
    
    def play_legato_sequence(self, sequence: LegatoSequence, blocking: bool = False) -> int:
        """
        Play a legato sequence with phase continuity.
        
        Args:
            sequence: LegatoSequence object
            blocking: If True, wait for the sequence to finish
            
        Returns:
            Sound ID for tracking
        """
        # Generate the continuous waveform
        wave = self.generate_legato_sequence(sequence)
        
        # Create pygame sound
        sound = pygame.sndarray.make_sound(wave)
        sound_id = self.sound_id_counter
        self.sound_id_counter += 1
        
        # Schedule playback
        def play_at_time():
            time.sleep(sequence.start_time)
            self.active_sounds[sound_id] = sound
            sound.play()
        
        if sequence.start_time > 0:
            threading.Thread(target=play_at_time, daemon=True).start()
        else:
            self.active_sounds[sound_id] = sound
            sound.play()
        
        if blocking:
            time.sleep(sequence.start_time + sequence.duration)
            if sound_id in self.active_sounds:
                del self.active_sounds[sound_id]
        else:
            # Clean up after duration
            def cleanup():
                time.sleep(sequence.start_time + sequence.duration + 0.1)
                if sound_id in self.active_sounds:
                    del self.active_sounds[sound_id]
            threading.Thread(target=cleanup, daemon=True).start()
        
        return sound_id
    
    def play_polyphonic(self, voices: List[Union[List[NoteEvent], LegatoSequence]], blocking: bool = False) -> List[List[int]]:
        """
        Play multiple melodic voices simultaneously.
        
        Args:
            voices: List of voice parts, each containing NoteEvent objects or LegatoSequence
            blocking: If True, wait for all voices to finish
            
        Returns:
            List of sound ID lists (one per voice)
        """
        all_sound_ids = []
        
        # Start all voices
        for voice in voices:
            if isinstance(voice, LegatoSequence):
                # Handle LegatoSequence
                sound_ids = self.play_legato_sequence(voice, blocking=False)
                all_sound_ids.append([sound_ids])  # Wrap in list for consistency
            else:
                # Handle list of NoteEvents
                sound_ids = self.play_melody(voice, blocking=False)
                all_sound_ids.append(sound_ids)
        
        if blocking:
            # Calculate total duration
            total_duration = 0
            for voice in voices:
                if isinstance(voice, LegatoSequence):
                    end_time = voice.start_time + voice.duration
                    total_duration = max(total_duration, end_time)
                else:
                    for note in voice:
                        end_time = note.start_time + note.duration
                        total_duration = max(total_duration, end_time)
            
            time.sleep(total_duration + 0.1)  # Small buffer
        
        return all_sound_ids
    
    def stop_all(self):
        """Stop all currently playing sounds."""
        pygame.mixer.stop()
        self.active_sounds.clear()
    
    def get_scale_degrees(self, scale_pattern: List[int], root_degree: int = 0) -> List[int]:
        """
        Generate scale degrees for common 19 TET scales.
        
        Args:
            scale_pattern: Pattern of steps (in 19 TET degrees)
            root_degree: Root degree in 19 TET
            
        Returns:
            List of 19 TET degrees for the scale
        """
        degrees = [root_degree]
        current = root_degree
        
        for step in scale_pattern:
            current += step
            degrees.append(current)
        
        return degrees[:-1]  # Remove the octave
    
    def close(self):
        """Clean up resources."""
        self.stop_all()
        pygame.mixer.quit()


# Common 19 TET scale patterns (these are examples - 19 TET offers many possibilities)
SCALE_PATTERNS = {
    'chromatic': [1] * 19,  # All 19 degrees
    'major_diatonic': [3, 3, 1, 3, 3, 3, 1],  # Traditional 7-note major scale approximation
    'minor_diatonic': [3, 1, 3, 3, 1, 3, 3],  # Traditional 7-note minor scale approximation
    'pentatonic': [4, 3, 4, 4, 4],  # 5-note scale
    'whole_tone': [3, 3, 3, 3, 3, 3],  # Whole tone scale approximation
}


def demo_19tet():
    """Demonstration of the 19 TET system capabilities."""
    print("19 TET Music System Demo")
    print("=" * 30)
    
    # Initialize the system
    tet = TET19System()
    
    try:
        # Demo 1: Play a scale
        print("1. Playing a 19 TET major scale...")
        scale = tet.get_scale_degrees(SCALE_PATTERNS['major_diatonic'], root_degree=0)
        for i, degree in enumerate(scale):
            print(f"   Degree {degree}: {tet.tet_to_frequency(degree):.2f} Hz")
            tet.play_note(degree, 0.5, blocking=True)
        
        time.sleep(1)
        
        # Demo 2: Play a chord
        print("2. Playing a 19 TET chord...")
        chord_degrees = [0, 6, 11]  # Root, approximate third, approximate fifth
        tet.play_chord(chord_degrees, 2.0, blocking=True)
        
        time.sleep(1)
        
        # Demo 3: Play a melody with rhythm
        print("3. Playing a melody with specific rhythm...")
        melody_notes = [
            NoteEvent(0, 0.5, 0.0),    # Root
            NoteEvent(3, 0.5, 0.5),    # 
            NoteEvent(6, 0.5, 1.0),    # 
            NoteEvent(9, 0.5, 1.5),    # 
            NoteEvent(12, 1.0, 2.0),   # 
            NoteEvent(6, 0.5, 3.0),    # 
            NoteEvent(0, 1.0, 3.5),    # Back to root
        ]
        tet.play_melody(melody_notes, blocking=True)
        
        time.sleep(1)
        
        # Demo 4: Polyphonic - two voices
        print("4. Playing polyphonic music (two voices)...")
        
        # Bass line
        bass_line = [
            NoteEvent(-19, 1.0, 0.0),  # One octave down
            NoteEvent(-13, 1.0, 1.0),
            NoteEvent(-8, 1.0, 2.0),
            NoteEvent(-19, 1.0, 3.0),
        ]
        
        # Melody line
        melody_line = [
            NoteEvent(0, 0.5, 0.0),
            NoteEvent(3, 0.5, 0.5),
            NoteEvent(6, 0.5, 1.0),
            NoteEvent(9, 0.5, 1.5),
            NoteEvent(12, 0.5, 2.0),
            NoteEvent(15, 0.5, 2.5),
            NoteEvent(18, 0.5, 3.0),
            NoteEvent(0, 0.5, 3.5),
        ]
        
        tet.play_polyphonic([bass_line, melody_line], blocking=True)
        
        print("Demo complete!")
        
    finally:
        tet.close()


if __name__ == "__main__":
    demo_19tet()
