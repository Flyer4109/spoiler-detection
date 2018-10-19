from tkinter import *

DARK_GREY = "#404040"


class TweetLabeller(Tk):
    def __init__(self, master=None):
        super().__init__(master)

        self.tweet_text = Text(self)

        self.yes_button = Button(self)

        self.no_button = Button(self)

        self.configure_grids()

        self.configure_widgets()

    def configure_grids(self):
        self.grid()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    @staticmethod
    def configure_button(button, text):
        button["text"] = text
        button["highlightbackground"] = DARK_GREY
        button["activebackground"] = DARK_GREY
        button["activeforeground"] = "white"
        button["background"] = "white"
        button["foreground"] = DARK_GREY

    def configure_widgets(self):
        self.tweet_text.insert(END, "All of these incorrect #GameofThrones quotes making me laugh so hard I peed in my pants😂😂😂")
        self.tweet_text["background"] = DARK_GREY
        self.tweet_text["foreground"] = "white"
        self.tweet_text["height"] = 8
        self.tweet_text["highlightbackground"] = DARK_GREY
        self.tweet_text.grid(row=0, column=0, columnspan=2)

        self.configure_button(self.yes_button, "yes")
        self.configure_button(self.no_button, "no")

        self.yes_button.grid(row=1, column=0)
        self.no_button.grid(row=1, column=1)


app = TweetLabeller()
app["background"] = DARK_GREY
app.minsize(width=500, height=200)
app.title = "Tweet Labeller"
app.mainloop()
