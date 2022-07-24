# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import os
import re
import socket
import subprocess
from typing import List  # noqa: F401
from libqtile import layout, bar, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, Rule
from libqtile.command import lazy
from libqtile.widget import Spacer
from unicodes import left_arrow, right_arrow

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')


@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# Most of our keybindings are in sxhkd file - except these

# SUPER + FUNCTION KEYS

    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),


# SUPER + SHIFT KEYS

    Key([mod, "shift"], "c", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),


# QTILE LAYOUT KEYS
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),

# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    # Key([mod, "shift"], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    # Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    # Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    # Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    # Key([mod, "mod1"], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

# TOGGLE FLOATIN LAYOUT
    # Key([mod, "shift"], "space", lazy.window.toggle_floating()),

# CHANGE KEYBOARD LAYOUT
    Key([mod, "shift"], "space", lazy.widget["keyboardlayout"].next_keyboard()),

   ]

def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)

def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)

keys.extend([
    # MOVE WINDOW TO NEXT SCREEN
    # Key([mod, "shift"], "Left", lazy.function(window_to_next_screen, switch_screen=True)),
    # Key([mod, "shift"], "Right", lazy.function(window_to_previous_screen, switch_screen=True)),
    Key([mod, "mod1"], "h", lazy.function(window_to_next_screen, switch_screen=True)),
    Key([mod, "mod1"], "l", lazy.function(window_to_previous_screen, switch_screen=True)),
])

groups = []

# FOR QWERTY KEYBOARDS
group_names = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",]

# FOR AZERTY KEYBOARDS
#group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave",]

group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
# group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall",]
# group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

#CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        # Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])


def init_layout_theme():
    return {"margin": 8,
            "border_width": 2,
            "border_focus": "#83a598",
            "border_normal": "#3c3836"
            }

layout_theme = init_layout_theme()


layouts = [
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Floating(**layout_theme),
    # layout.RatioTile(**layout_theme),
    layout.Max(**layout_theme)
]

# COLORS FOR THE BAR
#Theme name : ArcoLinux Gruvbox
def init_colors():
    return [["#282828", "#282828"], # color 0
            ["#3c3836", "#3c3836"], # color 1
            ["#98971a", "#98971a"], # color 2
            ["#d79921", "#d79921"], # color 3
            ["#cc241d", "#cc241d"], # color 4
            ["#ebdbb2", "#ebdbb2"], # color 5
            ["#83a598", "#83a598"], # color 6
            ["#fbf1c7", "#fbf1c7"], # color 7
            ["#1d2021", "#1d2021"], # color 8
            ["#458588", "#458588"]] # color 9


colors = init_colors()

def init_widgets_defaults():
    return dict(font="Noto Sans",
                fontsize = 12,
                padding = 2,
                background=colors[1])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    # prompt = "{0}@{1} ".format(os.environ["USER"], socket.gethostname())
    prompt = "{0} ".format(os.environ["USER"])
    widgets_list = [
                widget.GroupBox(
                        font = "FontAwesome",
                        fontsize = 16,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 6,
                        padding_x = 5,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[6],
                        inactive = colors[1],
                        rounded = False,
                        highlight_method = "text",
                        this_current_screen_border = colors[9],
                        foreground = colors[2],
                        background = colors[7]
                        ),
                right_arrow(colors[6], colors[7]),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                widget.CurrentLayoutIcon(
                        custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons/wmicons")],
                        background = colors[6],
                        padding = 0,
                        scale = 0.7
                        ),
                widget.TextBox(
                        font = "FontAwesome Bold",
                        fontsize = 16,
                        text = " [",
                        foreground = "#ffffff",
                        background = colors[6],
                        padding = 0,
                        ),
                widget.CurrentLayout(
                        font = "FontAwesome Bold",
                        fontsize = 14,
                        foreground = "#ffffff",
                        background = colors[6]
                        ),
                widget.TextBox(
                        font = "FontAwesome Bold",
                        fontsize = 16,
                        text = "] ",
                        foreground = "#ffffff",
                        background = colors[6],
                        padding = 0,
                        ),
                right_arrow(colors[1], colors[6]),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                widget.WindowName(
                        font = "FontAwesome Italic",
                        fontsize = 14,
                        foreground = colors[5],
                        background = colors[1],
                        ),
                # widget.TextBox(
                #         font = "FontAwesome",
                #         text = "",
                #         foreground = colors[2],
                #         background = colors[1],
                #         padding = 0,
                #         fontsize = 16
                #         ),
                # widget.ThermalSensor(
                #         font = "FontAwesome Bold",
                #         foreground = colors[5],
                #         foreground_alert = colors[6],
                #         background = colors[1],
                #         metric = True,
                #         padding = 3,
                #         threshold = 80
                #         ),
                # battery option 2  from Qtile
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                # widget.Battery(
                #         font = "FontAwesome",
                #         update_interval = 10,
                #         fontsize = 12,
                #         foreground = colors[5],
                #         background = colors[1],
	            #         ),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                left_arrow(colors[1], colors [7]),
                widget.Memory(
                        font = "FontAwesome Bold",
                        format = '{MemUsed: .2f} Gb /{MemTotal: .2f} Gb',
                        measure_mem = 'G',
                        update_interval = 1,
                        fontsize = 12,
                        foreground = colors[1],
                        background = colors[7],
                       ),
                widget.TextBox(
                        font = "FontAwesome",
                        text = "  ",
                        foreground = colors[1],
                        background = colors[7],
                        padding = 0,
                        fontsize = 16
                        ),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                left_arrow(colors[7], colors[6]),
                widget.KeyboardLayout(
                        font = "FontAwesome Bold",
                        foreground = "#ffffff",
                        background = colors[6],
                        padding = 0,
                        fontsize = 12,
                        max_chars = 2,
                        configured_keyboards = ['latam', 'us'],
                        display_map = {'latam': 'LA', 'us': 'US'}
                       ),
                widget.TextBox(
                        font = "FontAwesome",
                        text = "  ",
                        foreground = "#ffffff",
                        background = colors[6],
                        padding = 0,
                        fontsize = 16
                        ),
                # widget.Sep(
                #         font = "FontAwesome Bold",
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                left_arrow(colors[6], colors[7]),
                widget.Clock(
                        font = "FontAwesome Bold",
                        foreground = colors[1],
                        background = colors[7],
                        fontsize = 12,
                        format = "%a %d-%m-%y %H:%M",
                        ),
                widget.TextBox(
                        font = "FontAwesome",
                        text = "  ",
                        foreground = colors[1],
                        background = colors[7],
                        padding = 0,
                        fontsize = 16
                        ),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                left_arrow(colors[7], colors[6]),
                widget.Systray(
                        background = colors[6],
                        icon_size = 20,
                        padding = 4
                        ),
                # widget.Sep(
                #         linewidth = 1,
                #         padding = 10,
                #         foreground = colors[2],
                #         background = colors[1]
                #         ),
                left_arrow(colors[7], colors[6]),
                left_arrow(colors[6], colors[1]),
                widget.TextBox(
                        font = "FontAwesome Bold",
                        text = prompt,
                        foreground = colors[6],
                        background = colors[1],
                        padding = 0,
                        fontsize = 16
                        ),
                widget.TextBox(
                        font = "FontAwesome",
                        text = "  ",
                        foreground = colors[6],
                        background = colors[1],
                        padding = 0,
                        fontsize = 16
                        ),
    ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[19:20]
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    del widgets_screen2[9:15]
    del widgets_screen2[11:13]
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26, opacity=0.9)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=0.9))
            ]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),

],  fullscreen_border_width = 0, border_width = 0)
auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "Qtile"
