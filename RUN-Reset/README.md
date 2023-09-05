# Raspberry Pi RUN pin reset glitch

<figure>
    <img src="./images/RUN-Reset.png" width="800px"/>
    <figcaption>Raspberry Pi resetting when touching RUN</figcaption>
</figure>

**ESD** was a problem (for another chapter maybe), so I started to do the tests using an ESD wrist wrap.<br/>
Basically, the Y capacitor between primary DC+ and cold GND on the secondary side of a 5V (2-prong) power supply, is there to reduce the noise of HF switching, and thus meet EMI standards.<br/>
It also provides a path for common mode 50hz or 60hz line noise, which is ~80Vrms @220v,50hz in this particular SMPSU, unless properly grounded.

&nbsp;

Doing aggressive and repetitive resets was also risky so I designed an emulator, taking into account the open drain output of the XR77004, with the CMOS input of the BCM2837B

<img src="./images/RUN-Reset.svg" style="background-color: white;" width="1200px"/>

## Differential Probe Calibration:

- With open circuit, i.e. no path to ground:
  - Place the multimeter leads between R-Pi_GND and RUN, and use capture mode (peaks) on DC.
  - Take the min and max values: they should be, for example, between 3.170v and 3.434v
- With ground path present, using the MOSFET switch:
  - Do the same and capture min and max.
  - The values should be between 4.2v and 2.2v (2vpp)
- **DC coupling**:
  - Adjust the gain and differential compensation until both cases are achieved.
- **AC coupling**:
  - Set the control input at 5v. There should be no common mode voltage, so adjust the differential/common mode compensation so that you get a flat line.
  - Set the control at 0v. Adjust the gain until you get 2vpp
