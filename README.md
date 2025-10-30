# Car controller - Raspberry Pi 4 GPIO Controller

A modular Python 3.11 application to control three GPIO pins (`GPIO 17`, `GPIO 27`, `GPIO 22`) on a Raspberry Pi 4.  
Supports simple motion commands (`forward`, `backward`, `left`, `right`, `lock`, `unlock`, `stop`) and programmable **sequences** with automatic 1 second pause between each.

---

## Requirements

- **Hardware**
  - Raspberry Pi 4
  - 3 GPIO output pins configured (default: GPIO 17, 27, 22)  
  - Raspberry Pi OS

- **Software**
  - **Python 3.11**
  - System package:  
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip python3-rpi.gpio
    ```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AHuyHarryIT/car-controller.git
   cd car-controller
   ```

2. **(Optional) Create a virtual environment**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Project Structure

```
rpi3pins/
├─ app.py               # CLI entrypoint (interactive shell)
├─ sequencer.py         # Executes sequences of GPIO commands
├─ parser.py            # Command tokenizer & duration parser
├─ gpio_driver.py       # Low-level GPIO setup and control
└─ states.py            # Pin definitions, bit patterns, and aliases
```

---

## Usage

Run the interactive REPL:
```bash
sudo python3 app.py
```

**Example commands:**
```
forward           # run forward for default 1 s
backward 2        # run backward for 2 s
lock              # lock sequence (1,0,1)
unlock            # unlock sequence (1,1,0)
stop              # set all pins LOW
sleep 0.5         # pause for 0.5 s
seq forward 2; right 1; lock 0.5; stop
```


---

### Run one-shot sequence from CLI
```bash
sudo python3 app.py "seq forward 2; right 1; lock 0.5; stop"
```

---

## Configuration

All pin assignments and timing defaults are defined in [`states.py`](states.py):

```python
OUT1 = 17
OUT2 = 27
OUT3 = 22
DEFAULT_STEP_DURATION = 1.0
PAUSE_AFTER_SEQ_SECONDS = 1.0
```

Modify these constants to match your wiring or timing needs.

---

## Cleanup

Always ensure GPIO pins are released properly after exit:

```
GPIO cleanup complete.
```

If you encounter issues:
```bash
sudo reboot
```

---

## Notes

- Run with `sudo` to access GPIO.
- Safe for Python 3.11 and RPi.GPIO ≥ 0.7.1.
- You can extend this project with:
  - PWM speed control for L298N
  - Loop/Repeat syntax (e.g. `repeat 3 {forward 1; right 0.5}`)
  - File loader (`load plan.txt`) for offline command scripts

---

## License
MIT License © 2025 AHuyHarryIT
