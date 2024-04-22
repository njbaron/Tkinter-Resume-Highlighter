import tkinter as tk
from tkinter import ttk
import json
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit["state"] = "normal"
        txt_edit.insert(tk.END, text)
        enable_text_edit()
    window.title(f"Resume Element Selector - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Json Files", "*.json"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = result_text.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Resume Element Selector - {filepath}")

def process_radio():
    try:
        selected_text = txt_edit.selection_get()
    except tk.TclError:
        selected_text = ""

    current_radio_selected = selected_radio.get()
    if selected_text:
        text_fields[current_radio_selected].delete("1.0","end")
        text_fields[current_radio_selected].insert(tk.END, selected_text)
        txt_edit.tag_remove(tk.SEL, "1.0", tk.END)

def parse_to_json(*args, **kwargs):
    text_dict = {}
    for name, text in text_fields.items():
        new_name = name.lower().replace(" ", "_")
        text_dict[new_name] = text.get("1.0", tk.END).strip()
    result_text["state"] = "normal"
    result_text.delete("1.0", "end")
    result_text.insert(tk.END, json.dumps(text_dict, indent=4))
    result_text["state"] = "disabled"

def cycle_radio(event):
    if enable_editing.get():
        return
    
    process_radio()

    print(event)
    current_selection = selected_radio.get()
    index = button_names.index(current_selection) + 1
    selected_radio.set(button_names[index % len(button_names)])

def check_highlight(event):
    if enable_editing.get():
        return

    try:
        txt_edit.tag_add("sel", "sel.first wordstart", "sel.last wordend")
    except tk.TclError:
        return

def enable_text_edit():
    print(enable_editing.get())
    if enable_editing.get():
        txt_edit["state"] = "normal"
    else:
        txt_edit["state"] = "disabled"


window = tk.Tk()
window.title("Resume Element Selector")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=2)
window.columnconfigure(2, minsize=400, weight=1)

#### Right Column ####
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)


selected_radio = tk.StringVar()

button_names = ["name", "address", "email", "job", "start date", "end date"]

# label
label = ttk.Label(frm_buttons, text="What are you selecting?")
label.grid(row=3, column=0, sticky="ew", padx=5, pady=5)

# radio buttons
radio_buttons: dict[str, tk.Radiobutton] = {}
for index, name in enumerate(button_names):
    r = tk.Radiobutton(
        frm_buttons,
        text=name,
        value=name,
        variable=selected_radio,
        indicator = 0
    )
    r.grid(row=4+index, column=0, sticky="ew", padx=5)
    radio_buttons[name] = r
selected_radio.set(button_names[0])

btn_select = tk.Button(frm_buttons, text="Select", command=process_radio)
btn_select.grid(row=index+5, column=0, sticky="ew", padx=5, pady=5)

#### Center Column ####
txt_edit_frame = tk.Frame(window)
txt_edit = tk.Text(txt_edit_frame)
txt_edit["state"] = "disabled"
txt_edit.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

enable_editing = tk.BooleanVar(value=False)
txt_edit_enable_box = tk.Checkbutton(txt_edit_frame, text="Enable Editing", variable=enable_editing, onvalue=True, offvalue=False, command=enable_text_edit)
txt_edit_enable_box.pack()

#### Right Column ####
frm_items = tk.Frame(window, relief=tk.RAISED, bd=2)

text_fields: dict[str, tk.Text] = {}

for index, name in enumerate(button_names):
    label_thing = tk.Label(frm_items, text=name)
    label_thing.grid(row=index, column=0, sticky="ew")
    text_field = tk.Text(frm_items, height=2)
    text_field.grid(row=index, column=1, sticky="ew")
    text_fields[name] = text_field

btn_parse = tk.Button(frm_items, text="Parse", command=parse_to_json)
btn_parse.grid(row=index+1, column=0, sticky="n", columnspan=2)

result_label = ttk.Label(frm_items, text="Current Result")
result_label.grid(row=index+2, column=0, sticky="w", columnspan=2)

result_text = tk.Text(frm_items)
result_text["state"] = "disabled"
result_text.grid(row=index+3, column=0, sticky="nsew", columnspan=2)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit_frame.grid(row=0, column=1, sticky="nswe")
frm_items.grid(row=0, column=2, sticky="ns")

txt_edit.bind('<space>', cycle_radio)
txt_edit.bind('<Return>', parse_to_json)
txt_edit.bind('<ButtonRelease>', check_highlight)

window.mainloop()