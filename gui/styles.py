# gui/styles.py
import tkinter.ttk as ttk

def configure_styles():
    # Use the "clam" theme for a modern look
    style = ttk.Style()
    style.theme_use("clam")

    # Configure button style
    style.configure("TButton", font=("Segoe UI", 12), padding=10, background="#4CAF50", foreground="white", borderwidth=0)
    style.map("TButton", background=[("active", "#45a049")])  # Change color when button is pressed

    # Configure label style
    style.configure("TLabel", font=("Segoe UI", 12), background="#f5f5f5", foreground="#333333")

    # Configure combobox style
    style.configure("TCombobox", font=("Segoe UI", 11), padding=5)

    # Configure radiobutton style
    style.configure("TRadiobutton", font=("Segoe UI", 11), background="#f5f5f5", foreground="#333333")

    # Configure frame style
    style.configure("TFrame", background="#f5f5f5")