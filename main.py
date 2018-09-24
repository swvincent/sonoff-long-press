"""
SonOff Long Press detection

https://github.com/swvincent/sonoff-long-press

Detects short and long presses of the button on a SonOff Basic WiFi
smart switch. Also provides debouncing of the button. On a short
press the relay and LED are toggled. On a long press, a message is
printed which can be viewed in the REPL.

This code can be built upon to create a program for the SonOff Basic.
It should also adapt well to other ESP8266-based devices and boards.

All testing was done with a SonOff Basic marked SonOff TH_V1.1

Copyright 2018 Scott W. Vincent, shared under an MIT License.
"""

from machine import Pin
import utime

# I found 20ms works well without being too long. That filters
# out all of the bounces w/o losing the actual button presses.
# For the long press, I went by what feels to me like a "long"
# press but it's arbitrary.
DEBOUNCE_TIME = 20
LONG_PRESS_TIME = 600

time_last_button_press= 0

# GPIO Setup
button = Pin(0, Pin.IN, Pin.PULL_UP)
led = Pin(13, Pin.OUT)
relay = Pin(12, Pin.OUT)

# Everything off at start. led is "normally closed"
led.on()
relay.off()


def change_relay_state():
    """
    Toggle value of relay and LED. Note
    that led is NC so it's opposite.
    """
    relay.value(led.value())
    led.value(not led.value())


def button_pressed(p):
    global time_last_button_press

    time_pressed = utime.ticks_ms()

    if button.value() and time_last_button_press > 0:
        # Button released, determine length since press
        hold_length = utime.ticks_diff(time_pressed, time_last_button_press)

        if hold_length > LONG_PRESS_TIME:
            # Long press
            print(utime.ticks_ms(),
                  "Long press doesn't do anything yet! ({}ms)"
                  .format(hold_length))
        elif hold_length > DEBOUNCE_TIME:
            # Short press
            change_relay_state()

        # Reset last pressed time
        time_last_button_press = 0
    elif not button.value() and time_last_button_press == 0:
        # First button press since last release; record time
        time_last_button_press = time_pressed


# SonOff Basic button seems to be NC, so Falling is on press not release
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_pressed)
