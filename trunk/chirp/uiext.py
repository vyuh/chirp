"""
Copyright (c) 2007-2009 Egor Pomortsev <illicium@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import gtk, gtk.gdk
import cairo
import gobject

class CellRendererRoundedPixbuf(gtk.GenericCellRenderer):
    __gproperties__ = {
        'pixbuf': (gtk.gdk.Pixbuf, 'The pixbuf to render', 'The pixbuf to render', gobject.PARAM_READWRITE),
        'radius': (gobject.TYPE_FLOAT, 'Rounded corner radius ratio', 'Rounded corner radius ratio', 0, 1, 0.3, gobject.PARAM_READWRITE),
    }

    def __init__(self):
        self.__gobject_init__()
        self.pixbuf = None
        self.radius = 0.3
    
    def on_get_size(self, widget, cell_area):
        if not self.pixbuf:
                return (0, 0, 0, 0)

        pixbuf_width = self.pixbuf.get_width()
        pixbuf_height = self.pixbuf.get_height()

        calc_width = self.get_property('xpad') * 2 + pixbuf_width
        calc_height = self.get_property('ypad') * 2 + pixbuf_height

        if cell_area and pixbuf_width > 0 and pixbuf_height > 0:
            x_offset = self.get_property('xalign') * \
                            (cell_area.width - calc_width - \
                            self.get_property('xpad'))
            y_offset = self.get_property('yalign') * \
                            (cell_area.height - calc_height - \
                            self.get_property('ypad'))
        else:
            x_offset = 0
            y_offset = 0

        return x_offset, y_offset, calc_width, calc_height

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def do_set_property(self, pspec, value):
        if not hasattr(self, pspec.name):
            raise AttributeError, 'unknown property %s' % pspec.name
        setattr(self, pspec.name, value)

    def on_render(self, window, widget, background_area, cell_area, expose_area, flags):
        if not self.pixbuf:
            return

        pix_rect = gtk.gdk.Rectangle()
        pix_rect.x, pix_rect.y, pix_rect.width, pix_rect.height = \
                                self.on_get_size(widget, cell_area)

        pix_rect.x += cell_area.x + self.get_property('xpad')
        pix_rect.y += cell_area.y + self.get_property('ypad')
        pix_rect.width -= self.get_property('xpad') * 2
        pix_rect.height -= self.get_property('ypad') * 2

        draw_rect = cell_area.intersect(pix_rect)
        draw_rect = expose_area.intersect(draw_rect)

        context = window.cairo_create()
        context.set_source_pixbuf(self.pixbuf, pix_rect.x, pix_rect.y)

        rect_width = min((draw_rect.width, self.pixbuf.get_width()))
        rect_height = min((draw_rect.height, self.pixbuf.get_height()))
        r = self.get_property('radius') * min((rect_width, rect_height))

        self.draw_round_rect(context, draw_rect.x, draw_rect.y, \
            draw_rect.width, draw_rect.height, r)

        context.fill()

    def draw_round_rect(self, context, x, y, w, h, r):
        context.move_to(x+r,y)
        context.line_to(x+w-r,y)
        context.curve_to(x+w,y,x+w,y,x+w,y+r)
        context.line_to(x+w,y+h-r)
        context.curve_to(x+w,y+h,x+w,y+h,x+w-r,y+h)
        context.line_to(x+r,y+h)
        context.curve_to(x,y+h,x,y+h,x,y+h-r)
        context.line_to(x,y+r)
        context.curve_to(x,y,x,y,x+r,y)
        context.close_path()

gobject.type_register(CellRendererRoundedPixbuf)

