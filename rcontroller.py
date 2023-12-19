import tkinter as tk
from tkinter import messagebox, Menu
from PIL import Image
from PIL import ImageTk
import webbrowser
import RPi.GPIO as GPIO
import time


class RobotControllerApp:
    def __init__(self, root):
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
        
        
        

        
        # Create menus
        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        robot_programs_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Robot Programs", menu=robot_programs_menu)

        # Add options to the "Robot Programs" menu
        robot_programs_menu.add_command(label="Option 1", command=self.robot_program_1_action)
        robot_programs_menu.add_command(label="Option 2", command=self.robot_program_2_action)
        robot_programs_menu.add_command(label="Option 3", command=self.robot_program_3_action)
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
        messagebox.showinfo("Button UP", "Button 1 clicked")

    def button2_action(self):
        messagebox.showinfo("Button LEFT", "Button 2 clicked")

    def button3_action(self):
        messagebox.showinfo("Button STOP", "Button 3 clicked")

    def button4_action(self):
        messagebox.showinfo("Button RIGHT", "Button 4 clicked")

    def button5_action(self):
        messagebox.showinfo("Button DOWN", "Button 5 clicked")
        
        # Define the functions for the additional buttons
    def button6_action(self):
        messagebox.showinfo("Button ACC", "Button 6 clicked")

    def button7_action(self):
        messagebox.showinfo("Button DEC", "Button 7 clicked")

    def button8_action(self):
        messagebox.showinfo("Button BEEP", "Button 8 clicked")

    def button9_action(self):
        messagebox.showinfo("Button MODE", "Button 9 clicked")

    def button10_action(self):
        # Turn off the LEDs when the "OFF" button is clicked
        self.turn_off_leds()

    def button11_action(self):
        # Change the LED color to RED when the "RED" button is clicked
        self.turn_off_leds()
        self.set_led_color(GPIO.HIGH, GPIO.LOW, GPIO.LOW)

    def button12_action(self):
        # Change the LED color to GREEN when the "GREEN" button is clicked
        self.turn_off_leds()
        self.set_led_color(GPIO.LOW, GPIO.HIGH, GPIO.LOW)

    def button13_action(self):
        # Change the LED color to BLUE when the "BLUE" button is clicked
        self.turn_off_leds()
        self.set_led_color(GPIO.LOW, GPIO.LOW, GPIO.HIGH)

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
    def robot_program_1_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 1 clicked")

    def robot_program_2_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 2 clicked")
    def robot_program_3_action(self):
        messagebox.showinfo("Robot Program", "Robot Program 3 clicked")
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
    def cleanup_gpio(self):
        # Cleanup GPIO before exiting
        GPIO.cleanup()
        

    # Define the empty function for "About me"
if __name__ == "__main__":
    root = tk.Tk()
    app = RobotControllerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.cleanup_gpio)  # Handle window close event
    root.mainloop()

