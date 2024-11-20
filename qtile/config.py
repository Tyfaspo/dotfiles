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

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, hook, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = "kitty"
file_manager = "nautilus"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "q", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Return", lazy.spawn("rofi -modi drun -show drun"), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "e", lazy.spawn(file_manager), desc="Launch file manager"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "v", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "m", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # layout.Spiral(ratio=0.5),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(fair=False),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


screens = [

    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=15,
                    background='#282738',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/launch_Icon.png',
                    margin=2,
                    background='#282738',
                    # mouse_callbacks={"Button1": power},
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                ),

                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=24,
                    borderwidth=3,
                    highlight_method='block',
                    active='#CAA9E0',
                    block_highlight_text_color="#91B1F0",
                    highlight_color='#353446',
                    inactive='#282738',
                    foreground='#4B427E',
                    background='#353446',
                    this_current_screen_border='#353446',
                    this_screen_border='#353446',
                    other_current_screen_border='#353446',
                    other_screen_border='#353446',
                    urgent_border='#353446',
                    rounded=True,
                    disable_drag=True,
                ),

                widget.Spacer(
                    length=8,
                    background='#353446',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/1.png',
                ),


                widget.CurrentLayoutIcon(
                    custom_icon_paths=["~/.config/qtile/Assets/layout"],
                    background='#353446',
                    scale=0.50,
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#282738',
                    foreground='#CAA9E0',
                    # mouse_callbacks={"Button1": search},
                ),

                widget.TextBox(
                    fmt='Search',
                    background='#282738',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    foreground='#CAA9E0',
                    # mouse_callbacks={"Button1": search},
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/4.png',
                ),

                widget.WindowName(
                    background='#353446',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    empty_group_string="Desktop",
                    max_chars=130,
                    foreground='#CAA9E0',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/3.png',
                ),

                widget.Systray(
                    background='#282738',
                    fontsize=2,
                ),

                widget.TextBox(
                    text=' ',
                    background='#282738',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/6.png',
                    background='#353446',
                ),

                widget.TextBox(
                    text="",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                ),

                widget.Memory(
                    background='#353446',
                    format='{MemUsed: .0f}{mm}',
                    foreground='#CAA9E0',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    update_interval=5,
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.Spacer(
                    length=8,
                    background='#353446',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                ),

                widget.Battery(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                    format='{percent:2.0%}',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/2.png',
                ),

                widget.Spacer(
                    length=8,
                    background='#353446',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                ),

                widget.Volume(
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                    background='#353446',
                    foreground='#CAA9E0',
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/5.png',
                    background='#353446',
                ),

                widget.TextBox(
                    text=" ",
                    font="Font Awesome 6 Free Solid",
                    fontsize=13,
                    background='#282738',
                    foreground='#CAA9E0',
                ),

                widget.Clock(
                    format='%I:%M %p',
                    background='#282738',
                    foreground='#CAA9E0',
                    font="JetBrainsMono Nerd Font Bold",
                    fontsize=13,
                ),

                widget.Spacer(
                    length=18,
                    background='#282738',
                ),

            ],
            30,
            border_color='#282738',
            border_width=[0,0,0,0],
            margin=[15,60,6,60],

        ),
    ),
]
# screens = [
#     Screen(
# 	    wallpaper='~/.current_wallpaper/current.png',
#         wallpaper_mode='stretch',
# 	    top=bar.Bar(
#             [
#                 widget.CurrentLayout(),
#                 widget.GroupBox(),
#                 widget.Prompt(),
#                 widget.WindowName(),
#                 widget.Chord(
#                     chords_colors={
#                         "launch": ("#ff0000", "#ffffff"),
#                     },
#                     name_transform=lambda name: name.upper(),
#                 ),
#                 widget.TextBox("default config", name="default"),
#                 widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
#                 # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
#                 # widget.StatusNotifier(),
#                 widget.Systray(),
#                 widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
#                 widget.QuickExit(),
#             ],
#             24,
#             # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
#             # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
#         ),
#         # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
#         # By default we handle these events delayed to already improve performance, however your system might still be struggling
#         # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
#         # x11_drag_polling_rate = 60,
#     ),
#     Screen(wallpaper='~/.current_wallpaper/current.png', wallpaper_mode='stretch')
# ]

@hook.subscribe.startup_once
def _():
    run("/home/tyfaspo/.config/qtile/scripts/autostart.sh")


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

