import board
import neopixel
import touchio
import time
import math

# Configuration Variables
POMODORO_DURATION = 25 * 60  # 25 minutes in seconds for the entire focus period
BREAK_DURATION = 5 * 60  # 5 minutes in seconds for the break
FOCUS_SEGMENT_DURATION = POMODORO_DURATION / 5  # Duration of each of the five focus segments

# Color Configuration for ROYGBV Spectrum, Pause, and Break
ROYGBV_COLORS = [
    (255, 0, 0),      # Red
    (255, 165, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 128, 0),      # Green
    (0, 0, 255),      # Blue
    (75, 0, 130)      # Violet
]
PAUSE_COLOR = (255, 255, 0)  # Yellow for pause
BREAK_COLOR = (0, 0, 255)    # Blue for break
RESET_COLOR = (255, 0, 0)    # Red for reset prompt

# Initialize NeoPixels with default brightness of 0.1
num_pixels = 4
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, brightness=0.1, auto_write=False)

# Initialize touch inputs
touch1 = touchio.TouchIn(board.TOUCH1)
touch2 = touchio.TouchIn(board.TOUCH2)

# Timer states
timer_running = False
timer_paused = False
timer_reset = False
timer_start = 0
pause_start = 0
paused_time_total = 0  # Accumulator for total paused time

def get_progress_color(progress, segment):
    """Calculate the color based on the progress through the ROYGBV spectrum for a given segment."""
    # Adjust progress for the final segment to cover the full ROYGBV range
    if segment == 4:
        progress = progress * (len(ROYGBV_COLORS) - 1) / len(ROYGBV_COLORS)

    color_steps = len(ROYGBV_COLORS) - 1
    step_progress = progress * color_steps
    step_index = int(step_progress)
    next_step_index = min(step_index + 1, color_steps)

    blend = step_progress - step_index
    start_color = ROYGBV_COLORS[step_index]
    end_color = ROYGBV_COLORS[next_step_index]

    r = int(start_color[0] + (end_color[0] - start_color[0]) * blend)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * blend)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * blend)

    return (r, g, b)

def pulse_break_color(elapsed_break_time):
    """Generate a pulsing blue effect for the break period."""
    pulse = (math.sin(elapsed_break_time * math.pi / 1) + 1) / 2  # Oscillates between 0 and 1 over 2 seconds
    return tuple(int(c * pulse) for c in BREAK_COLOR)

# Function to pulse pixels for break time
def pulse_break_time(elapsed_break_time):
    # Use a sine wave for pulsing effect
    sine_value = math.sin(elapsed_break_time * math.pi / 5)  # 5-second period for a full pulse
    brightness = (sine_value + 1) / 2  # Normalize sine wave to 0-1 for brightness

    pixels.fill(BREAK_COLOR)
    pixels.brightness = brightness  # Set brightness based on sine wave
    pixels.show()

def update_pause_leds(timer_reset=False):
    """Update LEDs to the pause color"""
    if timer_reset:
        pixels.fill(RESET_COLOR)
    else:
        pixels.fill(PAUSE_COLOR)
    pixels.show()

def update_pixels(elapsed_time, in_break):
    if timer_paused:
        update_pause_leds(timer_reset)  # Ensure LEDs are updated to pause color
        return

    segment = int(elapsed_time // FOCUS_SEGMENT_DURATION)
    segment_progress = (elapsed_time % FOCUS_SEGMENT_DURATION) / FOCUS_SEGMENT_DURATION

    if in_break:
        # Get pulsing color for the break
        color = pulse_break_color(elapsed_time - POMODORO_DURATION)
        pixels.fill(color)
    else:
        for i in range(num_pixels):
            if i < segment < 4:  # Previous segments show their final ROYGBV color
                pixels[i] = get_progress_color(1, i)
            elif segment == 4:  # Fifth focus segment
                color = get_progress_color(segment_progress, segment)
                pixels.fill(color)
            elif i == segment:  # Current segment progresses through ROYGBV
                pixels[i] = get_progress_color(segment_progress, segment)
            else:
                pixels[i] = (0, 0, 0)  # Future segments are off

    pixels.show()

# Main loop
while True:
    if touch1.value:  # Start/restart or resume the timer, or end break early
        while touch1.value:  # Debounce
            time.sleep(0.1)
        if not timer_running or in_break:
            # Reset for a new session
            timer_running = True
            timer_paused = False
            timer_reset = False
            timer_start = time.monotonic()
            paused_time_total = 0
        elif timer_running and timer_paused:
            # Resume from pause
            timer_running = True
            timer_paused = False
            timer_reset = False
            paused_time_total += time.monotonic() - pause_start

    if touch2.value and timer_running:  # Pause the timer
        while touch2.value:  # Debounce
            time.sleep(0.1)
        if not timer_paused:
            # Pause timer
            timer_paused = True
            pause_start = time.monotonic()
            update_pause_leds()
        elif timer_paused and not timer_reset:
            # Go to pre-reset state
            timer_reset = True
            update_pause_leds(timer_reset)
        elif timer_paused and timer_reset:
            # Perform reset with timer_running = False
            # Any Button 1 action will create new
            timer_running = False

    if timer_running and not timer_paused:
        current_time = time.monotonic()
        elapsed_time = current_time - timer_start - paused_time_total
        in_break = elapsed_time > POMODORO_DURATION
        update_pixels(elapsed_time - POMODORO_DURATION if in_break else elapsed_time, in_break)
        if in_break and elapsed_time - POMODORO_DURATION > BREAK_DURATION:
            timer_running = False  # End timer after the break

    if not timer_running:
        pixels.fill((0, 0, 0))  # Turn off LEDs
        pixels.show()

    time.sleep(0.1)  # Small delay to reduce CPU usage
