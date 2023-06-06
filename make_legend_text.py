# coding: utf-8
import pyper
import pyperclip
styles='original special absolute calculated tentative zero temp'.split()
del styles[0]
styles
s = ""
for i = style in enumerate(styles):
    s += f'<path d="M 20 {80+i*10} 20 h 50" class="{style}\n>"
s = ""
for i = style in enumerate(styles):
    s += f'<path d="M 20 {80+i*10} 20 h 50" class="{style}\n>"'
s = ""
for i, style in enumerate(styles):
    s += f'<path d="M 20 {80+i*10} 20 h 50" class="{style}"/>\n'
    s += f'<text x="75" y="{85+i*10}">{style}</text>\n'
    
s
print(s)
pyperclip.copy(s)
s = ""
for i, style in enumerate(styles):
    s += f'<path d="M 20 {80+i*30} 20 h 50" class="{style}"/>\n'
    s += f'<text x="75" y="{85+i*30}">{style}</text>\n'
    
pyperclip.copy(s)
get_ipython().run_line_magic('pwd', '')
get_ipython().run_line_magic('cd', '~/Repos/bezier_calcs/')
