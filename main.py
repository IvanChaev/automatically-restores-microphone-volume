import os
import time
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

INTERVAL = 10
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "logs", "mic_volume.log")
PID_DIR = os.path.join(SCRIPT_DIR, "logs")
PID_FILE = os.path.join(PID_DIR, "pid.pid")


def write_pid():
    try:
        os.makedirs(PID_DIR, exist_ok=True)
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        log("Ошибка записи pid-файла: {}".format(e))


def write_raised_flag(value):
    try:
        os.makedirs(PID_DIR, exist_ok=True)
        with open(os.path.join(PID_DIR, "raised.flag"), "w") as f:
            f.write(value)
    except Exception as e:
        log("Ошибка записи флага громкости: {}".format(e))


def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("{} {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"), msg))
    except Exception:
        pass


def set_mic_volume_to_100():
    mic = AudioUtilities.GetMicrophone()
    if mic is None:
        log("Микрофон не найден")
        return
    interface = mic.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    endpoint = interface.QueryInterface(IAudioEndpointVolume)
    current = endpoint.GetMasterVolumeLevelScalar()
    if abs(current - 1.0) > 0.001:
        endpoint.SetMasterVolumeLevelScalar(1.0, None)
        msg = "Громкость микрофона: {:.0f}% -> 100%".format(current * 100)
        log(msg)
        write_raised_flag("{:.0f} -> 100".format(current * 100))


def main():
    write_pid()
    log("Скрипт запущен (pid {})".format(os.getpid()))
    while True:
        try:
            set_mic_volume_to_100()
        except Exception as e:
            log("Ошибка: {}".format(e))
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
