''' pour représenter une note ''' 
class Note:
    def __init__(self, key, start_velocity, end_velocity, note_duration, next_note_delay, tempo, instrument, timestamp):
        self.key = key
        self.start_velocity = start_velocity
        self.end_velocity = end_velocity
        self.note_duration = note_duration
        self.next_note_delay = next_note_delay
        self.tempo = tempo
        self.instrument = instrument
        self.timestamp = timestamp

    def __str__(self):
        return (f"Note(key={self.key}, start_velocity={self.start_velocity}, "
                f"end_velocity={self.end_velocity}, note_duration={self.note_duration}, "
                f"next_note_delay={self.next_note_delay}, tempo={self.tempo}, "
                f"instrument={self.instrument}, timestamp={self.timestamp})")

    def __eq__(self, other):
        if isinstance(other, Note):
            return (self.key == other.key and
                    self.start_velocity == other.start_velocity and
                    self.end_velocity == other.end_velocity and
                    self.note_duration == other.note_duration and
                    self.next_note_delay == other.next_note_delay and
                    self.tempo == other.tempo and
                    self.instrument == other.instrument)
        return False

    def __hash__(self):
        return hash((self.key, self.start_velocity, self.end_velocity,
                     self.note_duration, self.next_note_delay, self.tempo,
                     self.instrument))

    def rounded(self, velocity_rounding, duration_rounding, tempo_rounding):
        return Note(self.key,
                    self.start_velocity - (self.start_velocity % velocity_rounding),
                    self.end_velocity - (self.end_velocity % velocity_rounding),
                    self.note_duration - (self.note_duration % duration_rounding),
                    self.next_note_delay - (self.next_note_delay % duration_rounding),
                    self.tempo - (self.tempo % tempo_rounding),
                    self.instrument,
                    self.timestamp)

