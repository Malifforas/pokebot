from subprocess import Popen, PIPE, TimeoutExpired
import time
from threading import Thread, Event
from queue import Queue
import numpy as np


class Emulator:
    def __init__(self, emulator_path, rom_path):
        self.emulator_path = emulator_path
        self.rom_path = rom_path
        self.process = None
        self.input_queue = Queue()
        self.output_queue = Queue()
        self.thread = None
        self.stopped = Event()
        self.lock = None
        self.buffer = b''
        self.prev_buffer = b''

    def start(self):
        self.lock = Event()
        self.lock.set()
        self.process = Popen([self.emulator_path, self.rom_path], stdin=PIPE, stdout=PIPE)
        self.thread = Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.stopped.set()
        self.thread.join()
        self.process.kill()

    def _run(self):
        while not self.stopped.is_set():
            # Wait for input to become available
            self.lock.wait()
            # Send input to emulator
            if not self.input_queue.empty():
                input_data = self.input_queue.get()
                self.process.stdin.write(input_data)
                self.process.stdin.flush()
                self.lock.clear()

            # Read output from emulator
            try:
                output_data = self.process.stdout.read1(1024)
            except ValueError:
                continue
            if not output_data:
                break
            self.buffer += output_data
            if b'\n' in self.buffer:
                lines = self.buffer.split(b'\n')
                self.buffer = lines[-1]
                for line in lines[:-1]:
                    if line.startswith(b'State:'):
                        self.output_queue.put(line[6:])

    def send_input(self, input_data):
        self.input_queue.put(input_data)

    def get_output(self):
        if not self.output_queue.empty():
            output_data = self.output_queue.get()
            return output_data
        return None
