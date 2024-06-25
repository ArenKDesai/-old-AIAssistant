import tkinter as tk
from PIL import Image, ImageTk

def show_image_in_bottom_right(image_path, max_width=300, max_height=300):
    # Create the main window
    root = tk.Tk()
    
    # Hide the root window initially
    root.withdraw()

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Load the image
    image = Image.open(image_path).convert("RGBA")  # Ensure the image is in RGBA mode
    
    # Resize the image if max_width or max_height is specified
    if max_width or max_height:
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        
        if max_width and original_width > max_width:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_width = original_width
            new_height = original_height
        
        if max_height and new_height > max_height:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    photo = ImageTk.PhotoImage(image)

    # Create a new window to display the image
    window = tk.Toplevel(root)
    window.overrideredirect(1)  # Remove window borders
    window.geometry(f"{photo.width()}x{photo.height()}+{screen_width - photo.width()}+{screen_height - photo.height()}")
    window.attributes('-topmost', True)  # Keep the window on top
    window.wm_attributes('-transparentcolor', 'white')  # Set the transparency color to 'white' (or any other color if needed)
    window.attributes('-alpha', 0.0)  # Set full transparency of the window

    # Add the image to a label and pack it into the window
    label = tk.Label(window, image=photo, bg='white')
    label.pack()

    # Update the window to appear in the bottom right corner
    window.update()
    
    # Set the window's alpha to 1 (fully opaque) after updating the window's geometry
    window.attributes('-alpha', 1.0)

    # Keep the window open
    root.mainloop()