from tkinter import *
import time


class Dashboard2:
    def __init__(self, window):
        self.window = window
        self.window.title("Atlas Dashboard")
        self.window.geometry("700x600")
        self.window.resizable(0, 0)
        self.window.state('zoomed')
        self.window.config(background='#eff5f6')

        self.header = Frame(self.window, bg='#009df4')
        self.header.place(x=300, y=0, width=2000, height=60)

        self.sidebar = Frame(self.window, bg='#ffffff')
        self.sidebar.place(x=0, y=0, width=300, height=1000)

        self.heading = Label(self.window, text='HANDCRAFT — Atlas Dashboard', font=("", 15, "bold"), fg='#0064d3', bg='#eff5f6')
        self.heading.place(x=325, y=70)

        self.bodyFrame1 = Frame(self.window, bg='#ffffff')
        self.bodyFrame1.place(x=328, y=110, width=1180, height=450)

        self.bodyFrame2 = Frame(self.window, bg='#009aa5')
        self.bodyFrame2.place(x=328, y=600, width=310, height=220)

        self.bodyFrame3 = Frame(self.window, bg='#e21f26')
        self.bodyFrame3.place(x=760, y=600, width=310, height=220)

        self.bodyFrame4 = Frame(self.window, bg='#ffcb1f')
        self.bodyFrame4.place(x=1200, y=600, width=310, height=220)

        self.logo = Label(self.sidebar, bg='#ffffff')
        self.logo.place(x=70, y=80)

        self.brandName = Label(self.sidebar, text='Club de Robótica', bg='#ffffff', font=("", 20, "bold"))
        self.brandName.place(x=35, y=150)

        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='blue', font=("", 20, "bold"), bd=0, fg= 'white',
                            cursor='hand2', activebackground='#32cf8e')
        self.dashboard_text.place(x=85, y=270)

        self.manage_text = Button(self.sidebar, text="Manage", bg='green', font=("", 20, "bold"), bd=0, fg = 'white',
                        cursor='hand2', activebackground='#32cf8e')
        self.manage_text.place(x=85, y=375)

        self.settings_text = Button(self.sidebar, text="Settings", bg='grey', font=("", 20, "bold"), bd=0, fg = 'white',
                        cursor='hand2', activebackground='#32cf8e')
        self.settings_text.place(x=85, y=475)

        self.Exit_text = Button(self.sidebar, text="Stop", bg='red', font=("", 20, "bold"), bd=0, fg= 'white',
                        cursor='hand2', activebackground='#32cf8e', command=self.window.destroy)
        self.Exit_text.place(x=85, y=575)

        self.pieChart = Label(self.bodyFrame1, bg='#ffffff')
        self.pieChart.place(x=690, y=70)

        self.graph = Label(self.bodyFrame1, bg='#ffffff')
        self.graph.place(x=40, y=70)

        self.Moving = Label(self.bodyFrame2, text='', bg='#009aa5', font=("", 25, "bold"), anchor="center", justify="center", width=10)
        self.Moving.place(x=50, y=100)


        self.Moving_label = Label(self.bodyFrame2, text="Moving", bg='#009aa5', font=("", 40, "bold"),
                                       fg='white')
        self.Moving_label.place(x=5, y=5)

        self.people_left = Label(self.bodyFrame3, text= 'YES', bg='#e21f26', font=("", 25, "bold"), anchor="center", justify="center", width=10)
        self.people_left.place(x=50, y=100)

        self.parked = Label(self.bodyFrame3, bg='#e21f26')
        self.parked.place(x=220, y=0)

        self.parked_label = Label(self.bodyFrame3, text="Parked", bg='#e21f26', font=("", 40, "bold"),
                                      fg='white')
        self.parked_label.place(x=5, y=5)

        self.voltage = Label(self.bodyFrame4, text='5V', bg='#ffcb1f', font=("", 25, "bold"),  anchor="center", justify="center", width=10)
        self.voltage.place(x=50, y=100)

        self.voltage_label = Label(self.bodyFrame4, text="Voltage", bg='#ffcb1f', font=("", 40, "bold"),
                                    fg='white')
        self.voltage_label.place(x=5, y=5)
        
        self.earningsIcon = Label(self.bodyFrame4, bg='#ffcb1f')
        self.earningsIcon.place(x=220, y=0)

        self.date_time_image = Label(self.sidebar, bg="white")
        self.date_time_image.place(x=30, y=20)

        self.date_time = Label(self.window)
        self.date_time.place(x=80, y=15)
        self.show_time()

        # Variable para rastrear el estado del movimiento
        self.is_moving = False

        # Bind keyboard events
        self.window.bind("<KeyPress>", self.key_pressed)

    def show_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime('%Y/%m/%d')
        set_text = f"  {current_time} \n {current_date}"
        self.date_time.configure(text=set_text, font=("", 20, "bold"), bd=0, bg="white", fg="black")
        self.date_time.after(100, self.show_time)

    def key_pressed(self, event):
        key = event.keysym
        if key == 'w' or key == 'a' or key == 's' or key == 'd':
        # Si se presiona una de las teclas de movimiento, el robot está en movimiento
         self.is_moving = True
         self.people_left.configure(text="NO")
         self.update_moving_label(key)
        
        elif key == 'q':
        # Si se presiona la tecla Q y el robot estaba en movimiento, ahora se detiene
         if self.is_moving:
            self.people_left.configure(text="YES")
            self.is_moving = False
            # Si el robot se detiene, actualiza el label de movimiento para indicar que está parado
            self.Moving.configure(text=" ")

    def update_moving_label(self, direction):
        # Actualiza el label de movimiento según la dirección
        if direction == 'w':
            self.Moving.configure(text="Forward")
        elif direction == 's':
            self.Moving.configure(text="Backward")
        elif direction == 'a':
            self.Moving.configure(text="Left")
        elif direction == 'd':
            self.Moving.configure(text="Right")


def wind():
    window = Tk()
    Dashboard2(window)
    window.mainloop()


if __name__ == '__main__':
    wind()


