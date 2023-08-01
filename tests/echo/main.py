"""
Echoes random messages for a testing purposes of listening.
"""
import random
import time


MESSAGES: list[str] = [
    "hello",
    "goodbye",
    "interesting day sir",
    "java.lang.OutOfMemory",
    "don't know what are you talking about"
]


def main():
    while True:
        print(random.choice(MESSAGES))
        time.sleep(5)


if __name__ == "__main__":
    main()
