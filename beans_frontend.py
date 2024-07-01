import tkinter as tk
from PIL import Image, ImageTk
import webbrowser
import os

lastClickX = 0
lastClickY = 0

def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y

def Dragging(event):
    x, y = event.x - lastClickX + window.winfo_x(), event.y - lastClickY + window.winfo_y()
    window.geometry("+%s+%s" % (x , y))

def show_image_in_bottom_right(image_path, max_width=300, max_height=300):
    global window  # Make window global so it can be accessed in Dragging function
    
    # Create the main window
    root = tk.Tk()
    # Hide the root window initially
    root.withdraw()
    
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Load the image
    image = Image.open(image_path).convert("RGBA")  # Ensure the image is in RGBA mode
    
    # Get original dimensions
    original_width, original_height = image.size
    new_width, new_height = original_width, original_height
    
    # Resize the image if max_width or max_height is specified
    if max_width or max_height:
        aspect_ratio = original_width / original_height
        if max_width and original_width > max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        if max_height and new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
    
    # Resize the image
    try:
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    except AttributeError:
        image = image.resize((new_width, new_height), Image.LANCZOS)
    
    photo = ImageTk.PhotoImage(image)
    
    # Create a new window to display the image
    window = tk.Toplevel(root)
    window.overrideredirect(1)  # Remove window borders
    window.geometry(f"{photo.width()}x{photo.height()}+{screen_width - photo.width()}+{screen_height - photo.height()}")
    window.attributes('-topmost', True)  # Keep the window on top
    window.attributes('-alpha', 0.0)  # Set initial transparency of the window
    
    window.bind('<Button-1>', SaveLastClickPos)
    window.bind('<B1-Motion>', Dragging)
    
    # Add the image to a label and pack it into the window
    label = tk.Label(window, image=photo)
    label.pack()
    
    # Update the window to appear in the bottom right corner
    window.update()
    
    # Set the window's alpha to 1 (fully opaque) after updating the window's geometry
    window.attributes('-alpha', 1.0)
    
    # Keep the window open
    root.mainloop()