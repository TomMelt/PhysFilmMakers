import curses
import traceback
import time
from measure import get_readings
from sound import playsound


#def get_readings():
#    temp = time.localtime(time.time()).tm_sec
#    return temp, temp, temp


def draw_screen(stdscr):

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(1)

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while 1:
        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Title String
        title = "PhysFilm Makers"[:width-1]

        # Get current value of current, voltage and power
        I, V, P = get_readings()

        I = round(I,2)
        V = round(V,1)

        if I > 0.3:
            playsound(FREQUENCY=int(600*(1+I)))

        # Declaration of strings
        sub1 = "Current : {0:5.3f} mA".format(I)
        sub2 = "Voltage : {0:5.3f} V ".format(V)
        sub3 = "Power   : {0:5.3f} mW".format(P)
        statusbarstr = "Press '<Esc>' or 'q' to exit"

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(sub1) // 2) - len(sub1) % 2)
        start_y = int((height // 2) - 2)

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(
                height-1,
                len(statusbarstr),
                " " * (width - len(statusbarstr) - 1),
                )
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, (width // 2) - 10, '-' * 20)
        stdscr.addstr(start_y + 2, start_x_subtitle, sub1)
        stdscr.addstr(start_y + 3, start_x_subtitle, sub2)
        stdscr.addstr(start_y + 4, start_x_subtitle, sub3)
        stdscr.addstr(start_y + 5, (width // 2) - 10, '-' * 20)

        # Refresh the screen
        stdscr.move(0, 0)

        key = stdscr.getch()
        if key == 27 or key == ord('q'):
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            break

        stdscr.refresh()


def main():
    try:
        curses.wrapper(draw_screen)
    except:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()


if __name__ == "__main__":
    main()
