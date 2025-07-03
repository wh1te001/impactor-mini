import os
import random
import string
import tkinter as tk 
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  

def open_image():
    file_path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    
    if not file_path:
        return
    
    try:
        image = Image.open(file_path)
        max_size = (800, 600)
        image.thumbnail(max_size, Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(image)
        
        image_label.config(image=tk_image)
        image_label.image = tk_image 
        
        status_label.config(text=f"Загружено: {os.path.basename(file_path)}")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть изображение:\n{str(e)}")

root = tk.Tk()  
root.title("импактор мини")
try:
    root.iconbitmap("src/icon.ico")  
except:
    pass 
root.geometry("600x400+400+200")

select_button = tk.Button(
    root,
    text="Выбрать изображение",
    command=open_image,
    font=("Arial", 14),
    padx=10,
    pady=5
)
select_button.pack(pady=20)

image_label = tk.Label(root)
image_label.pack(pady=10, fill="both", expand=True)

status_label = tk.Label(root, text="Выберите изображение", bd=1, relief="sunken", anchor="w")
status_label.pack(side="bottom", fill="x")

root.mainloop()



# def generate_string(length):
#     all_symbols = string.ascii_uppercase + string.digits
#     result = ''.join(random.choice(all_symbols) for _ in range(length))
#     return result


# image = str(input("Введите название файла"))
# text = str(input("Введите текст"))
# size = str(input("Введите размер шрифта"))
# random_name = generate_string(6)

# os.system(f"ffmpeg -i {image} -vf \"drawtext=text='{text}':fontfile='C\:/Windows/Fonts/impact.ttf':fontsize={size}:fontcolor=white:bordercolor=black:borderw=1:x=(w-text_w)/2:y=h-th-10\" -r 15 {random_name}.gif")
# os.system(f"ffmpeg -i {image} -vf \"drawtext=text='{text}':fontfile='C\:/Windows/Fonts/impact.ttf':fontsize={size}:fontcolor=white:bordercolor=black:borderw=1:x=(w-text_w)/2:y=h-th-10\" -r 15 {random_name}.gif")