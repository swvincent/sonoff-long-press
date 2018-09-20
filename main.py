from machine import Pin, PWM
import utime

# Constants
BUTTON_PIN = 0
RELAY_PIN = 12
LED_PIN = 13
DEBOUNCE_TIME = 20
LONG_PRESS_TIME = 600

# Global
button_last_pressed_time= 0

# GPIO Setup
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led = Pin(LED_PIN, Pin.OUT)
relay = Pin(RELAY_PIN, Pin.OUT)

# Everything off at start. led is NC.
led.on()
relay.off()


def change_relay_state():
    # Toggle value of relay and led. Note that led is NC so it's opposite.
    relay.value(led.value())
    led.value(not led.value())


def button_pressed(p):
    global button_last_pressed_time

    time_pressed = utime.ticks_ms()

    if button.value() and button_last_pressed_time > 0:
        # Button released, determine length since press
        hold_length = utime.ticks_diff(time_pressed, button_last_pressed_time)

        if hold_length > LONG_PRESS_TIME:
            # Long press
            print(utime.ticks_ms(),
                  "Long press doesn't do anything yet! ({}ms)"
                  .format(hold_length))
        elif hold_length > DEBOUNCE_TIME:
            # Short press
            change_relay_state()
        else:
            # This is just for TS purposes
            print(time_pressed,
                  'Short press ignored: {}ms'.format(hold_length))

        # Reset last pressed time
        button_last_pressed_time = 0
    elif not button.value() and button_last_pressed_time == 0:
        # First button press since last release; record time
        button_last_pressed_time = time_pressed


# SonOff Basic button seems to be NC, so Falling is on press not release
button.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=button_pressed)
