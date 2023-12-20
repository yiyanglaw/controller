import tkinter as tk
from tkinter import messagebox, Menu
from PIL import Image
from PIL import ImageTk
import webbrowser
import RPi.GPIO as GPIO
import time



class RobotControllerApp:
    def __init__(self, root):
        GPIO.setmode(GPIO.BCM)
        self.root = root
        self.root.title("Robot Controller App")
        self.root.geometry("680x400")

        # Variables for login
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Instance variables for button images
        self.button1_image = tk.PhotoImage(file="/home/pi/Downloads/Newf/up.png")
        self.button2_image = tk.PhotoImage(file="/home/pi/Downloads/Newf/left.png")
        self.button3_image = tk.PhotoImage(file="/home/pi/Downloads/Newf/stop.png")
        self.button4_image = tk.PhotoImage(file="/home/pi/Downloads/Newf/right.png")
        self.button5_image = tk.PhotoImage(file="/home/pi/Downloads/Newf/down.png")

        # Convert JPEG to GIF
        self.convert_to_gif("/home/pi/Downloads/Newf/4k.jpg",
                            "/home/pi/Downloads/Newf/4k.gif")
        self.convert_to_gif("/home/pi/Downloads/Newf/4k7.jpg",
                            "/home/pi/Downloads/Newf/4k7.gif")

        # Load background images
        # Make image objects class attributes
        self.login_bg_image = ImageTk.PhotoImage(file="/home/pi/Downloads/Newf/4k.gif")
        self.menu_bg_image = ImageTk.PhotoImage(file="/home/pi/Downloads/Newf/4k7.gif")


        # Login Page
        self.login_frame = tk.Frame(root)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # Set background image for login page
        login_bg_label = tk.Label(self.login_frame, image=self.login_bg_image)
        login_bg_label.place(relwidth=1, relheight=1)
        
        # Add text "Yang Robot GUI" above the username label
        tk.Label(self.login_frame, text="Yang Robot Gui", font=("Helvetica", 16)).pack(pady=30)

        tk.Label(self.login_frame, text="Username:",font=("Helvetica", 16)).pack(pady=20)
        tk.Entry(self.login_frame, textvariable=self.username_var).pack(pady=10)

        tk.Label(self.login_frame, text="Password:",font=("Helvetica", 16)).pack(pady=10)
        tk.Entry(self.login_frame, textvariable=self.password_var, show="*").pack(pady=10)

        tk.Button(self.login_frame, text="Login",font=("Helvetica", 16), command=self.login).pack(pady=10)

        # Center the widgets both vertically and horizontally
        self.center_widgets()
        
        # Definition of RGB module pin
        self.LED_R = 22
        self.LED_G = 27
        self.LED_B = 24
        # Definition of motor control pins
        self.IN1 = 20
        self.IN2 = 21
        self.IN3 = 19
        self.IN4 = 26
        self.ENA = 16
        self.ENB = 13
        
        # Definition of buzzer pin
        self.buzzer = 8

        # Set up buzzer pin
        GPIO.setup(self.buzzer, GPIO.OUT)
        GPIO.output(self.buzzer, GPIO.HIGH)  # Initially set the buzzer to HIGH (off)


        # Motor control pins initialization
        self.motor_init()

        # GPIO cleanup function when the program exits
        root.protocol("WM_DELETE_WINDOW", self.cleanup_gpio)
        
        # Add a delay before starting motor control
        time.sleep(2)


        # Set the GPIO port to BCM encoding mode.
        GPIO.setmode(GPIO.BCM)

        # RGB pins are initialized into output mode
        GPIO.setup(self.LED_R, GPIO.OUT)
        GPIO.setup(self.LED_G, GPIO.OUT)
        GPIO.setup(self.LED_B, GPIO.OUT)


    def center_widgets(self):
        # Get the frame size
        frame_width = self.login_frame.winfo_reqwidth()
        frame_height = self.login_frame.winfo_reqheight()

        # Center the widgets vertically and horizontally
        x = (self.root.winfo_screenwidth() - frame_width) // 2
        y = (self.root.winfo_screenheight() - frame_height) // 2

        self.root.geometry("+%d+%d" % (x, y))

    def convert_to_gif(self, input_path, output_path):
        try:
            img = Image.open(input_path)
            img.save(output_path, "GIF")
            print(f"Conversion successful: {output_path}")
        except Exception as e:
            print(f"Error during conversion: {e}")

    def login(self):
        # Dummy credentials (replace with your authentication logic)
        valid_username = "a"
        valid_password = "a"

        entered_username = self.username_var.get()
        entered_password = self.password_var.get()

        if entered_username == valid_username and entered_password == valid_password:
            # If credentials are valid, show menu page
            self.show_menu_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_menu_page(self):
        # Destroy login frame and show menu frame
        self.login_frame.destroy()

        # Menu Page
        self.menu_frame = tk.Frame(self.root)
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        # Use ImageTk.PhotoImage to load the images
        # Load background images


        # Set background image for menu page
        menu_bg_label = tk.Label(self.menu_frame, image=self.menu_bg_image)
        menu_bg_label.place(relwidth=1, relheight=1)

        # Load button images using instance variables
        button1 = tk.Button(self.menu_frame, image=self.button1_image, command=self.button1_action)
        button2 = tk.Button(self.menu_frame, image=self.button2_image, command=self.button2_action)
        button3 = tk.Button(self.menu_frame, image=self.button3_image, command=self.button3_action)
        button4 = tk.Button(self.menu_frame, image=self.button4_image, command=self.button4_action)
        button5 = tk.Button(self.menu_frame, image=self.button5_image, command=self.button5_action)

        # Place buttons at specific coordinates
        button1.place(x=74, y=400)
        button2.place(x=0, y=474)
        button3.place(x=74, y=474)
        button4.place(x=152, y=474)
        button5.place(x=74, y=552)

        # Create 8 more buttons with text 1 to 8
        button6 = tk.Button(self.menu_frame, text="ACC", font=("Helvetica", 12), command=self.button6_action,width=7, height=3)
        button6.place(x=300, y=546)

        button7 = tk.Button(self.menu_frame, text="DEC", font=("Helvetica", 12), command=self.button7_action,width=7, height=3)
        button7.place(x=400, y=546)

        button8 = tk.Button(self.menu_frame, text="BEEP", font=("Helvetica", 12), command=self.button8_action,width=7, height=3)
        button8.place(x=500, y=546)

        button9 = tk.Button(self.menu_frame, text="MODE", font=("Helvetica", 12), command=self.button9_action,width=7, height=3)
        button9.place(x=600, y=546)
        
        
        button10 = tk.Button(self.menu_frame, text="OFF", font=("Helvetica", 12), command=self.button10_action,width=7, height=3)
        button10.place(x=700, y=546)

        button11 = tk.Button(self.menu_frame, text="RED", font=("Helvetica", 12), command=self.button11_action,width=7, height=3)
        button11.place(x=800, y=546)

        button12 = tk.Button(self.menu_frame, text="GREEN", font=("Helvetica", 12), command=self.button12_action,width=7, height=3)
        button12.place(x=900, y=546)

        button13 = tk.Button(self.menu_frame, text="BLUE", font=("Helvetica", 12), command=self.button13_action,width=7, height=3)
        button13.place(x=1000, y=546)
        
        button14 = tk.Button(self.menu_frame, text="SPIN L", font=("Helvetica", 12), command=self.button14_action,width=7, height=3)
        button14.place(x=1100, y=546)
        
        button15 = tk.Button(self.menu_frame, text="SPIN R", font=("Helvetica", 12), command=self.button15_action,width=7, height=3)
        button15.place(x=1200, y=546)

        
        # Create menus
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        robot_programs_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Robot Programs", menu=robot_programs_menu)

        # Add options to the "Robot Programs" menu
        robot_programs_menu.add_command(label="Black Line Tracking", command=self.robot_program_1_action)
        robot_programs_menu.add_command(label="Light Following", command=self.robot_program_2_action)
        robot_programs_menu.add_command(label="RGB_LED", command=self.robot_program_3_action)
        robot_programs_menu.add_command(label="Option 4", command=self.robot_program_4_action)
        robot_programs_menu.add_command(label="Option 5", command=self.robot_program_5_action)
        robot_programs_menu.add_command(label="Option 6", command=self.robot_program_6_action)
        robot_programs_menu.add_command(label="Option 7", command=self.robot_program_7_action)
        robot_programs_menu.add_command(label="Option 8", command=self.robot_program_8_action)
        robot_programs_menu.add_command(label="Option 9", command=self.robot_program_9_action)
        robot_programs_menu.add_command(label="Option 10", command=self.robot_program_10_action)
        # Add commands for options 3 to 40 similarly

        about_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About me", command=self.about_me_action)


    # Define the functions for the buttons
    def button1_action(self):
        # Set the initial speed
        self.speed = 50
        self.move_forward()

    def button2_action(self):
        self.move_left()

    def button3_action(self):
        self.stop_robot()

    def button4_action(self):
        self.move_right()

    def button5_action(self):
        self.move_backward()

        # Define the functions for the additional buttons
    def button6_action(self):
        # Check if the speed has been initialized by clicking the "Move Forward" button
        if hasattr(self, 'speed'):
            # Accelerate by increasing the speed
            self.speed += 10
            if self.speed > 100:
                self.speed = 100  # Limit the speed to 100
            self.move_forward()
        else:
            messagebox.showwarning("Warning", "Please click 'Move Forward' first to set the initial speed.")

    def button7_action(self):
        # Check if the speed has been initialized by clicking the "Move Forward" button
        if hasattr(self, 'speed'):
            # Decelerate by decreasing the speed
            self.speed -= 10
            if self.speed < 0:
                self.speed = 0  # Limit the speed to 0
            self.move_forward()
        else:
            messagebox.showwarning("Warning", "Please click 'Move Forward' first to set the initial speed.")

    def button8_action(self):
        self.whistle()
        
    def button9_action(self):
        messagebox.showinfo("Button MODE", "Button 9 clicked")

    def button10_action(self):
        # Turn off the LEDs when the "OFF" button is clicked
        self.turn_off_leds()

    def button11_action(self):
        # Change the LED color to RED when the "RED" button is clicked
        self.set_led_color(GPIO.HIGH, GPIO.LOW, GPIO.LOW)

    def button12_action(self):
        # Change the LED color to GREEN when the "GREEN" button is clicked
        self.set_led_color(GPIO.LOW, GPIO.HIGH, GPIO.LOW)

    def button13_action(self):
        # Change the LED color to BLUE when the "BLUE" button is clicked
        self.set_led_color(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
        
    def button14_action(self):
        self.spin_left(1)
    
    def button15_action(self):
        self.spin_right(1)
        

    def turn_off_leds(self):
        # Turn off all LEDs
        GPIO.output(self.LED_R, GPIO.LOW)
        GPIO.output(self.LED_G, GPIO.LOW)
        GPIO.output(self.LED_B, GPIO.LOW)

    def set_led_color(self, red, green, blue):
        # Set the LED color based on the provided parameters
        GPIO.output(self.LED_R, red)
        GPIO.output(self.LED_G, green)
        GPIO.output(self.LED_B, blue)
        # Define the functions for each robot program option (1 to 40)
        
    #black_line_tracking_action    
    def robot_program_1_action(self):
        try:
            # Definition of motor pins
            IN1 = 20
            IN2 = 21
            IN3 = 19
            IN4 = 26
            ENA = 16
            ENB = 13

            # Definition of button
            key = 8

            # TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
            # 3 5 4 18
            TrackSensorLeftPin1 = 3
            TrackSensorLeftPin2 = 5
            TrackSensorRightPin1 = 4
            TrackSensorRightPin2 = 18

            # Set the GPIO port to BCM encoding mode.
            GPIO.setmode(GPIO.BCM)

            # Ignore warning information
            GPIO.setwarnings(False)

            # Motor pins are initialized into output mode
            # Key pin is initialized into input mode
            # Track sensor module pins are initialized into input mode
            GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(key, GPIO.IN)
            GPIO.setup(TrackSensorLeftPin1, GPIO.IN)
            GPIO.setup(TrackSensorLeftPin2, GPIO.IN)
            GPIO.setup(TrackSensorRightPin1, GPIO.IN)
            GPIO.setup(TrackSensorRightPin2, GPIO.IN)
            # Set the PWM pin and frequency is 2000hz
            pwm_ENA = GPIO.PWM(ENA, 2000)
            pwm_ENB = GPIO.PWM(ENB, 2000)
            pwm_ENA.start(0)
            pwm_ENB.start(0)

            def run(leftspeed, rightspeed):
                GPIO.output(IN1, GPIO.HIGH)
                GPIO.output(IN2, GPIO.LOW)
                GPIO.output(IN3, GPIO.HIGH)
                GPIO.output(IN4, GPIO.LOW)
                pwm_ENA.ChangeDutyCycle(leftspeed)
                pwm_ENB.ChangeDutyCycle(rightspeed)

            def spin_right(leftspeed, rightspeed):
                GPIO.output(IN1, GPIO.HIGH)
                GPIO.output(IN2, GPIO.LOW)
                GPIO.output(IN3, GPIO.LOW)
                GPIO.output(IN4, GPIO.HIGH)
                pwm_ENA.ChangeDutyCycle(leftspeed)
                pwm_ENB.ChangeDutyCycle(rightspeed)

            # Other tracking.py code

            while True:
                # Your tracking.py loop logic here
                TrackSensorLeftValue1 = GPIO.input(TrackSensorLeftPin1)
                TrackSensorLeftValue2 = GPIO.input(TrackSensorLeftPin2)
                TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
                TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)

                # 4 tracking pins level status
                # 0 0 X 0
                # 1 0 X 0
                # 0 1 X 0
                # Turn right in place, speed is 50, delay 80ms
                # Handle right acute angle and right right angle
                if (TrackSensorLeftValue1 == False or TrackSensorLeftValue2 == False) and TrackSensorRightValue2 == False:
                    spin_right(35, 35)
                    time.sleep(0.08)

                # 4 tracking pins level status
                # 0 X 0 0
                # 0 X 0 1
                # 0 X 1 0
                # Turn right in place, speed is 50, delay 80ms
                # Handle left acute angle and left right angle
                elif TrackSensorLeftValue1 == False and (
                        TrackSensorRightValue1 == False or TrackSensorRightValue2 == False):
                    spin_left(35, 35)
                    time.sleep(0.08)

                # 0 X X X
                # Left_sensor1 detected black line
                elif TrackSensorLeftValue1 == False:
                    spin_left(35, 35)

                # X X X 0
                # Right_sensor2 detected black line
                elif TrackSensorRightValue2 == False:
                    spin_right(35, 35)

                # 4 tracking pins level status
                # X 0 1 X
                elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == True:
                    run(0, 40)

                # 4 tracking pins level status
                # X 1 0 X
                elif TrackSensorLeftValue2 == True and TrackSensorRightValue1 == False:
                    run(40, 0)

                # 4 tracking pins level status
                # X 0 0 X
                elif TrackSensorLeftValue2 == False and TrackSensorRightValue1 == False:
                    run(45, 45)

        except KeyboardInterrupt:
            pass
        pwm_ENA.stop()
        pwm_ENB.stop()
        GPIO.cleanup()

        
    def robot_program_2_action(self):
        # Definition of motor pins
        IN1 = 20
        IN2 = 21
        IN3 = 19
        IN4 = 26
        ENA = 16
        ENB = 13

        # Definition of button
        key = 8

        # Definition of photoresistor pin
        LdrSensorLeft = 7
        LdrSensorRight = 6

        # Set the GPIO port to BCM encoding mode.
        GPIO.setmode(GPIO.BCM)

        # Ignore warning information
        GPIO.setwarnings(False)

        def init():
            global pwm_ENA
            global pwm_ENB
            GPIO.setup(ENA, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(ENB, GPIO.OUT, initial=GPIO.HIGH)
            GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(key, GPIO.IN)
            GPIO.setup(LdrSensorLeft, GPIO.IN)
            GPIO.setup(LdrSensorRight, GPIO.IN)
            # Set the PWM pin and frequency is 2000hz
            pwm_ENA = GPIO.PWM(ENA, 2000)
            pwm_ENB = GPIO.PWM(ENB, 2000)
            pwm_ENA.start(0)
            pwm_ENB.start(0)

        # Advance
        def run():
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            pwm_ENA.ChangeDutyCycle(50)
            pwm_ENB.ChangeDutyCycle(50)

        # Back
        def back():
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            pwm_ENA.ChangeDutyCycle(50)
            pwm_ENB.ChangeDutyCycle(50)

        # Turn left
        def left():
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            pwm_ENA.ChangeDutyCycle(0)
            pwm_ENB.ChangeDutyCycle(50)

        # Turn right
        def right():
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.LOW)
            pwm_ENA.ChangeDutyCycle(50)
            pwm_ENB.ChangeDutyCycle(0)

        # Turn left in place
        def spin_left():
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            pwm_ENA.ChangeDutyCycle(50)
            pwm_ENB.ChangeDutyCycle(50)

        # Turn right in place
        def spin_right():
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            pwm_ENA.ChangeDutyCycle(50)
            pwm_ENB.ChangeDutyCycle(50)

        # Brake
        def brake():
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.LOW)

        def key_scan():
            while GPIO.input(key):
                pass
            while not GPIO.input(key):
                time.sleep(0.01)
                if not GPIO.input(key):
                    time.sleep(0.01)
                    while not GPIO.input(key):
                        pass

        # Delay 2s
        time.sleep(2)

        try:
            init()
            key_scan()
            while True:
                LdrSersorLeftValue = GPIO.input(LdrSensorLeft)
                LdrSersorRightValue = GPIO.input(LdrSensorRight)

                if LdrSersorLeftValue and LdrSersorRightValue:
                    run()
                elif LdrSersorLeftValue and not LdrSersorRightValue:
                    spin_left()
                    time.sleep(0.002)
                elif LdrSersorRightValue and not LdrSersorLeftValue:
                    spin_right()
                    time.sleep(0.002)
                elif not LdrSersorRightValue and not LdrSersorLeftValue:
                    brake()

        except KeyboardInterrupt:
            pass

        # Cleanup GPIO
        pwm_ENA.stop()
        pwm_ENB.stop()
        GPIO.cleanup()

    def robot_program_3_action(self):
        # Definition of RGB module pin
        LED_R = 22
        LED_G = 27
        LED_B = 24

        # Set the GPIO port to BCM encoding mode.
        GPIO.setmode(GPIO.BCM)

        # RGB pins are initialized into output mode
        GPIO.setup(LED_R, GPIO.OUT)
        GPIO.setup(LED_G, GPIO.OUT)
        GPIO.setup(LED_B, GPIO.OUT)

        try:
            # Continuously change the LED color
            while True:
                # Red
                self.set_led_color(GPIO.HIGH, GPIO.LOW, GPIO.LOW)
                time.sleep(1)

                # Green
                self.set_led_color(GPIO.LOW, GPIO.HIGH, GPIO.LOW)
                time.sleep(1)

                # Blue
                self.set_led_color(GPIO.LOW, GPIO.LOW, GPIO.HIGH)
                time.sleep(1)

        except KeyboardInterrupt:
            pass
        finally:
            # Cleanup GPIO
            GPIO.cleanup()

    def robot_program_4_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 4 clicked")
    def robot_program_5_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 5 clicked")
    def robot_program_6_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 6 clicked")
    def robot_program_7_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 7 clicked")
    def robot_program_8_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 8 clicked")
    def robot_program_9_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 9 clicked")
    def robot_program_10_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 10 clicked")    

    # Define functions for options 3 to 40 similarly
        
    # Define the empty functions for robot control options 1 to 40
    def about_me_action(self):
        # Replace the URL with the actual URL of your portfolio
        portfolio_url = "https://www.youtube.com/"
        webbrowser.open(portfolio_url)
        
        # Cleanup GPIO before exiting
        GPIO.cleanup()
        
    # Function to initialize motor control
    def motor_init(self):
        GPIO.setup(self.ENA, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN2, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.ENB, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(self.IN3, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.IN4, GPIO.OUT, initial=GPIO.LOW)
        # Set the PWM pin and frequency is 2000hz
        self.pwm_ENA = GPIO.PWM(self.ENA, 2000)
        self.pwm_ENB = GPIO.PWM(self.ENB, 2000)
        self.pwm_ENA.start(0)
        self.pwm_ENB.start(0)

    # Motor control functions
    def run(self, delaytime):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)

    def back(self, delaytime):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)

    def left(self, delaytime):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)

    def right(self, delaytime):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)

    def spin_left(self, delaytime):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)

    def spin_right(self, delaytime):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)

    def brake(self, delaytime):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(50)
        self.pwm_ENB.ChangeDutyCycle(50)
        time.sleep(delaytime)
    
    
     # Function to move the robot forward
    def move_forward(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        self.pwm_ENA.ChangeDutyCycle(self.speed)
        self.pwm_ENB.ChangeDutyCycle(self.speed)
        time.sleep(1)

    # Function to move the robot backward
    def move_backward(self):
        self.back(1)

    # Function to turn the robot left
    def move_left(self):
        self.left(1)

    # Function to turn the robot right
    def move_right(self):
        self.right(1)

    # Function to stop the robot
    def stop_robot(self):
        self.brake(1)
        
    def whistle(self):
        # Assuming you have defined the buzzer pin as buzzer (replace with your actual buzzer pin)
        buzzer = 8

        # Activate the buzzer
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(0.001)
        

    def cleanup_gpio(self):
        # Cleanup GPIO before exiting
        GPIO.cleanup()
        
        

    # Define the empty function for "About me"
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup_gpio)  # Handle window close event
    root.mainloop()

