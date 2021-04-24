# Unofficial Talon Head Up Display

This set of user scripts is meant to help build an awesome visual head up display elements using the Talon Canvas apis. 
It keeps your preferences saved in a CSV file, so that whenever you restart Talon, your HUD will be as you left it.
All the widgets are themeable, which means you can change the colours and images around as you see fit.
Buttons are mapped to actions as well, so you can change those to your wishes using .talon files as well.

# Setup

In order to use the HUD, it is best to set it up next to a version of [knausj_talon](https://github.com/knausj85/knausj_talon/) as it works out of the box. 
However, if you have a different user folder, you can look at the knausj_bindings.py and implement your own content updater.

# Widgets

The status bar

This widget will display the current Talon mode ( Command, dictation or sleep ) and will display the detected or forced language.
The default action of dwelling on the mode icon puts Talon in sleep mode after 1.5 seconds, and the close icon closes the HUD. These actions can be overridden in .talon files.

The event log

This widget works like the command history from knausj, but instead every message has a timed life of about 9 seconds before it disappears, keeping your screen free of clutter.
It isn't just limited to the command history however, you can append any message you want using the user.add_hud_log() action.
For example, adding this to your talon files adds a log to the event log widget

```
testing event log message:
	user.add_hud_log("event", "What I like to drink most is wine that belongs to others")
```

# Commands

All the commands of this repository can be found in commands.talon . A brief rundown of the commands is listed here:

`head up show` opens up the HUD as you left it
`head up hide` hides the complete HUD
`head up theme <themename>` switches the theme of all the widgets to the selected theme. Default themes are `light` and `dark` for light and dark mode respectively

You can also target individual widgets like the status bar and event log for hiding and showing. 
`head up show <widget name>` enables the chosen widget
`head up hide <widget name>` hides the chosen widget

On top of being able to turn widgets on and off, you can configure their attributes to your liking.
Currently, you can change the size, position and font size

`head up drag <widget name>` starts dragging the widget
`head up resize <widget name>` starts resizing the widget
`head up text scale <widget name>` starts resizing the text in the widget
`head up drop` confirms and saves the changes of your changed widgets
`head up cancel` cancels the changes. Hiding a widget also discards of the current changes

Some widgets like the event log also allow you to change the text direction and alignment
`head up align <widget name> left` aligns the text and the widget to the left side of its bounds
`head up align <widget name> right` aligns the text and the widget to the right side of its bounds
`head up expand <widget name> up` changes the direction in which content is placed upwards
`head up expand <widget name> down` changes the direction in which content is placed downwards

# Updating content

As there only exists a single widget right now, the updating content flow is still in its infancy and is subject to change.
This section will be properly expanded when more widgets are added.

# Guidelines

The general idea of this repository is to seperate out three concepts, the users UI preferences, the content on display and the actual display logic.
These three silos are based on assumptions for three personas. The User, the Scripter and the Themer.

The **User** wants to have their content displayed in a way that matches their intentions. 
They decide where they want to place their widgets, what dimensions the widgets should have, what theme should be on display and what size the font should be. After all, the User might be colour blind or have a reduced field of vision. This repository aims to accomodate to them.
The User preferably doesn't have to change code when changing widgets around, and really doesn't want to lose their carefully crafted preferences or change their voice workflow around.

The **Scripter** wants to display their awesome creations in a visually appealing way without actually having to write out all the code required for that. They spent a bunch of time making an output that is useful, like an autocomplete feature or a command log, and they really don't want to spend more time fiddling around with canvas stuff.
The Scripter just sends their content over to the HUD, which knows where the user wants it and in what way.

The **Themer** wants to make an amazing visual experience happen, but do not really want to deal with the nitty gritty details of the widgets themselves. They want to change icons, colours and other visual properties of the UI themselves. And they do not like being limited, preferably having as much freedom of expression as possible.

These three personas are the spirit of this repository. As such, when new content is added to this repository, it should try to adhere to the needs and wishes above.

# Theming

If you want to add your own theme, simply copy and paste an existing theme folder over, give it a new name, define it in the commands.talon file and start changing values in the themes.csv file of your copied over directory.
In general, it is best to keep the images small for memory sake. But otherwise go nuts.

# Roadmap

These are ideas that I want to implement in no specific order and with no specific timeline in mind.

- WIP - An event log that can be filtered by the user, with a time to life setting that makes the message fade away ( much like a status message in an FPS )
- A regular text panel with a header and a close icon with limited growth bounds.
- A fallback text panel that shows every content update that isn't specifically registered by another text panel
- An indicator widget that follows the cursor around to show a single state that is important to the current task at hand
- An image panel with a header and a close icon which displays image content
- WIP - Widget resizing ( width and height rather than a fixed scale ) using the mouse movement position relative to the widgets position
- Widget expand limiting ( relying on the widget resizing above )
- Enabling and disabling animations using a voice command
- User driven icons and buttons on the status bar instead of hard coded ones
- A capture that checks what themes are available on app ready by checking the directories in themes
- Mouse drag and drop, button clicking and other things you would expect in a library like this, instead of polling every so often for changes

If any of these ideas seem cool for you to work on, give me a message on the talon slack so we can coordinate stuff.

# Acknowledgements

The icons used are taken from https://icons.getbootstrap.com/.