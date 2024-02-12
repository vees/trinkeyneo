Pomodoro Timer for Trinkey Neo
---

### Starting a Pomodoro

- Press Button 1 and a 25 minute pomodoro timer will begin
- The LED on the Trinkey Neo will light up in order from 0 to 3 which is clockwise on the device starting from the one nearest the reset button
- Over the first five minutes the color on the LED will progress from Red to Violet through the rainbow
- After five minutes the first LED will remain violet and the second LED will start from red for the next five minutes
- In the last 5 minutes of the pomodoro (minutes 20-25) all four LEDs will move from red to violet in sync with each other
- At the end of the pomodoro, all four LEDs will slowly pulse blue for a five minute break and then turn off

### Pausing a Pomodoro in progress

- Press Button 2 and all four LED will turn bright yellow
- Time will not pass in the Pomodoro while it is paused
- Press Button 1 to resume the current Pomodoro and the display will go back to the previous state

### Resetting a Pomodoro in the middle

- Press Button 2 while in the Pause state where all four LED are bright yellow
- All four LED will turn bright red
- Press Button 2 a second time to reset the timer completely
- Press Button 1 to resume the current Pomodoro in process

### To install on Trinkey Neo:

- Install CircuitPython 9.0 with the usual instructions
- Once installed, copy these files (excluding the subdirectory) to the root of the folder
