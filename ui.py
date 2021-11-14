from imports import *


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
