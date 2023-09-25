from typing import Callable

from pydantic import BaseModel, Field


def do_nothing():
    pass


class Select(BaseModel):
    choices: list[str]
    choice_label: str = "确认"
    choice_callback: Callable
    choice_multi: bool = False

    input_enabled: bool = False
    input_btn_text: str = ""
    input_instruction: str = ""
    input_callback: Callable = do_nothing

    extra_buttons: list[tuple[str, Callable]] = Field(default_factory=list)

    def enable_input(self, label: str, instruction: str, callback: Callable):
        self.input_area = True
        self.input_btn_text = label
        self.input_instruction = instruction
        self.input_callback = callback

    def add_button(self, text: str, func: Callable):
        self.extra_buttons.append((text, func))
