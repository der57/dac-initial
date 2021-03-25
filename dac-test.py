#!/usr/bin/env -S python3 -u

import sys
import os
import curses
import time
import json
import pigpio

CS = 19
SCK = 26
DIN = 13

class Dac:
    def __init__(self, pi):
        self.pi = pi
        self.clean()

    ## Public entrypoint
    def send(self, addr, value):
        if addr > 7 or addr < 0:
            raise ValueError(f"addr ({addr}) must be 0..7")

        if value > 1023 or value < 0:
            raise ValueError(f"value ({value}) must be 0..1023")

        value = (addr<<12) | (value << 2) | 0b00

        self.select(True)
        print("Select, writing:", end="")

        b = 15
        while b >= 0:
            v = (value >> b) & 1

            print(f"{v}", end="")

            self.pi.write(DIN, v)
            time.sleep(0.001)
            self.pi.write(SCK, 1)
            time.sleep(0.001)
            self.pi.write(SCK, 0)
            b -= 1

        self.select(False)
        print(", deselect")

    # Internal function
    def select(self, v):
        self.pi.write(CS, 0 if v else 1)

    def clean(self):
        self.select(False)
        self.pi.write(SCK, 0)
        self.pi.write(DIN, 0)

def runit(d):

    x = 0
    while True:
        d.send(1, x)
        time.sleep(0.1)
        x = (x + 1) % 1024

def main():
    pi = pigpio.pi()

    pi = pigpio.pi()
    pi.set_mode(CS, pigpio.OUTPUT)
    pi.set_mode(SCK, pigpio.OUTPUT)
    pi.set_mode(DIN, pigpio.OUTPUT)

    pi.set_pull_up_down(CS, pigpio.PUD_OFF)
    pi.set_pull_up_down(SCK, pigpio.PUD_OFF)
    pi.set_pull_up_down(DIN, pigpio.PUD_OFF)

    d = Dac(pi)

    if True:
        d.send(1, 512)
        time.sleep(5)
    else:
        try:
            runit(d)
        except KeyboardInterrupt:
            print("Keyboard interrupt")

    d.clean()
    exit(0)

if __name__ == "__main__":
    main()
