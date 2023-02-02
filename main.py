import curses
from curses import wrapper
import time
import random

def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Esse é um Teste de Digitação!")
    stdscr.addstr("\nAperte qualquer tecla para começar")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, ppm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"PPM: {ppm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)

        stdscr.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

def ppm_test(stdscr):
    target = load_text()
    current_text = []
    ppm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        ppm = round((len(current_text) / (time_elapsed / 60 )) / 5)

        stdscr.clear()
        display_text(stdscr, target, current_text, ppm)
        stdscr.refresh()

        if "".join(current_text) == target:
            stdscr.nodelay(False)
            return ppm
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target):
            current_text.append(key)
    

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    start_screen(stdscr)
    cont = 0
    avg = 0
    while True:
        cont += 1
        avg += ppm_test(stdscr)
        med = round(avg / cont)
        stdscr.addstr(2, 0, f"Seu PPM médio é de: {med}")
        stdscr.addstr(3, 0, "Você completou o teste! Aperte qualquer letra para continuar...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break

wrapper(main)

# fim do programa