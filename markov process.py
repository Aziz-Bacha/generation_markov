import pretty_midi
import random
import note_file

class MarkovMusic:
    def __init__(self):
        self.instrument_map = {}  # Map pretty_midi instrument numbers to your identifiers
        self.next_instrument_id = 0
        self.output = []
        self.option_map = {}  # Similar to HashMap in Java
        self.count_map = {}
        self.files = ["Beethoven_Fur_Elise.mid"]  # MIDI files to process
        self.order = 3  # Order of the Markov chain
        self.resolution = 500        # Rounding properties of notes
        self.velocity_rounding = 40
        self.duration_rounding = 2000
        self.tempo_rounding = 1000000000

        # Array for target channels, empty means all channels
        self.target_channels = []
        
        # Default tempo if not specified in the MIDI file
        self.default_tempo = 500001

    def run(self):
        for file in self.files:
            print(f"Reading file: {file}")
            notes = self.read_input(file)
            self.add_to_map(notes)
            print(f"{len(notes)} notes converted from {file}")
        print(f"\n{len(self.option_map)} mappings made (order {self.order})")
        print("Generating music")
        self.output = self.generate()
        print(f"{len(self.output)} notes generated")
        self.write_to_file()


    def read_input(self, file_name):
        merged_notes = []
        #instrument_set = set()  # To track unique instruments
        try:
            midi_data = pretty_midi.PrettyMIDI(file_name)
            
            for instrument in midi_data.instruments:
                
                for pretty_midi_note in instrument.notes:
                    converted_note = self.convert_to_note(pretty_midi_note, instrument)
                    merged_notes.append(converted_note)  
            merged_notes.sort(key=lambda x: x.timestamp)
            for i in range(len(merged_notes) - 1):
                current_note = merged_notes[i]
                next_note = merged_notes[i + 1]
                current_note.next_note_delay = next_note.timestamp - current_note.timestamp
                merged_notes[i] = current_note

        except Exception as e:
            print(f"Error reading {file_name}: {e}")

        return merged_notes

    def convert_to_note(self, pretty_midi_note, midi_instrument):
        key = pretty_midi_note.pitch
        start_velocity = pretty_midi_note.velocity
        end_velocity = pretty_midi_note.velocity
        note_duration = int((pretty_midi_note.end - pretty_midi_note.start) * self.resolution)  # Assuming resolution is in ms
        timestamp = int(pretty_midi_note.start * self.resolution)  # Adjust resolution as needed

        # Use the MIDI instrument program number directly
        instrument = midi_instrument.program

        # Assuming default value for tempo as pretty_midi.Note doesn't include these
        tempo = self.default_tempo

        return note_file.Note(key, start_velocity, end_velocity, note_duration, 0, tempo, instrument, timestamp)

    def add_to_map(self, notes):
        for i in range(len(notes)):
            # Iterate through each note and consider sequences up to the specified order
            for j in range(i, max(i - self.order, -1), -1):
                # Create a tuple as the key for the dictionary, since lists are not hashable in Python
                sequence = tuple(notes[j:i+1])
                # Get the next note, or None if at the end of the sequence
                next_note = notes[i + 1] if i < len(notes) - 1 else None

                # Initialize dictionaries if sequence is not already in optionMap
                if sequence not in self.option_map:
                    self.option_map[sequence] = []
                    self.count_map[sequence] = []

                # If the next_note is already in the option list, increment its count
                if next_note in self.option_map[sequence]:
                    index = self.option_map[sequence].index(next_note)
                    self.count_map[sequence][index] += 1
                else:
                    # Otherwise, add the next_note to the option list and its count to the count list
                    self.option_map[sequence].append(next_note)
                    self.count_map[sequence].append(1)
    def generate(self):
        # Choose an initial sequence (of notes) from the option_map
        initial_sequence = random.choice(list(self.option_map.keys()))
        current_sequence = list(initial_sequence)  # Convert tuple to list for easier manipulation
        generated_notes = []
    
        while True:
            # Use the last 'order' elements of the current_sequence to form the subsequence
            subsequence = tuple(current_sequence[-self.order:])
    
            if subsequence in self.option_map:
                next_note = self.pick(self.option_map[subsequence], self.count_map[subsequence])
    
                if next_note is None:
                    break
    
                generated_notes.append(next_note)
                current_sequence.append(next_note)
            else:
                print("Subsequence not found in option_map.")
                break
        if self.output:
            first_note_timestamp = self.output[0].timestamp
            for note in self.output:
                note.timestamp -= first_note_timestamp    
        return generated_notes


    def pick(self, options, counts):
        total = sum(counts)
        r = random.randint(1, total)
        for i, count in enumerate(counts):
            r -= count
            if r <= 0:
                return options[i]
        return None

    def write_to_file(self, output_filename="isitgood.mid"):
        midi_output = pretty_midi.PrettyMIDI()
    
        # Create a dictionary to store instruments by their program number
        instruments = {}
        for note in self.output:
            if note.instrument not in instruments:
                new_instrument = pretty_midi.Instrument(program=note.instrument)
                instruments[note.instrument] = new_instrument
                midi_output.instruments.append(new_instrument)
    
            # Convert to pretty_midi Note and add to the correct instrument
            start_time = note.timestamp / self.resolution
            end_time = (note.timestamp + note.note_duration) / self.resolution
            midi_note = pretty_midi.Note(velocity=note.start_velocity, pitch=note.key, start=start_time, end=end_time)
            instruments[note.instrument].notes.append(midi_note)
    
        midi_output.write(output_filename)


# Usage
markov_music = MarkovMusic()
markov_music.run()
