import os
import random
import string
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def open_image():
    global current_image
    file_path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[("Изображения", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    
    if not file_path:
        return
    
    try:
        current_image = Image.open(file_path)
        max_size = (400, 400)
        preview_image = current_image.copy()
        preview_image.thumbnail(max_size, Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(preview_image)
        
        image_label.config(image=tk_image)
        image_label.image = tk_image
        status_label.config(text=f"Загружено: {os.path.basename(file_path)}")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось открыть изображение:\n{str(e)}")

def generate_gif():
    try:
        text = text_entry.get()
        if not text:
            messagebox.showwarning("Ошибка", "Введите текст!")
            return
            
        try:
            font_size = int(size_entry.get())
        except ValueError:
            messagebox.showwarning("Ошибка", "Размер шрифта должен быть числом!")
            return
            
        if current_image is None:
            messagebox.showwarning("Ошибка", "Сначала выберите изображение!")
            return
            
        random_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        output_file = f"{random_name}.gif"
        
        temp_file = "temp_image.gif"
        current_image.save(temp_file)
        
        cmd = (
            f'ffmpeg -i {temp_file} -vf "'
            f"drawtext=text='{text}':fontfile='C\:/Windows/Fonts/impact.ttf':"
            f"fontsize={font_size}:fontcolor=white:bordercolor=black:borderw=1:"
            f'x=(w-text_w)/2:y=h-th-10" -r 15 {output_file}'
        )
        
        os.system(cmd)
        os.remove(temp_file)
        messagebox.showinfo("Успех", f"Гифка сохранена как {output_file}")
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при создании гифки:\n{str(e)}")

def on_closing():
    dialog = tk.Toplevel(root)
    dialog.title("Подтверждение выхода")
    dialog.geometry("450x200+500+400")
    dialog.resizable(False, False)
    dialog.transient(root)
    dialog.iconbitmap("src/icon.ico")
    dialog.grab_set()
    
    try:
        warning_img = Image.open("src/warning.png")
        warning_img = warning_img.resize((128, 128), Image.LANCZOS)
        tk_warning_img = ImageTk.PhotoImage(warning_img)
        img_label = tk.Label(dialog, image=tk_warning_img)
        img_label.image = tk_warning_img
        img_label.place(x=20, y=20)
    except:
        pass
    
    message = tk.Label(dialog, 
                      text="Вы действительно хотите выйти?",
                      font=("Arial", 11),
                      justify="left")
    message.place(x=150, y=30)
    
    btn_frame = tk.Frame(dialog)
    btn_frame.place(x=150, y=120)
    
    yes_btn = tk.Button(btn_frame, 
                       text="Да", 
                       width=10, 
                       command=root.destroy)
    yes_btn.pack(side="left", padx=10)
    
    no_btn = tk.Button(btn_frame, 
                      text="Нет", 
                      width=10, 
                      command=dialog.destroy)
    no_btn.pack(side="left")
    
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    dialog.wait_window()

root = tk.Tk()
root.title("Импактор мини")
try:
    root.iconbitmap("src/icon.ico")
except:
    pass 
root.geometry("800x500+400+200")
root.protocol("WM_DELETE_WINDOW", on_closing)

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

left_frame = tk.Frame(main_frame, bd=2, relief="sunken")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

image_label = tk.Label(left_frame, bg="white")
image_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

control_frame = tk.LabelFrame(right_frame, text="Параметры", padx=10, pady=10)
control_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(control_frame, text="Текст для наложения:").grid(row=0, column=0, sticky="w", pady=2)
text_entry = tk.Entry(control_frame, width=30)
text_entry.grid(row=0, column=1, sticky="we", padx=5, pady=2)

tk.Label(control_frame, text="Размер шрифта:").grid(row=1, column=0, sticky="w", pady=2)
size_entry = tk.Spinbox(control_frame, from_=10, to=100, width=5)
size_entry.grid(row=1, column=1, sticky="w", padx=5, pady=2)
size_entry.delete(0, "end")
size_entry.insert(0, "48")

select_button = tk.Button(
    right_frame,
    text="Выбрать изображение",
    command=open_image,
    font=("Arial", 12),
    padx=10,
    pady=5
)
select_button.pack(pady=(10, 5), fill=tk.X)

generate_button = tk.Button(
    right_frame,
    text="сделать гифку",
    command=generate_gif,
    font=("Arial", 12, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=8
)
generate_button.pack(pady=10, fill=tk.X)

status_frame = tk.Frame(root, bd=1, relief="sunken")
status_frame.pack(side=tk.BOTTOM, fill=tk.X)

current_image = None
root.mainloop()