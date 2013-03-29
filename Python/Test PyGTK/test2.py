#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import gtk
 
class Entry1(object):
 
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Entry und Frame")
        self.window.set_default_size(300, 100)
        self.window.connect("delete_event", self.event_delete)
        self.window.connect("destroy", self.destroy)
 
        frame = gtk.Frame("Möchten Sie SPAM bekommen?")
        self.window.add(frame)
        # vertikale Box
        vbox = gtk.VBox(True, 10)
        frame.add(vbox)
        # obere hbox
        hbox1 = gtk.HBox(True, 0)
        vbox.pack_start(hbox1)
        label = gtk.Label("Name")
        label.show()
        hbox1.pack_start(label)
        self.entry1 = gtk.Entry()
        self.entry1.show()
        hbox1.pack_start(self.entry1)
        hbox1.show()
        # untere hbox
        hbox2 = gtk.HBox(True, 0)
        vbox.pack_start(hbox2)
        label = gtk.Label("E-Mail")
        label.show()
        hbox2.pack_start(label)
        self.entry2 = gtk.Entry()
        self.entry2.show()
        hbox2.pack_start(self.entry2)
        hbox2.show()
        # Knopf
        button = gtk.Button("Im SPAM-Verteiler eintragen")
        button.connect("clicked", self.button_clicked)
        button.show()
        vbox.pack_start(button)
        # fertig vertikale Box
        vbox.show()
        frame.show()
        self.window.show()
 
    def button_clicked(self, data=None):
        name = self.entry1.get_text()
        email = self.entry2.get_text()
        text = "%s, wir schicken ihnen ab sofort regelmäßig SPAM an die Adresse %s!" % (name, email)
        dlg = gtk.MessageDialog(flags=gtk.DIALOG_MODAL, buttons=gtk.BUTTONS_OK, message_format=text)
        dlg.set_title("Danke für ihre Adresse")
        dlg.run()
        dlg.destroy()
 
    def event_delete(self, widget, event, data=None):
        return False
 
    def destroy(self, data=None):
        gtk.main_quit()
 
    def main(self):
        gtk.main()
 
if __name__ == "__main__":
    e = Entry1()
    e.main()
