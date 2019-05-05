from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
import click
from fuzzyfinder import fuzzyfinder
from pygments.lexers.python import Python3Lexer
from prompt_toolkit.lexers import PygmentsLexer

from pygments.styles import get_style_by_name
from prompt_toolkit.styles import style_from_pygments_cls, Style, merge_styles

class MyCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, list(globals().keys()))
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))

my_lexer = PygmentsLexer(Python3Lexer)

prompt_style = Style.from_dict({
    'prompt': '#00aa00',
    'arrow': '#aa0000'
})

python_style = style_from_pygments_cls(get_style_by_name('vim'))

final_style = merge_styles([
    prompt_style,
    python_style
])

prompt_text = [('class:prompt', 'bioarineo'), 
               ('class:arrow', '> ')]

class Test():
    def __init__(self):
        self.CONST = 5

t = Test()

while 1:
    user_input = prompt(prompt_text,
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=MyCompleter(),
                        lexer=my_lexer,
                        style=final_style
                        )
    try:
        exec(user_input)
    except Exception as e:
        print(e)