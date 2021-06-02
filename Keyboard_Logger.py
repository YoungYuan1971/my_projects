from pynput.keyboard import Key, Listener
import datetime


def on_press(key):
    date = datetime.datetime.now()
    date_format = f'{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}'
    msg = f'{date_format}--> {key} 被按下\n'

    f.write(msg)


def on_release(key):
    if key == Key.esc:
        return False


if __name__ == '__main__':
    with open('key_log.txt', 'w', encoding='utf-8') as f:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
