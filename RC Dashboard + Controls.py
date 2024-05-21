from tkinter import *
import time
import threading
import picar
from picar import front_wheels, back_wheels
from RPi import GPIO

# Setup for the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)  # Channel 1 for forward/backward
GPIO.setup(27, GPIO.IN)  # Channel 2 for left/right

# Initialize the PiCar components
picar.setup()
fw = front_wheels.Front_Wheels()
bw = back_wheels.Back_Wheels()

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

        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='blue', font=("", 20, "bold"), bd=0, fg='white',
                                     cursor='hand2', activebackground='#32cf8e')
        self.dashboard_text.place(x=85, y=270)

        self.manage_text = Button(self.sidebar, text="Manage", bg='green', font=("", 20, "bold"), bd=0, fg='white',
                                  cursor='hand2', activebackground='#32cf8e')
        self.manage_text.place(x=85, y=375)

        self.settings_text = Button(self.sidebar, text="Settings", bg='grey', font=("", 20, "bold"), bd=0, fg='white',
                                    cursor='hand2', activebackground='#32cf8e')
        self.settings_text.place(x=85, y=475)

        self.Exit_text = Button(self.sidebar, text="Stop", bg='red', font=("", 20, "bold"), bd=0, fg='white',
                                cursor='hand2', activebackground='#32cf8e', command=self.window.destroy)
        self.Exit_text.place(x=85, y=575)

        self.pieChart = Label(self.bodyFrame1, bg='#ffffff')
        self.pieChart.place(x=690, y=70)

        self.graph = Label(self.bodyFrame1, bg='#ffffff')
        self.graph.place(x=40, y=70)

        self.Moving = Label(self.bodyFrame2, text='', bg='#009aa5', font=("", 25, "bold"), anchor="center", justify="center", width=10)
        self.Moving.place(x=50, y=100)

        self.Moving_label = Label(self.bodyFrame2, text="Moving", bg='#009aa5', font=("", 40, "bold"), fg='white')
        self.Moving_label.place(x=5, y=5)

        self.people_left = Label(self.bodyFrame3, text='YES', bg='#e21f26', font=("", 25, "bold"), anchor="center", justify="center", width=10)
        self.people_left.place(x=50, y=100)

        self.parked = Label(self.bodyFrame3, bg='#e21f26')
        self.parked.place(x=220, y=0)

        self.parked_label = Label(self.bodyFrame3, text="Parked", bg='#e21f26', font=("", 40, "bold"), fg='white')
        self.parked_label.place(x=5, y=5)

        self.voltage = Label(self.bodyFrame4, text='5 V', bg='#ffcb1f', font=("", 25, "bold"), anchor="center", justify="center", width=10)
        self.voltage.place(x=50, y=100)

        self.voltage_label = Label(self.bodyFrame4, text="Voltage", bg='#ffcb1f', font=("", 40, "bold"), fg='white')
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

        # Start the RC control thread
        self.rc_thread = threading.Thread(target=self.rc_control)
        self.rc_thread.daemon = True
        self.rc_thread.start()

    def show_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime('%Y/%m/%d')
        set_text = f"  {current_time} \n {current_date}"
        self.date_time.configure(text=set_text, font=("", 20, "bold"), bd=0, bg="white", fg="black")
        self.date_time.after(1000, self.show_time)

    # Function to read PWM signals from RC receiver
    def read_pwm(self, channel):
        GPIO.setup(channel, GPIO.IN)
        while GPIO.input(channel) == GPIO.LOW:
            start = time.time()
        while GPIO.input(channel) == GPIO.HIGH:
            end = time.time()
        return (end - start) * 1000000

    # Control functions
    def forward(self):
        bw.forward()
        bw.speed = 95  # Set speed, adjust as necessary
        self.update_moving_label("Forward")

    def backward(self):
        bw.backward()
        bw.speed = 70  # Set speed, adjust as necessary
        self.update_moving_label("Backward")

    def stop(self):
        bw.stop()
        self.update_moving_label("Stopped")

    def turn_left(self):
        fw.turn_left()
        self.update_moving_label("Left")

    def turn_right(self):
        fw.turn_right()
        self.update_moving_label("Right")

    def straight(self):
        fw.turn_straight()

    def update_moving_label(self, direction):
        self.Moving.configure(text=direction)
        if direction == "Stopped":
            self.people_left.configure(text="YES")
        else:
            self.people_left.configure(text="NO")

    # Thread to handle RC commands
    def rc_control(self):
        while True:
            ch1 = self.read_pwm(17)
            ch2 = self.read_pwm(27)

            # Threshold values may need adjusting based on your RC setup
            if ch1 < 1500:
                self.forward()
            elif ch1 > 1500:
                self.backward()
            else:
                self.stop()

            if ch2 < 1500:
                self.turn_left()
            elif ch2 > 1500:
                self.turn_right()
            else:
                self.straight()

            time.sleep(0.1)

def wind():
    window = Tk()
    Dashboard2(window)
    window.mainloop()

if __name__ == '__main__':
    wind()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program terminated.")
        time.sleep(1)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Program terminated.")


