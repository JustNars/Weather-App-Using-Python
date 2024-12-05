from customtkinter import *
from PIL import Image
import requests

class MainApp(CTk):
    def __init__(self):
        super().__init__()

        set_appearance_mode("dark")

        # set up the main window
        self.geometry("400x660")
        self.title("Nar's Weather App")
        self.resizable(False, False)
        self.iconbitmap("")

        # main frame
        self.main_frame = CTkFrame(self, corner_radius=20)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # display widgets
        self.show_menu()

    def show_menu(self):
        self.image1 = CTkImage(Image.open("weather-app-images/icon-cloud.png"), size=(160, 160))
        # labels
        self.title_label = CTkLabel(self.main_frame, text="Nar's Weather App", font=("Cascadia Code", 25), image=self.image1, compound=TOP)
        self.title_label.pack(side=TOP, pady=20)
        self.credits_label = CTkLabel(self.main_frame, text="Made By", font=("Cascadia Code", 15))
        self.credits_label.pack(side=TOP, pady=10)
        self.credits_label2 = CTkLabel(self.main_frame, text="JustNars", font=("Cascadia Code", 20))
        self.credits_label2.pack(side=TOP)
        self.seg_label = CTkLabel(self.main_frame, text="Choose A Theme", font=("Cascadia Code", 25))
        self.seg_label.pack(side=BOTTOM)

        # buttons
        self.continue_button = CTkButton(self.main_frame, text="Continue", font=("Cascadia Code", 20), fg_color="#a3aab5", corner_radius=10,
                                         hover_color="Gray", width=60, height=40, command=self.show_main_app)
        self.continue_button.pack(side=TOP, pady=60)
        self.seg = CTkSegmentedButton(self.main_frame, values=["Dark", "Light"], font=("Cascadia Code", 20), fg_color="Gray",
                                      corner_radius=10, selected_color="#8b929e", selected_hover_color="#8b929e", command=self.theme)
        self.seg.pack(side=BOTTOM, pady=20)
        self.seg.set("Dark")

    def show_main_app(self):
        for child in self.main_frame.winfo_children():
            child.destroy()
        # Frames
        self.frame_display_1 = CTkFrame(self.main_frame, height=190, width=150, corner_radius=20, fg_color="#363836")
        self.frame_display_1.place(x=20, y=415)

        self.frame_display_2 = CTkFrame(self.main_frame, height=190, width=150, corner_radius=20, fg_color="#363836")
        self.frame_display_2.place(x=190, y=415)

        # Entry
        self.entry_box = CTkEntry(self.main_frame, placeholder_text="Search a City", font=("Cascadia Code", 15), corner_radius=10, width=300, height=40)
        self.entry_box.pack(pady=15)
        self.entry_box.bind("<Return>", self.get_weather)

        # images
        self.weather_image = CTkImage(Image.open("weather-app-images/sun.png"), size=(150, 150))
        self.humity_image = CTkImage(Image.open("weather-app-images/haze.png"), size=(30, 30))
        self.wind_image = CTkImage(Image.open("weather-app-images/wind.png"), size=(30, 30))
        
        # Labels
        self.big_title = CTkLabel(self.main_frame, text="", font=("Cascadia Code", 35))
        self.big_title.pack(side=TOP)
        self.des_label = CTkLabel(self.main_frame, text="", font=("Cascadia Code", 15))
        self.des_label.pack(side=TOP, pady=8)
        self.display_image = CTkLabel(self.main_frame, text="", image=self.weather_image)
        self.display_image.pack(side=TOP)
        self.stat_label = CTkLabel(self.main_frame, text="", font=("Cascadia Code", 20))
        self.stat_label.pack(side=TOP, pady=8)
        self.temp_label = CTkLabel(self.main_frame, text="", font=("Arial", 35))
        self.temp_label.pack(side=TOP)
        self.max_temp = CTkLabel(self.main_frame, text="", font=("Cascadia Code", 15))
        self.max_temp.place(x=20, y=360)
        self.min_temp = CTkLabel(self.main_frame, text="", font=("Cascadia Code", 15))
        self.min_temp.place(x=262, y=360)
        self.wind_label = CTkLabel(self.frame_display_1, text=" Wind", font=("Cascadia Code", 20), image=self.wind_image, compound=LEFT)
        self.wind_label.place(x=8,y=20)
        self.humity_label = CTkLabel(self.frame_display_1, text=" Humidity", font=("Cascadia Code", 20), image=self.humity_image, compound=LEFT)
        self.humity_label.place(x=8, y=95)

    def get_weather(self, event):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = { "q": self.entry_box.get(), "appid": "17d678349374714a0cb8702690a57526", "units": "metric"}
        try:
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                weather_data = response.json()

                # don't try to read this block of code. your welcome.
                self.big_title.configure(text=self.entry_box.get().capitalize(), font=("Cascadia Code", 35))
                self.des_label.configure(text=f"City/State in {weather_data["sys"]["country"]}")
                self.stat_label.configure(text=weather_data["weather"][0]["description"].title())
                self.temp_label.configure(text=f"{weather_data["main"]["temp"]}°C")
                self.wind_label.configure(text=f" Wind\n{weather_data["wind"]["speed"]}km/h")
                self.humity_label.configure(text=f" Humidity\n{weather_data["main"]["humidity"]}%")
                self.max_temp.configure(text=f"Max Temp: \n{weather_data["main"]["temp_max"]}°C")
                self.min_temp.configure(text=f"Min Temp: \n{weather_data["main"]["temp_min"]}°C")

                weather = weather_data["weather"][0]["main"]

                # learned this trick from a friend. can't stop using it xd
                if weather in ("Clear", "Clouds", "Rain", "Drizzle", "Thunderstorm", "Snow"):
                     my_lovely_dir_string = f"weather-app-images/{weather}.png"
                     self.display_image.configure(image=CTkImage(Image.open(my_lovely_dir_string), size=(150, 150)))
                else:
                     self.display_image.configure(image=CTkImage(Image.open("weather-app-images/mist.png"), size=(150, 150)))
                          
            else:
                for children in self.main_frame.winfo_children():
                     children.destroy()    
                self.show_main_app()
                self.big_title.configure(text="Error: City Not Found", font=("Cascadia Code", 20))
        except Exception as e:
             self.big_title.configure(text="Error: City Not Found", font=("Cascadia Code", 15))

    def theme(self, value):
        try:
            if value == "Light":
                set_appearance_mode("light")
                self.frame_display_1.configure(fg_color="#9a9da1")
                self.frame_display_2.configure(fg_color="#9a9da1")
            else:
                set_appearance_mode("dark")
                self.frame_display_1.configure(fg_color="#363836")
                self.frame_display_2.configure(fg_color="#363836")
        except Exception: pass

if __name__ == "__main__":
    MainApp().mainloop()
