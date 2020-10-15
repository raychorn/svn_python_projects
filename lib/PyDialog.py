from msilib import Dialog

class PyDialog(Dialog):
    def __init__(self, *args, **kw):
        Dialog.__init__(self, *args)
        ruler = self.h - 36
        bmwidth = 152*ruler/328
        if kw.get("bitmap", True):
            self.bitmap("Bitmap", 0, 0, bmwidth, ruler, "PythonWin")
        self.line("BottomLine", 0, ruler, self.w, 0)

    def title(self, title):
        self.text("Title", 135, 20, 220, 60, 196611,
                  r"{\VerdanaBold13}%s" % title)

    def back(self, title, next, name = "Back", active = 1):
        if active:
            flags = 3
        else:
            flags = 1
        return self.pushbutton(name, 180, self.h-27 , 56, 17, flags, title, next)

    def cancel(self, title, next, name = "Cancel", active = 1):
        if active:
            flags = 3
        else:
            flags = 1
        return self.pushbutton(name, 304, self.h-27, 56, 17, flags, title, next)

    def next(self, title, next, name = "Next", active = 1):
        if active:
            flags = 3
        else:
            flags = 1
        return self.pushbutton(name, 236, self.h-27, 56, 17, flags, title, next)

    def xbutton(self, name, title, next, xpos):
        return self.pushbutton(name, int(self.w*xpos - 28), self.h-27, 56, 17, 3, title, next)

