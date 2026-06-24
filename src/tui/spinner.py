import time
import itertools
import random
import threading

class Spinner:
    def __init__(self, message="Processing..."):
        self.frames = self.get_sequence()
        self.spinner = itertools.cycle(self.frames)
        self.message = message
        self.done = False # for stopping the loop
        self.thread = threading.Thread(target=self._spin)

    def _spin(self):
        while not self.done:
            print(f"\r{next(self.spinner)} {self.message}", end="", flush=True)
            time.sleep(0.08)
        spaces = " " * (len(self.message) + 2)  # +2 for the spinner and space
        print(f"\r{spaces}\r", end="", flush=True)  # Clear the line when done

    def start(self):
        self.done = False
        self.thread.start()

    def stop(self):
        self.done = True
        self.thread.join()

    def get_sequence(self):
        """
        Returns a random sequence of spinner frames from a predefined set of sequences.
        """
        all_sequences = [
            ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
            ['⠁', '⠂', '⠄', '⡀', '⢀', '⠠', '⠐', '⠈'],
            ['⣾', '⣷', '⣽', '⣯', '⣻', '⣟', '⢿', '⡿'],
            ['⡀', '⣀', '⣄', '⣤', '⣦', '⣶', '⣷', '⣿'],
            ['⡇', '⠏', '⠉', '⠹', '⢸', '⠼', '⠉', '⠧'],
            ['⠉', '⠒', '⠤', '⣀', '⠤', '⠒'],
            ['⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿'],
            ['⡇',' ⡏',' ⡆',' ⠆',' ⠒',' ⠰','','','',' ⢸',' ⢹',' ⢰',' ⠰',' ⠒',' ⠆',' ⡆',' ⡏'],
        ]
        return random.choice(all_sequences)


if __name__ == "__main__":

    spinner = Spinner("Loading...")
    spinner.start()
    
    try:
        unknown_duration = random.uniform(2, 5)  # Simulate a task taking between 2 to 5 seconds
        time.sleep(unknown_duration)
    finally:
        spinner.stop()
        print("Done!")
