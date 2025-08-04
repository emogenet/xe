#!/home/mgix/venv/bin/python3

# hack the systray to add random apps launcher buttons with PNG icons

# we're going to need to self-forkexec, so we need our own path
# -------------------------------------------------------------
import os
import sys
my_path = sys.executable + ' ' + os.path.realpath(__file__)

# parse cmd line and do things accordingly
# ----------------------------------------
def main():
  if                          1==len(sys.argv): launch()
  elif 'spawn'==sys.argv[1]:  spawn(sys.argv[2], daemon = True)
  elif 'xembed'==sys.argv[1]: xembed(sys.argv[2], sys.argv[3])
  else:                       raise('no comprendo')
  sys.exit(0)

'''
  ./xe.py <no args>                              : from config, launch a bunch of of xe.py embed processes
  ./xe.py spawn /usr/bin/blah                    : launches an app in forking daemon mode w/out ever talking to X11
  ./xe.py xembed /usr/bin/blah /path/to/icon.png : system tray app that waits and launches app 'blah' when clicked
'''

# assumption: I don't believe the gtk api can easily do multiples indicators per gtk app
# TODO: check if assumption is true, in which case this whole affair could be simplified a lot

# launch one instance per button app we want
# ------------------------------------------
def launch():

  import json
  import time
  with open('config.json', 'r') as f:
    config = json.load(f)
    for app in config:
      cmd_path = app['path']
      cmd_icon = app['icon']
      full_cmd = f'{my_path} xembed {cmd_path} {cmd_icon}'
      print(f'{full_cmd=}')
      spawn(cmd = full_cmd, daemon = True)
      time.sleep(0.2) # "animation :-)"

# since python has an officially fucked fork, things are a tad gnarly
# -------------------------------------------------------------------
def spawn(
  cmd,
  daemon
):

  # daemon mode if requested
  # ------------------------
  if daemon:

    # fork
    # ----
    if os.fork():
      return

    # batten down the hatches
    # -----------------------
    for i in range(0, 3):
      try:
        os.close(i)
      except:
        pass

    # become process group leader
    # ---------------------------
    try:
      os.setsid()
    except:
      pass

    # chdir to something generic
    # --------------------------
    try:
      os.chdir('/')
    except:
      pass

  # spawn child process
  # -------------------
  import shlex
  import subprocess
  try:
    args = shlex.split(cmd)
    child = subprocess.Popen(
      args,
      shell = False,
      close_fds = True,
      start_new_session=True,
      stdin = subprocess.DEVNULL,
      stdout = subprocess.DEVNULL,
      stderr = subprocess.DEVNULL,
      #creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    )

    # lest you be plagued by zombies
    # ------------------------------
    if not daemon:
      child.wait()

  except:
    pass

# pretend to be a full-fledged app with an indicator in the systray
# -----------------------------------------------------------------
def xembed(
  cmd_path,
  icon_path
):

  # hide these imports inside func, if not, they fuck fork up real bad
  # ------------------------------------------------------------------
  import gi
  gi.require_version('Gtk', '3.0')
  from gi.repository import Gtk
  from gi.repository import GdkPixbuf

  # straight from the GTK example code
  # ----------------------------------
  class TrayApp:

    def __init__(self, cmd_path, icon_path):
      '''create a GTK status icon for the system tray'''
      self.tray = Gtk.StatusIcon()
      self.tray.set_tooltip_text(cmd_path)
      self.tray.set_from_pixbuf(self.load_icon(icon_path))
      self.tray.connect('activate', self.on_left_click)
      self.cmd_path = cmd_path

    def load_icon(self, icon_path):
      '''Load an image to be displayed in the tray.'''
      try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_path)
        return pixbuf
      except Exception as e:
        print(f'error loading icon: {e}')
        return None

    def on_left_click(self, icon):
      '''Handle left-click events on the tray icon.'''
      spawn(f'{my_path} spawn {self.cmd_path}', daemon = False)

    def run(self):
      '''Start the GTK main loop.'''
      Gtk.main()

  # run the pretend gtk app with a clickable indicator icon
  # -------------------------------------------------------
  app = TrayApp(cmd_path, icon_path)
  app.run()

# python is effing weird
# ----------------------
if __name__=='__main__':
  main()

