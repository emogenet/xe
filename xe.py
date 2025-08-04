#!/home/mgix/venv/bin/python3

# add user-defined app launcher PNG-icon buttons to the systray

# things we need
# --------------
import os
import sys
own_dir = os.path.dirname(os.path.realpath(__file__))
own_path = sys.executable + ' ' + os.path.realpath(__file__)

# fork a subprocess
# -----------------
def spawn(
  cmd,
  daemon
):

  # do the daemon mode dance if requested
  # -------------------------------------
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
      os.chdir(own_dir)
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

# single-process tray icon manager
# --------------------------------
def launch():

  print(f'in launch')

  # hide these imports inside func, they don't play nice with  fork
  # ---------------------------------------------------------------
  import gi
  gi.require_version('Gtk', '3.0')
  from gi.repository import Gtk
  from gi.repository import GdkPixbuf

  # straight from the GTK example code
  # ----------------------------------
  class Tray_Button:

    def __init__(
      self,
      cmd_path,
      icon_path
    ):
      self.tray = Gtk.StatusIcon()
      self.tray.set_tooltip_text(cmd_path)
      self.tray.set_from_pixbuf(self.load_icon(icon_path))
      self.tray.connect('activate', self.on_left_click)
      self.cmd_path = cmd_path

    def load_icon(
      self,
      icon_path
    ):
      try:
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon_path)
        return pixbuf
      except Exception as e:
        print(f'error loading icon: {icon_path} - {e}')
        return None

    def on_left_click(
      self,
      icon
    ):
      spawn(
        f'{own_path} spawn {self.cmd_path}',
        daemon = False
      )

  # load config
  # -----------
  config = None
  try:
    with open('config.json', 'r') as f:
      import json
      config = json.load(f)
  except Exception as e:
    print(f'could not read file config.json: {e}')
    sys.exit(1)

  # for all buttons in config
  # -------------------------
  tray_buttons = []
  for app in config:
    cmd  = app['path']
    icon = app['icon']
    tray = Tray_Button(
      cmd_path  = cmd,
      icon_path = icon
    )
    tray_buttons.append(tray)

  # run the GTK main loop
  # ---------------------
  Gtk.main()

if __name__=='__main__':
  if   1==len(sys.argv):      spawn(f'{own_path} self', daemon = True)
  elif 'spawn'==sys.argv[1]:  spawn(sys.argv[2], daemon = True)
  elif 'self'==sys.argv[1]:   launch()
  else:                       raise('no comprendo')
  sys.exit(0)

