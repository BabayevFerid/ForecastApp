import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class WeatherApp:
    def __init__(self, root):
        # API KEY - Enter your WeatherAPI key here
        self.api_key = "YOUR_WEATHERAPI_KEY_HERE"
        
        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        
        # Initialize city list (BUG FIX: Added this line)
        self.cities = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "New York", "London", "Berlin"]
        
        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI elements"""
        # Title
        title_label = ttk.Label(self.root, text="Weather Forecast", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # City entry field
        city_frame = ttk.Frame(self.root)
        city_frame.pack(pady=5)
        
        ttk.Label(city_frame, text="City Name:", font=("Arial", 10)).pack(side="left", padx=5)
        
        self.city_entry = ttk.Combobox(city_frame, font=("Arial", 10), width=25)
        self.city_entry.pack(side="left")
        self.city_entry["values"] = self.cities  # Now self.cities is defined
        
        # Query button
        self.query_button = ttk.Button(self.root, text="Get Weather", command=self.get_weather)
        self.query_button.pack(pady=10)
        
        # Results frame
        self.result_frame = ttk.LabelFrame(self.root, text="Weather Information")
        self.result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Result labels
        self.location_label = ttk.Label(self.result_frame, text="", font=("Arial", 12, "bold"))
        self.location_label.pack(pady=5)
        
        self.temp_label = ttk.Label(self.result_frame, text="", font=("Arial", 10))
        self.temp_label.pack(anchor="w", padx=10)
        
        self.condition_label = ttk.Label(self.result_frame, text="", font=("Arial", 10))
        self.condition_label.pack(anchor="w", padx=10)
        
        self.humidity_label = ttk.Label(self.result_frame, text="", font=("Arial", 10))
        self.humidity_label.pack(anchor="w", padx=10)
        
        self.wind_label = ttk.Label(self.result_frame, text="", font=("Arial", 10))
        self.wind_label.pack(anchor="w", padx=10)
        
        # Status update
        self.status_label = ttk.Label(self.root, text="Ready", relief="sunken", anchor="w")
        self.status_label.pack(fill="x", padx=5, pady=5)
    
    def get_weather(self):
        """Get weather information"""
        city = self.city_entry.get().strip()
        
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        self.query_button.config(state="disabled")
        self.status_label.config(text="Fetching data...")
        self.root.update()
        
        try:
            url = f"http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}&lang=en"
            response = requests.get(url)
            data = response.json()
            
            if "error" in data:
                messagebox.showerror("Error", f"{data['error']['message']}")
                return
            
            # Process data
            location = data["location"]
            current = data["current"]
            
            # Update UI
            self.location_label.config(text=f"{location['name']}, {location['country']}")
            self.temp_label.config(text=f"🌡 Temperature: {current['temp_c']}°C")
            self.condition_label.config(text=f"☁ Condition: {current['condition']['text']}")
            self.humidity_label.config(text=f"💧 Humidity: %{current['humidity']}")
            self.wind_label.config(text=f"🌬 Wind: {current['wind_kph']} km/h")
            
            self.status_label.config(text="Data retrieved successfully")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not connect to API: {e}")
            self.status_label.config(text="Connection error")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_label.config(text="Error occurred")
        finally:
            self.query_button.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
