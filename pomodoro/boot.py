import usb_cdc
import usb_hid
import storage
import board
import touchio
import time
import neopixel

# Initialize NeoPixels with default brightness of 0.1
num_pixels = 4
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.1, auto_write=False)
pixels.fill((65, 87, 23)) # Different color than other boot colors
pixels.show()

enable_drive = False  # Do not show drive by default

touch1 = touchio.TouchIn(board.TOUCH1)
start_time = time.monotonic()
while time.monotonic() - start_time < 3:  # If touched in 3 seconds
    if touch1.value:
        while touch1.value:  # Debounce
            time.sleep(0.1)
        enable_drive = True  # Enable the drive
        pixels.fill((255, 255, 255)) # Flash if drive will come on
        pixels.show()
        break
    time.sleep(0.1)

if not enable_drive:  # Truthy value is ok
    storage.disable_usb_drive()

usb_hid.enable((usb_hid.Device.KEYBOARD,))
usb_cdc.enable(console=True, data=True)

