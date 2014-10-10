import tty, termios, sys
import config

def init():
	sys.stdout.write("\x1b]2;" + config.TITLE + "\x07")
	clear()
	   
def intro():
	pass
	
def options():
	print "Press 'q' to quit"   

def clear():
	sys.stderr.write("\x1b[2J\x1b[H")
   
def render(snapshot):
	pass
	
def read():
   #Returns a single character from standard input
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   
   return ch

def cycle(snapshot):
	print snapshot
	return True
	   
def cleanup():
	clear()
	    