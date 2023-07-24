
from typing import List
import re
##pynput package importieren https://pypi.org/project/pynput/
from pynput.keyboard import Key, Listener

DIGITS = [
    ["_", "|", " ", "|", "|", "_", "|"],  # 0
    [" ", " ", " ", "|", " ", " ", "|"],  # 1
    ["_", " ", "_", "|", "|", "_", " "],  # 2
    ["_", " ", "_", "|", " ", "_", "|"],  # 3
    [" ", "|", "_", "|", " ", " ", "|"],  # 4
    ["_", "|", "_", " ", " ", "_", "|"],  # 5
    ["_", "|", "_", " ", "|", "_", "|"],  # 6
    ["_", " ", " ", "|", " ", " ", "|"],  # 7
    ["_", "|", "_", "|", "|", "_", "|"],  # 8
    ["_", "|", "_", "|", " ", "_", "|"]   # 9
]


class DigitNumber:
    def __init__(self, number: List[str]):
        self.number = number

    def get_number(self):
        return self.number

    def mirror_x(self):
        # Gibt eine neue DigitNumber zurück, die horizontal gespiegelt ist.
        return DigitNumber([self.number[5], self.number[4], self.number[2], self.number[6], self.number[1], self.number[0],
                            self.number[3]])

    def mirror_y(self):
        # Gibt eine neue DigitNumber zurück, die vertikal gespiegelt ist.
        return DigitNumber([self.number[0], self.number[3], self.number[2], self.number[1], self.number[6], self.number[5],
                            self.number[4]])


class BigNumber:
    def __init__(self, numbers: List[DigitNumber]):
        self.numbers = numbers

    def mirror_x(self):
        # Gibt eine neue BigNumber zurück, deren Zahlen horizontal gespiegelt sind.
        return BigNumber([n.mirror_x() for n in self.numbers])

    def mirror_y(self):
        # Gibt eine neue BigNumber zurück, deren Zahlen vertikal gespiegelt sind.
        return BigNumber([n.mirror_y() for n in self.numbers][::-1])


class Anzeige:
    def __init__(self):
        self.is_mirrored_x = False
        self.is_mirrored_y = False
        self.clock_digits: BigNumber
        self.numbers = [DigitNumber(digit) for digit in DIGITS]

    def set_time(self, time: str):
        """
        Setzt die Uhrzeit basierend auf einer gegebenen Zeichenkette.
        Die Zeichenkette sollte eine vierstellige Zahl sein (z. B. "1234").
        """
        offset = 4- len(time)
        self.clock_digits = BigNumber(
            [
            self.numbers[int(time[i-offset])]
            if 0 + offset <= i < 4
            else self.numbers[0]
            for i in range(4)])

    def set_mirrored_x(self):
        # Schaltet die Spiegelung (horizontal) der Anzeige um.
        self.is_mirrored_x = not self.is_mirrored_x

    def set_mirrored_y(self):
        # Schaltet die Spiegelung (vertikal) der Anzeige um.
        self.is_mirrored_y = not self.is_mirrored_y

    def draw_numbers(self, numbers_in_line: List[BigNumber]):
        """
        Zeichnet die Zahlen in der gegebenen Liste auf dem Bildschirm.
        numbers: Eine Liste von DigitNumber-Objekten.
        """
        for i in range(3):
            line = '            '
            for four_digit_number in numbers_in_line:
                line += "".join(" " + number.number[0] + " " if i == 0
                                else "".join(number.number[i * i: i * i + 3])
                                for number in four_digit_number.numbers)
                if numbers_in_line.index(four_digit_number) == 0:
                    line += " | "
            print(line)

    def draw(self):
        # Zeichnet die Uhrzeit auf dem Bildschirm unter Berücksichtigung von Spiegelungen.
        print("\n" *4)

        word1 = [self.clock_digits]
        word2 = []
        if self.is_mirrored_x:
            word2.append(self.clock_digits.mirror_x())
        if self.is_mirrored_y:
            word1.append(self.clock_digits.mirror_y())
        if self.is_mirrored_x and self.is_mirrored_y:
            word2.append(self.clock_digits.mirror_x().mirror_y())
        yachse = (' ' * 22) + "YAchse"
        print(yachse)
        self.draw_numbers(word1)
        xachse = "XAchse" + ("-" * 21 * len(word1))
        print(xachse)
        if word2:
            self.draw_numbers(word2)


def read_number():
    """
    Liest eine Zahl vom Benutzer ein und gibt sie als Zeichenkette zurück.
    """
    while True:
        pattern = r'^\d{1,4}$'
        user_input = input("Geben Sie eine Zahl ein: ")
        if re.match(pattern, user_input):
            return user_input
        else:
            print("Gebe eine Zahl zwischen 1 - 4 stellen lang ein")


if __name__ == "__main__":
    anzeige = Anzeige()
    anzeige.set_time(read_number())
    anzeige.draw()
    pressedY = False;

    # Schleife zum Erkennen von Tastatureingaben
    def on_press(key):
        try:
            # Überprüfen, ob die gedrückte Taste 'x' oder 'y' ist
            if key.char.lower() == 'x':
                anzeige.set_mirrored_x()
                anzeige.draw()
            if key.char.lower() == 'y':
                anzeige.set_mirrored_y()
                anzeige.draw()

        except AttributeError:
            # Die gedrückte Taste ist kein druckbares Zeichen
            pass

    def on_release(key):
        if key == Key.esc:
            return False

    # Initialisiert den Listener der Tastatureingaben
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
