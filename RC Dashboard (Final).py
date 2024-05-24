import time
import cv2
import threading 
from picar import front_wheels, back_wheels
from picar.SunFounder_PCA9685 import Servo
import picar
from RPi import GPIO

# Setup for the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN)  # Channel 1 for forward/backward
GPIO.setup(12, GPIO.IN)  # Channel 2 for left/right

picar.setup()
rear_wheels_enable = True
front_wheels_enable = True
bw = back_wheels.Back_Wheels()
fw = front_wheels.Front_Wheels()
picar.setup()
fw.offset = 0
bw.speed = 0
fw.turn(72)
cap = cv2.VideoCapture(0)

width, height = 225, 350  # Width of camera, Height of Camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


class Dashboard2:
    def __init__(self, window):
        self.window = window
        self.window.title("Atlas Dashboard")
        self.window.geometry("1000x750")
        self.window.resizable(0, 0)
        self.window.state('normal')
        self.window.config(background='#eff5f6')

        self.header = Frame(self.window, bg='#009df4')
        self.header.place(x=300, y=0, width=900, height=60)

        self.sidebar = Frame(self.window, bg='#ffffff')
        self.sidebar.place(x=0, y=0, width=300, height=800)

        self.heading = Label(self.window, text='HANDCRAFT — Atlas Dashboard', font=("", 15, "bold"), fg='#0064d3', bg='#eff5f6')
        self.heading.place(x=325, y=70)
        
        # Here is the frame where the camera goes
        self.bodyFrame1 = Frame(self.window, bg='#ffffff')
        self.bodyFrame1.place(x=328, y=110, width=645, height=450)
        
        # BodyFrame Status
        self.bodyFrame2 = Frame(self.window, bg='#009aa5')
        self.bodyFrame2.place(x=328, y=600, width=200, height=125)
        
        # BodyFrame Parked
        self.bodyFrame3 = Frame(self.window, bg='#e21f26')
        self.bodyFrame3.place(x=550, y=600, width=200, height=125)
        
        # BodyFrame Voltage
        self.bodyFrame4 = Frame(self.window, bg='#ffcb1f')
        self.bodyFrame4.place(x=770, y=600, width=200, height=125)
        

        self.TeamName = Label(self.sidebar, text='Club de Robótica', bg='#ffffff', font=("", 20, "bold"))
        self.TeamName.place(x=35, y=150)


        self.dashboard_text = Button(self.sidebar, text="Dashboard", bg='blue', font=("", 20, "bold"), bd=0, fg= 'white',
                        cursor='hand2', activebackground='#32cf8e')
        self.dashboard_text.place(x=70, y=270)

        self.manage_text = Button(self.sidebar, text="Manage", bg='green', font=("", 20, "bold"), bd=0, fg = 'white',
                        cursor='hand2', activebackground='#32cf8e')
        self.manage_text.place(x=70, y=375)

        self.settings_text = Button(self.sidebar, text="Settings", bg='grey', font=("", 20, "bold"), bd=0, fg = 'white',
                        cursor='hand2', activebackground='#32cf8e')
        self.settings_text.place(x=70, y=475)

        self.Exit_text = Button(self.sidebar, text="Stop", bg='red', font=("", 20, "bold"), bd=0, fg= 'white',
                        cursor='hand2', activebackground='#32cf8e', command=self.window.destroy)
        self.Exit_text.place(x=70, y=575)




        self.Moving = Label(self.bodyFrame2, text='', bg='#009aa5', font=("", 18, "bold"), anchor="center", justify="center", width=10)
        self.Moving.place(x=20, y=65)


        self.Moving_label = Label(self.bodyFrame2, text="Status:", bg='#009aa5', font=("", 25, "bold"), fg='white')
        self.Moving_label.place(x=40, y=5)


        self.Parking_Status = Label(self.bodyFrame3, text= 'YES', bg='#e21f26', font=("", 18, "bold"), anchor="center", justify="center", width=10)
        self.Parking_Status.place(x=20, y=65)


        self.Parked = Label(self.bodyFrame3, bg='#e21f26')
        self.Parked.place(x=220, y=0)

        self.Parked_label = Label(self.bodyFrame3, text="Parked:", bg='#e21f26', font=("", 25, "bold"), fg='white')
        self.Parked_label.place(x=40, y=5)


        self.voltage = Label(self.bodyFrame4, text='7.5 V', bg='#ffcb1f', font=("", 18, "bold"),  anchor="center", justify="center", width=10)
        self.voltage.place(x=20, y=65)


        self.voltage_label = Label(self.bodyFrame4, text="Voltage", bg='#ffcb1f', font=("", 25, "bold"), fg='white')
        self.voltage_label.place(x=40, y=5)
        

        self.date_time = Label(self.window)
        self.date_time.place(x=80, y=15)
        self.show_time()

        # Variable para rastrear el estado del movimiento
        self.is_moving = False
        
        self.camera_frame = Label(self.bodyFrame1, bg='#ffffff')
        self.camera_frame.place(x=350, y=130)

        self.start_camera()
        self.start_movement()
        
        
    def show_time(self):
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime('%Y/%m/%d')
        set_text = f"  {current_time} \n {current_date}"
        self.date_time.configure(text=set_text, font=("", 20, "bold"), bd=0, bg="white", fg="black")
        self.date_time.after(100, self.show_time)


    def start_camera(self):
        def cam():
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (226, 200))
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_frame.imgtk = imgtk
                self.camera_frame.configure(image=imgtk)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

        threading.Thread(target=cam, daemon=True).start()


    def start_movement(self):
        def movement():
            def read_pwm(channel):
                GPIO.setup(channel, GPIO.IN)
                start = time.time()
                while GPIO.input(channel) == GPIO.LOW:
                    start = time.time()
                while GPIO.input(channel) == GPIO.HIGH:
                    end = time.time()
                duration = (end - start) * 1000000
                return duration

            def forward():
                bw.forward()
                bw.speed = 70


            def backward():
                bw.backward()
                bw.speed = 95


            def stop():
                bw.stop()


            def turn_left():
                fw.turn_left()


            def turn_right():
                fw.turn
        

            def straight():
                fw.turn_straight()


            def rc_control():
                while True:
                    ch1 = read_pwm(13)
                    ch2 = read_pwm(12)

                    if ch1 < 1300:
                        forward()
                        self.Moving.configure(text="Forward")

                    elif ch1 > 1700:
                        backward()
                        self.Moving.configure(text="Backward")


                    else:
                        stop()
                        self.Moving.configure(text="Stopping")


                    if ch2 < 800:
                        turn_left()
                        self.Moving.configure(text="Left")

                    elif ch2 > 1000:
                        turn_right()
                        self.Moving.configure(text="Right")

                    else:
                        straight()

                    time.sleep(0.1)

            rc_thread = threading.Thread(target=rc_control)
            rc_thread.daemon = True
            rc_thread.start()

        threading.Thread(target=movement, daemon=True).start()


    def update_labels(self, action):
        self.Moving.configure(text=action)
        self.Parking_Status.configure(text="NO")


    def reset_labels(self):
        self.Moving.configure(text="")
        self.Parking_Status.configure(text="YES")


def wind():
    window = Tk()
    Dashboard2(window)
    window.mainloop()

if __name__ == '__main__':
    wind()
