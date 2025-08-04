# ***XE.PY*** #

### **What is it?** ###

xe.py adds clickable buttons with PNG icons to your desktop system tray.

### **What does it look like?** ###

Here's an i3 status bar, and the system tray with xe.py doing its thing (look at the red arrow):

![](bar.png "i3bar with xe.py")


## **Will it work for me?** ##

The usual desktop environments usually include this feature natively.

xe.py was specifically designed to add the feature to i3wm, which does not
by design choice.

xe.py has been briefly tested and seems to work fine on the following
desktop environments:

  - i3wm
  - cinnamon
  - ubuntu unity

Generally speaking, if your system tray speaks the xembed protocol, I expect
xe.py to work out of the box (caveat emptor: it won't work on wayland).

Easiest way to check if it works for you:

  - install it (see below)
  - change xeconfig.json to point at valid icon files and valid
    applications on your machine
  - launch: python3 ./xe.py
  - ignore annoying warning messages about deprecated GTK APIs
  - see if new buttons show up in your tray
  - if they do, click on them, see what happens

## **Why?** ##

  When I write code, by a very wide margin, my prefered environments are
  tiling window managers.

  Specifically, I use: [i3wm](https://i3wm.org/)

  However, the original author of i3wm as well as its subsequent maintainers
  subscribe to a strict minimalist philosophy whereby everything is supposed
  to be done via the keyboard and displaying little pictures in the status bar
  generally seems to be considered in that community to be bad taste 😃

  I am in fact in general agreement with that philosophy, with some exceptions:

  - I code on a laptop with a touchpad, which means a button click is *far
    less costly* (in terms of speed and muscle use) than it is with a mouse.

  - for apps used super often (e.g. terminals via $mod+enter) keyboard
    shortcuts is indeed **The Way**.

  - for somewhat rarely used apps, launching them via
    [dmenu](https://tools.suckless.org/dmenu/) or
    [xlunch](https://xlunch.org/), or any of the plethora of similar
    utilities, using $mod+d is a perfectly fine choice.

  - there is however a very short list of apps that fall exactly in the
    cracks separating these two cases:

     - apps launched often enough that using $mod+d launching is a giant
       PITN (too slow)

     - but apps launched not often enough that the cognitive load of
       committing a keyoard shortcut to memory for each is simply not
       worth the exertion, especially at my age.

  - It looks like I am not the only one feeling this way, and there are a
    number of existing solutions to the problem that make some areas of the
    i3 status bar clickable and can launch stuff.

    *However*: they all share one major shortcoming (my biased opinion):
    because the i3 status bar can only (again, by deliberate design choice
    of the i3 authors) display text, and all these solutions are very far
    from aesthetically pleasing. They are also much harder to spot quickly
    than icons.

    Yes, there are workarounds e.g. using hacked fonts that display little
    drawings instead of letters. Again, my own opinion here, but ... these
    are still not very nice, and in particular hard to spot quickly because
    they're B&W.

    Actual pictures are:
      - *way* faster to spotvisually
      - *way* more visually pleasing

  So as a result, I've been wanting to scratch this specific itch probably
  for the better part of 10 years.

  xe.py is the outcome, and, sure, not a perfect one (it's hackish, probably
  violates a large number of UI design guidelines, can only insert buttons in
  the tray and nowhere else, etc...), but ... itch scratched, I can finaly
  launch apps from nicely rendered clickable buttons in the i3 status bar.

## **The good** ##

  - does the job
  - moderate amount of dependencies
  - lightweight: 1 small python script, 1 config file

## **The less good** ##

  - won't work on wayland
  - relies on things slightly annoying to install
  - purposefully violates the intended purpose of the system tray
  - relies on a old-ish protocol (xembed) that might or might not survive the next decade

## **Installation** ##

~~~
  sudo apt install libgirepository1.0-dev gir1.2-gtk-3.0 libglib2.0-dev libgirepository-2.0-dev gir1.2-appindicator3-0.1
  pip install pygtkcompat
  git clone https://gitlab.gnome.org/GNOME/pygobject.git
  cd pygobject
  pip install .
  cd ..
  git clone https://github.com/emogenet/xe.git
  cd xe
  /usr/bin/python3 ./xe.py
~~~

