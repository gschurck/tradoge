import time

import timg
from art import tprint
from colorama import Fore
from progress.bar import Bar


class SlowBar(Bar):
    suffix = Fore.YELLOW + '%(remaining_minutes)d minutes ' + Fore.RESET + ' (%(remaining_seconds)d seconds)'
    fill = Fore.YELLOW + '$' + Fore.RESET

    @property
    def remaining_minutes(self):
        return self.eta // 60

    @property
    def remaining_seconds(self):
        return self.eta // 1


def on_start():
    # Decorations
    print(Fore.YELLOW)
    obj = timg.Renderer()
    obj.load_image_from_file("data/dogecoin.png")
    obj.resize(100, 100)
    obj.render(timg.ASCIIMethod)
    tprint("TraDOGE", "font: varsity")
    print(Fore.RESET)


def print_loading_bar(message, delay_seconds):
    bar = SlowBar(
        message, max=delay_seconds
    )
    for i in reversed(range(delay_seconds)):
        time.sleep(1)
        bar.next()
    bar.finish()