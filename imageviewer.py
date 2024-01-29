# all of the code in this file is GPL licensed
# follow the link for GPL license <http://www.gnu.org/licenses/licenses.html>

import glob
import os
import sys

import clutter

# window size
x = 800
y = 600

# Supported File Formats
formats = ["*.jpg", "*.png", "*.jpeg", "*.gif", "*.JPG", "*.PNG", "*.GIF"]
files = []


# defining main class which will do all the magic
class playbutt:
    def mouse(self, stage, event):
        print("x:" + str(event.x) + " y:" + str(event.y))
        if (0 <= event.x and event.x <= ((x / 2) - 10)) and (
            0 <= event.y and event.y <= (y / 20)
        ):
            print("You Pressed Button Previous")

            # Changing Pic
            self.current = self.current - 1
            if self.current < 0:
                self.current = self.totalfiles - 1
            self.pic.set_from_file(self.files[self.current])
            self.status.set_text("Current File:   " + str(self.files[self.current]))

            self.rectprev.set_color(clutter.color_from_string("yellow"))
            self.rectnext.set_color(clutter.color_from_string("blue"))
        elif (((x / 2) + 10) <= event.x and event.x <= x) and (
            0 <= event.y and event.y <= (y / 20)
        ):
            print("You Pressed Button Next")

            # Changing Pic
            self.current = self.current + 1
            if self.current == self.totalfiles:
                self.current = 0
            self.pic.set_from_file(self.files[self.current])
            self.status.set_text("Current File:   " + str(self.files[self.current]))

            self.rectnext.set_color(clutter.color_from_string("yellow"))
            self.rectprev.set_color(clutter.color_from_string("blue"))
        else:
            self.rectprev.set_color(clutter.color_from_string("blue"))
            self.rectnext.set_color(clutter.color_from_string("blue"))

    def __init__(self, filename, files, boolfolder):
        # Some Logic for navigating through files
        self.files = files
        self.totalfiles = len(self.files)
        self.filename = filename
        if boolfolder == True:
            self.current = 0
            print("Current file:" + str(self.current))
        else:
            self.current = self.files.index(self.filename)
            print("Current file:" + str(self.current))

        self.stage = clutter.Stage()
        self.stage.set_size(x, y)
        self.stage.set_title("Rajat Image Viewer")
        self.stage.set_color(clutter.color_from_string("red"))
        self.stage.connect("button-press-event", self.mouse)
        self.stage.connect("destroy", clutter.main_quit)

        self.rectprev = clutter.Rectangle()
        self.rectprev.set_size(((x / 2) - 10), (y / 20))
        self.rectprev.set_color(clutter.color_from_string("blue"))
        self.rectprev.set_position(0, 0)

        self.rectnext = clutter.Rectangle()
        self.rectnext.set_size(((x / 2) - 10), (y / 20))
        self.rectnext.set_color(clutter.color_from_string("blue"))
        self.rectnext.set_position(((x / 2) + 10), 0)

        self.rectsep1 = clutter.Rectangle()
        self.rectsep1.set_size(x, 1)
        self.rectsep1.set_color(clutter.color_from_string("grey"))
        self.rectsep1.set_position(0, y / 20 + 2)

        self.rectsep2 = clutter.Rectangle()
        self.rectsep2.set_size(x, 1)
        self.rectsep2.set_color(clutter.color_from_string("grey"))
        self.rectsep2.set_position(0, y - 23)

        # loading initial picture
        self.pic = clutter.Texture()
        try:
            self.pic.set_from_file(self.filename)
        except:
            print("Opening first pic in the folder")
            self.pic.set_from_file(self.files[0])
        self.pic.set_size(x, y - 2 * (y / 20))
        self.pic.set_position(0, y / 20 + 6)

        # Status Bar String
        self.status = clutter.Text()
        self.status.set_position(0, y - 20)
        self.status.set_text("Current File:   " + str(self.files[self.current]))
        self.status.set_color(clutter.color_from_string("pink"))

        self.labelp = clutter.Text()
        self.labelp.set_text("<Previous")
        self.labelp.set_position(((x / 2) - 10) / 4, y / 100)
        self.labelp.set_color(clutter.color_from_string("black"))

        self.labeln = clutter.Text()
        self.labeln.set_text("Next>")
        self.labeln.set_position((x - x / 4) - x / 8, y / 100)
        self.labeln.set_color(clutter.color_from_string("black"))

        # adding everything to stage
        self.stage.add(self.rectprev)
        self.stage.add(self.rectnext)
        self.stage.add(self.rectsep1)
        self.stage.add(self.rectsep2)
        self.stage.add(self.pic)
        self.stage.add(self.labelp)
        self.stage.add(self.labeln)
        self.stage.add(self.status)
        self.stage.show_all()

    def main(self):
        clutter.main()


if __name__ == "__main__":
    boolfolder = False

    # Setting Current Working Directory and extracting the names ofall the pictures available
    # under that directory
    try:
        filename = sys.argv[1]
        if filename[len(filename) - 1] == "/":
            os.chdir(filename)
            boolfolder = True
            for name in formats:
                for nameex in glob.glob(name):
                    files.append(nameex)
        else:
            location = filename.rfind("/")
            filereal = filename[location + 1 :]
            os.chdir(filename[:location])
            filename = filereal
            for name in formats:
                for nameex in glob.glob(name):
                    files.append(nameex)
    except OSError as err:
        print("Location not available,is the drive already mounted?")
    obj = playbutt(filename, files, boolfolder)
    obj.main()
