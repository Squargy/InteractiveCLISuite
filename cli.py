#   TODO: Add documentation
#   TODO: Clean up syntax

from ssl import Options
from click import option
import os
from getch import _Getch
from constants import KEY, ARG_SOURCE, DIRECTION

getch = _Getch()

clear = lambda: os.system('cls')

class Callback:
    def __init__(self, func: 'function', arg_source: ARG_SOURCE = ARG_SOURCE.ARGS, *args: any) -> None:
        self.func = func
        self.arg_source = arg_source
        self.args = args

    def __call__(self):
        match self.arg_source:
            case ARG_SOURCE.VALUE:
                self.func(self.option.value)
            case ARG_SOURCE.TEXT:
                self.func(self.option.text)
            case _:
                self.func(*self.args)


class Option:
    def __init__(self, text: str, callback: Callback, picked: bool = False, value: any = None) -> None:
        self.text = text
        self.picked = picked
        self.value = value
        self.callback = callback
        self.callback.option = self

    def invoke(self):
        self.callback()

    def __str__(self) -> str:
        return f"{self.text}: {self.callback.__name__} -- Picked: {self.picked}"

class OptionsContainerIterator:
    def __init__(self, options) -> None:
        self._options = options
        self._index = 0

    def __next__(self) -> Option:
        if self._index < len(self._options):
            result = self._options[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration

class OptionsContainer:
    def __init__(self, options: 'list[Option]' = []) -> None:
        self.options = options

    def add_option(self, option: Option) -> None:
        self.options.append(option)

    def set_picked(self, index: int) -> None:
        self.options[index].picked = not self.options[index].picked

    def __str__(self) -> str:
        return '\n'.join([str(opt) for opt in self.options])

    def __iter__(self) -> OptionsContainerIterator:
        return OptionsContainerIterator(self.options)

    def __len__(self) -> int:
        return len(self.options)

class RadioOptionsContainer(OptionsContainer):
    def __init__(self, options: 'list[Option]' = []) -> None:
        options[0].picked = True
        super().__init__(options)

    def set_picked(self, index: int) -> None:
        for option in self:
            option.picked = False
        super().set_picked(index)

class Menu:
    def __init__(self, name, options: OptionsContainer, description: str = '') -> None:
        self.name = name
        self.description = description
        self.options = options
        self.cursor = 0
    
    def move(self, direction: DIRECTION):
        self.cursor = (self.cursor + direction) % (len(self.options))

    def move_to(self, index: int):
        if index < len(self.options) - 1:
            self.cursor = index

    def set_picked(self):
        self.options.set_picked(self.cursor)

    def render(self) -> None:
        print(self.name)
        if self.description != "":
            print(self.description)
        for index, option in enumerate(self.options):
            picked = "X" if option.picked else " "
            cursor = "<-------" if self.cursor == index else ""
            print(f"[{picked}] {option.text}{cursor}")

    def run(self) -> None:
        self.render()
        key = None
        while key != KEY.ENTER:
            key = getch()
            match key:
                case KEY.UP:
                    self.move(DIRECTION.UP)
                case KEY.DOWN:
                    self.move(DIRECTION.DOWN)
                case KEY.SPACE:
                    self.set_picked()
                case KEY.CTRLC:
                    exit()
                case _:
                    continue
            clear()
            self.render()

    def invoke_picked(self) -> None:
        for option in self.options:
            if option.picked:
                option.invoke()

    def __str__(self) -> str:
        return str(self.options)

#   TODO: Add the class PaginatedMenu

class PaginatedMenu(Menu):
    #   Använd istället flera OptionsContainer??
    def __init__(self, name, options: OptionsContainer, items_per_page: int, description: str = '') -> None:
        self.name = name
        self.description = description
        self.cursor = 0
        self.items_per_page = items_per_page
        self.all_options = options
        self.options = OptionsContainer(self.options[0:items_per_page])
        self.options.options.append(Option("Next page", callback=Callback(self.next_page)))

    # def __init__(self, name, options: OptionsContainer, items_per_page: int, description: str = '') -> None:
    #     super().__init__(name, options, description)
    #     self.items_per_page = items_per_page
    #     max_per_page_options = max(self.items_per_page, len(options))
    #     self.current_options_indices = range(0, max_per_page_options)
    #     self.prev_and_next = OptionsContainer([
    #         Option("Previous page", callback=Callback(self.prev_page)),
    #         Option("Next page", callback=Callback(self.next_page))
    #     ])

    def render(self) -> None:
        print(self.name)
        if self.description != "":
            print(self.description)
        for i in self.current_options_indices:
            picked = "X" if self.options[i].picked else " "
            cursor = "<-------" if self.cursor == i else ""
            print(f"[{picked}] {self.options[i].text}{cursor}")
        self.render_prev_and_next()

    def render_prev_and_next(self) -> None:
        if 0 < self.current_options_indices[0]:
            print()

    def next_page(self) -> None:
        max_index = max(self.current_options_indices[-1] + self.items_per_page, len(self.options))
        self.current_options_indices = range(self.current_options_indices[-1], max_index)
        self.cursor = self.current_options_indices[-1]

    def prev_page(self) -> None:
        min_index = min(self.current_options_indices[0] - self.items_per_page, 0)
        self.current_options_indices = range(min_index, self.current_options_indices[0])
        self.cursor = min_index


class CLI:
    def __init__(self, menus: 'list[Menu]', active: str) -> None:
        self.menus = dict(menus.name, menus)
        self.active_menu = self.menus[active]

    def render(self) -> None:
        self.active_menu.render()
        # for index, option in enumerate(self.menu.options.options):
        #     picked = "X" if option.picked else " "
        #     cursor = "<-------" if self.menu.cursor == index else ""
        #     # cursor = bcolors.OKGREEN if self.menu.cursor == index else ""
        #     end = bcolors.ENDC if self.menu.cursor == index else ""
        #     print(f"{cursor}[{picked}] {option.text}{end}")

    def run(self) -> None:
        self.active_menu.run()

if __name__ == "__main__":
    print("None")