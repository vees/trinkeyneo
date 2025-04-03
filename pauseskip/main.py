import time
import board
import touchio
import usb_hid
import neopixel
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# Create a ConsumerControl object to send media key events
cc = ConsumerControl(usb_hid.devices)

# Set up both touch pads
touch_pad1 = touchio.TouchIn(board.TOUCH1)
touch_pad2 = touchio.TouchIn(board.TOUCH2)

# Optional: Adjust thresholds to avoid accidental triggers.
# A typical offset of 200-500 is enough, but you can fine-tune.
touch_pad1.threshold = touch_pad1.raw_value + 300
touch_pad2.threshold = touch_pad2.raw_value + 300

# Track the previous touch state so we only fire on *new* touches
pad1_touched_prev = False
pad2_touched_prev = False

ROYGBV_COLORS = [
    (255, 0, 0),      # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 128, 0),      # Green
    (0, 0, 255),      # Blue
    (75, 0, 130)      # Violet
]

num_pixels = 4
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.02, auto_write=True)
pixels[1] = ROYGBV_COLORS[0]
pixels[2] = ROYGBV_COLORS[4]

while True:
    pad1_touched = touch_pad1.value
    pad2_touched = touch_pad2.value

    # If Pad 1 is just touched, send Play/Pause
    if pad1_touched and not pad1_touched_prev:
        cc.send(ConsumerControlCode.PLAY_PAUSE)

    # If Pad 2 is just touched, send Next Track
    if pad2_touched and not pad2_touched_prev:
        cc.send(ConsumerControlCode.SCAN_NEXT_TRACK)

    # Update previous state
    pad1_touched_prev = pad1_touched
    pad2_touched_prev = pad2_touched

    # Small delay for debouncing
    time.sleep(0.05)
