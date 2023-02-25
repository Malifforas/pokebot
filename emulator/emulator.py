import subprocess
import time
import pyautogui
import numpy as np
import cv2
from .utils import load_rom, perform_action

class Emulator:
    def __init__(self, emulator_path, rom_path):
        self.emulator_path = emulator_path
        self.rom_path = rom_path
        self.process = None

    def start(self):
        # Start the emulator process and load the ROM
        self.process = subprocess.Popen([self.emulator_path, self.rom_path])
        time.sleep(5)

    def stop(self):
        # Stop the emulator process
        self.process.terminate()

    def get_screenshot(self):
        # Capture a screenshot of the emulator window and return it
        screenshot = pyautogui.screenshot()
        return np.array(screenshot)

    def click(self, x, y):
        # Simulate a mouse click at the specified coordinates on the emulator window
        pyautogui.click(x=x, y=y)

    def press_key(self, key):
        # Simulate a key press for the specified key on the emulator window
        pyautogui.press(key)

    def type(self, text):
        # Simulate typing the specified text on the emulator window
        pyautogui.typewrite(text)

    def wait_for_screen(self, template_path, threshold=0.9, timeout=10):
        # Load the template image
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        # Loop until the template is found or the timeout is reached
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Capture a screenshot of the emulator window
            screenshot = self.get_screenshot()

            # Preprocess the screenshot and the template image
            preprocessed_screenshot = preprocess(screenshot)
            preprocessed_template = preprocess(template)

            # Search for the template in the screenshot
            result = cv2.matchTemplate(preprocessed_screenshot, preprocessed_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)

            # Check if the template was found
            if max_val >= threshold:
                return True

            # Wait for a short period before trying again
            time.sleep(0.1)

        # If the template was not found, return False
        return False


def preprocess(image):
    # Convert the image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the image
    blurred = cv2.GaussianBlur(grayscale, (5, 5), 0)

    # Apply binary thresholding to the image
    _, thresholded = cv2.threshold(blurred, 160, 255, cv2.THRESH_BINARY)

    return thresholded


def compare_images(image1, image2):
    # Compute the mean squared error (MSE) between the two images
    mse = np.mean((image1 - image2) ** 2)

    # If the MSE is less than 500, the images are considered to be the same
    return mse < 500
class Emulator:
    def __init__(self, emulator_path, rom_path):
        self.emulator_path = emulator_path
        self.rom_path = rom_path
        self.process = None
        self.pipe = None

    def start(self):
        # Start emulator process and establish communication pipe
        self.process, self.pipe = start_emulator(self.emulator_path, self.rom_path)

    def stop(self):
        # Terminate emulator process and close communication pipe
        stop_emulator(self.process, self.pipe)

    def send_command(self, command):
        # Send command to emulator via communication pipe
        send_command(self.pipe, command)

    def get_state(self):
        # Get game state from emulator
        return get_game_state(self.pipe)

    def perform_action(self, action):
        # Perform action in emulator
        perform_action(self.pipe, action)

    def reset(self):
        # Reset emulator to starting state
        reset_emulator(self.pipe)

    def load_rom(self):
        # Load ROM into emulator
        load_rom(self.pipe, self.rom_path)