import unittest
import io
from cli import DIRECTION, Callback, Option
from cli import OptionsContainer, Menu, RadioOptionsContainer
from constants import ARG_SOURCE
from unittest.mock import patch


def func() -> None:
    print("test func")


def func2(name) -> None:
    print("test", name)


def new_callback_without_args(func: 'func') -> Callback:
    return Callback(func)


def new_option_container() -> OptionsContainer:
    opt = Option("test", new_callback_without_args(func))
    opt2 = Option("test2", new_callback_without_args(func))
    opt3 = Option("test3", new_callback_without_args(func))
    return OptionsContainer([opt, opt2, opt3])


def new_radio_option_container() -> RadioOptionsContainer:
    opt = Option("test", new_callback_without_args(func))
    opt2 = Option("test2", new_callback_without_args(func))
    opt3 = Option("test3", new_callback_without_args(func))
    return RadioOptionsContainer([opt, opt2, opt3])


def new_menu() -> Menu:
    return Menu("test", new_option_container())


class Test_TestCLI(unittest.TestCase):
    def test_new_option(self):
        opt = Option("test", func)
        self.assertEqual(str(opt), "test: func -- Picked: False")

    def test_new_OptionContainer(self):
        optContainer = new_option_container()
        self.assertTrue(len(optContainer.options) == 3
                        and optContainer.options[0].picked is False
                        and optContainer.options[1].picked is False
                        and optContainer.options[2].picked is False)

    def test_new_RadioOptionContainer(self):
        optContainer = new_radio_option_container()
        self.assertTrue(len(optContainer.options) == 3
                        and optContainer.options[0].picked is True 
                        and optContainer.options[1].picked is False 
                        and optContainer.options[2].picked is False)

    def test_new_menu(self):
        menu = new_menu()
        self.assertTrue(menu.options.options[0].picked == False and menu.options.options[1].picked == False and menu.options.options[2].picked == False)

    def test_move_cursor_up(self):
        menu = new_menu()
        menu.move(DIRECTION.UP)
        self.assertEqual(menu.cursor, 2)

    def test_move_cursor_down(self):
        menu = new_menu()
        menu.move(DIRECTION.DOWN)
        self.assertEqual(menu.cursor, 1)

    def test_pick_option(self):
        menu = new_menu()
        menu.move(DIRECTION.UP)
        menu.set_picked()
        self.assertTrue(menu.options.options[0].picked == False and menu.options.options[1].picked == False and menu.options.options[2].picked == True)

    def test_pick_radio_option(self):
        menu = new_menu()
        menu.move(DIRECTION.DOWN)
        menu.set_picked()
        self.assertTrue(menu.options.options[0].picked == False and menu.options.options[1].picked == True and menu.options.options[2].picked == False)

    def test_move_to_option1(self):
        menu = new_menu()
        menu.move_to(1)
        menu.set_picked()
        self.assertTrue(menu.options.options[0].picked == False and menu.options.options[1].picked == True and menu.options.options[2].picked == False)

    def test_wont_move_to_option3(self):
        menu = new_menu()
        menu.move_to(3)
        menu.set_picked()
        self.assertFalse(menu.options.options[0].picked == False and menu.options.options[1].picked == True and menu.options.options[2].picked == True)

    def test_menu_render_correct_init(self):
        menu = new_menu()
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            menu.render()
        self.assertEqual(fake_stdout.getvalue().strip(), """test\n[ ] test<-------\n[ ] test2\n[ ] test3""")

    def test_menu_render_correct_moved(self):
        menu = new_menu()
        menu.move(DIRECTION.DOWN)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            menu.render()
        self.assertEqual(fake_stdout.getvalue().strip(), """test\n[ ] test\n[ ] test2<-------\n[ ] test3""")

    def test_menu_render_correct_picked(self):
        menu = new_menu()
        menu.set_picked()
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            menu.render()
        self.assertEqual(fake_stdout.getvalue().strip(), """test\n[X] test<-------\n[ ] test2\n[ ] test3""")

    def test_invoke_option(self):
        opt = Option("", func, True)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            opt.invoke()
        self.assertEqual(fake_stdout.getvalue().strip(), "test func")

    def test_invoke_option_with_args_source_args(self):
        cb = Callback(func2, ARG_SOURCE.ARGS, "squargy")
        opt = Option("", cb)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            opt.invoke()
        self.assertEqual(fake_stdout.getvalue().strip(), "test squargy")

    def test_invoke_option_with_args_source_text(self):
        cb = Callback(func2, ARG_SOURCE.TEXT)
        opt = Option("test", cb)
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            opt.invoke()
        self.assertEqual(fake_stdout.getvalue().strip(), "test test")

    def test_invoke_option_with_args_source_default_value(self):
        cb = Callback(func2, ARG_SOURCE.VALUE)
        opt = Option("", cb, value="hej")
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            opt.invoke()
        self.assertEqual(fake_stdout.getvalue().strip(), "test hej")

    def test_invoke_multiple_options(self):
        menu = new_menu()
        menu.set_picked()
        menu.move(DIRECTION.DOWN)
        menu.set_picked()
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            menu.invoke_picked()
        self.assertEqual(fake_stdout.getvalue().strip(), "test func\ntest func")


if __name__ == "__main__":
    unittest.main()
