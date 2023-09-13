import sys
import os
import tksvg
import tkinter as tk
from tkinter import ttk
from main import start_bot
from threading import Thread
import json
from main import stop_bot


# ---------------- Exact Paths Solution ----------------

# Exact Paths for .tcl references, needed if you want 'One File' instead of 'One Directory' for auto-py-to-exe (PyInstaller) .exe standalone.
# resource_path function gets the absolute path to a resource in a PyInstaller-packaged application. 
# If application is a standalone .exe, sys._MEIPASS provides path to temp folder PyInstaller unpacks the resources into.
# If application is not packaged, just returns the original path.

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Gets paths for sun-valley.tcl, dark.tcl, and light.tcl. Stores them so sun-valley.tcl can access its source properly.
sun_valley_path = resource_path("sun-valley.tcl")
dark_tcl_path = resource_path("theme/dark.tcl").replace("\\", "/") # Convert to Unix-style path for TCL
light_tcl_path = resource_path("theme/light.tcl").replace("\\", "/") # Convert to Unix-style path for TCL
os.environ['DARK_TCL_PATH'] = dark_tcl_path
os.environ['LIGHT_TCL_PATH'] = light_tcl_path

with open("configs.json", "r") as f:
    config_data = json.load(f)

class Window(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.grid(sticky="nsew")

        self.env_entry_vars = []

        self.labels = ["Telegram Token:", "Telegram Chat ID:", "ETH Address:", "ETH Private Key:", "Stark Key Testnet:", "DYDX Key Testnet:", "DYDX Secret Testnet:", "DYDX Passphrase Testnet:", "HTTP Provider Testnet:", "Stark Key Mainnet:", "DYDX Key Mainnet:", "DYDX Secret Mainnet:", "DYDX Passphrase Mainnet:", "HTTP Provider Mainnet:"]

        self.env_labels = ["TELEGRAM_TOKEN", "TELEGRAM_CHAT_ID", "ETHEREUM_ADDRESS", "ETH_PRIVATE_KEY", "STARK_PRIVATE_KEY_TESTNET", "DYDX_API_KEY_TESTNET", "DYDX_API_SECRET_TESTNET", "DYDX_API_PASSPHRASE_TESTNET", "HTTP_PROVIDER_TESTNET", "STARK_PRIVATE_KEY_MAINNET", "DYDX_API_KEY_MAINNET", "DYDX_API_SECRET_MAINNET", "DYDX_API_PASSPHRASE_MAINNET", "HTTP_PROVIDER_MAINNET"]

        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1) 
        self.columnconfigure(index=2, weight=1) 
        self.rowconfigure(index=0, weight=1) 

        self.setup_left_frame()
        self.setup_middle_frame()
        self.setup_right_frame()

# ---------------- Frames ----------------
    def setup_left_frame(self):

        ### LEFT FRAME ###
        left_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        left_frame.grid(row=0, column=0, padx=20)
        left_frame.columnconfigure(index=0, weight=1)
        left_frame.rowconfigure(index=0, weight=0)
        left_frame.rowconfigure(index=1, weight=0)

        ### PERSONAL INFO FRAME ###
        info_frame = ttk.LabelFrame(left_frame, text="Personal Information", labelanchor="n")
        info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        info_frame.columnconfigure(1, weight=1)

        ### Labels, Entries, & Button ###
        for i, label in enumerate(self.labels):
            special_pady_indices = [2, 4, 9]
            pady_value = (15,5) if i in special_pady_indices else 5
            
            ttk.Label(info_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=pady_value)
            text_var = tk.StringVar()
            self.env_entry_vars.append(text_var)
            ttk.Entry(info_frame, textvariable=text_var, width=45).grid(row=i, column=1, sticky="ew", padx=10, pady=pady_value)

        save_info_button = ttk.Button(info_frame, text="Save Information", width=15, style="Accent.TButton", command=self.save_persoanl_info)
        save_info_button.grid(row=14, column=0, columnspan=2, sticky="ew", padx=10, pady=5)


    def setup_middle_frame(self):

        ### MIDDLE FRAME ###
        middle_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        middle_frame.grid(row=0, column=1, padx=20)
        middle_frame.columnconfigure(index=0, weight=1)
        middle_frame.rowconfigure(index=0, weight=0)
        middle_frame.rowconfigure(index=1, weight=0)

        ### ENTRY FRAME ###
        entry_frame = ttk.LabelFrame(middle_frame, text="Entry", labelanchor="n")
        entry_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        entry_frame.columnconfigure(1, weight=1)

        ttk.Label(entry_frame, text="Indicator").grid(row=0, column=0, padx=5, pady=(10,0))
        ttk.Label(entry_frame, text="Use").grid(row=0, column=1, padx=5, pady=(10,0))
        ttk.Label(entry_frame, text="Value").grid(row=0, column=2, padx=5, pady=(10,0))
        ttk.Label(entry_frame, text="Above").grid(row=0, column=3, padx=5, pady=(10,0))
        ttk.Label(entry_frame, text="Below").grid(row=0, column=4, padx=5, pady=(10,0))

        # EMA - ENTRY
        ttk.Label(entry_frame, text="EMA").grid(row=1, column=0, padx=5)

        self.entry_ema_use_var = tk.BooleanVar()
        self.entry_ema_use_var.set(config_data["ENTRY_EMA_USE"])
        toggle_entry_ema_use = ttk.Checkbutton(entry_frame, variable=self.entry_ema_use_var, command=self.toggle_entry_ema_use)
        toggle_entry_ema_use.grid(row=1, column=1, padx=10, pady=10)

        self.entry_ema_value_var = tk.StringVar()
        self.entry_ema_value_var.set(config_data["ENTRY_EMA_VALUE"])
        self.entry_ema_value_var.trace("w", self.update_entry_ema_value)
        entry_ema_value = ttk.Spinbox(entry_frame, width=8, from_=5, to=300, increment=1, textvariable=self.entry_ema_value_var)
        entry_ema_value.grid(row=1, column=2, padx=10, pady=10)

        self.entry_ema_above_var = tk.BooleanVar()
        self.entry_ema_above_var.set(config_data["ENTRY_EMA_ABOVE"])
        above_entry_ema_radio = ttk.Radiobutton(entry_frame, variable=self.entry_ema_above_var, value=True, command=self.toggle_entry_ema_above)
        above_entry_ema_radio.grid(row=1, column=3)
        below_entry_ema_radio = ttk.Radiobutton(entry_frame, variable=self.entry_ema_above_var, value=False, command=self.toggle_entry_ema_above)
        below_entry_ema_radio.grid(row=1, column=4)

        # RSI - ENTRY
        ttk.Label(entry_frame, text="RSI").grid(row=2, column=0, padx=5)

        self.entry_rsi_use_var = tk.BooleanVar()
        self.entry_rsi_use_var.set(config_data["ENTRY_RSI_USE"])
        toggle_entry_rsi_use = ttk.Checkbutton(entry_frame, variable=self.entry_rsi_use_var, command=self.toggle_entry_rsi_use)
        toggle_entry_rsi_use.grid(row=2, column=1, padx=10, pady=10)

        self.entry_rsi_value_var = tk.StringVar()
        self.entry_rsi_value_var.set(config_data["ENTRY_RSI_VALUE"])
        self.entry_rsi_value_var.trace("w", self.update_entry_rsi_value)
        entry_rsi_value = ttk.Spinbox(entry_frame, width=8, from_=5, to=300, increment=1, textvariable=self.entry_rsi_value_var)
        entry_rsi_value.grid(row=2, column=2, padx=10, pady=10)

        self.entry_rsi_above_var = tk.BooleanVar()
        self.entry_rsi_above_var.set(config_data["ENTRY_RSI_ABOVE"])
        above_entry_rsi_radio = ttk.Radiobutton(entry_frame, variable=self.entry_rsi_above_var, value=True, command=self.toggle_entry_rsi_above)
        above_entry_rsi_radio.grid(row=2, column=3)
        below_entry_rsi_radio = ttk.Radiobutton(entry_frame, variable=self.entry_rsi_above_var, value=False, command=self.toggle_entry_rsi_above)
        below_entry_rsi_radio.grid(row=2, column=4)

        # Position - ENTRY
        ttk.Label(entry_frame, text="Position Size USD").grid(row=3, column=0, sticky='w', padx=(10,0))
        self.position_var = tk.StringVar()
        self.position_var.set(config_data["POSITION_SIZE_USD"])
        self.position_var.trace("w", self.update_position_size)
        self.position_usd_entry = ttk.Spinbox(entry_frame, width=12, from_=30, to=100000, increment=10, textvariable=self.position_var)
        self.position_usd_entry.grid(row=3, column=1, padx=10, pady=10)

        # Time Frame - ENTRY
        ttk.Label(entry_frame, text="Time Frame").grid(row=4, column=0, padx=(10,0), pady=5)
        self.time_frame_var = tk.StringVar()
        self.time_frame_var.set(config_data["RESOLUTION_STR"])
        self.time_frame_var.trace('w', self.update_time_frame)
        self.time_frame = ttk.Combobox(entry_frame, width=12, state="readonly", values=["5MINS", "15MINS", "30MINS", "1HOUR", "4HOURS", "1DAY"], textvariable=self.time_frame_var)
        self.time_frame.grid(row=4, column=1, pady=10)

        # Side - ENTRY
        self.side_var = tk.StringVar()
        self.side_var.set(config_data["SIDE"])
        buy_side_radio = ttk.Radiobutton(entry_frame, text="Long", variable=self.side_var, value="BUY", command=self.toggle_side)
        buy_side_radio.grid(row=3, rowspan=2, column=2)
        sell_side_radio = ttk.Radiobutton(entry_frame, text="Short", variable=self.side_var, value="SELL", command=self.toggle_side)
        sell_side_radio.grid(row=3, rowspan=2, column=3)


        ### EXIT FRAME ###
        exit_frame = ttk.LabelFrame(middle_frame, text="Exit", labelanchor="n")
        exit_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        exit_frame.columnconfigure(1, weight=1)

        ### TAKE PROFIT FRAME ###
        tp_frame = ttk.LabelFrame(exit_frame, text="Take Profit", labelanchor="n")
        tp_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        tp_frame.columnconfigure(1, weight=1)

        ttk.Label(tp_frame, text="Indicator").grid(row=0, column=0, padx=5, pady=(10,0))
        ttk.Label(tp_frame, text="Use").grid(row=0, column=1, padx=5, pady=(10,0))
        ttk.Label(tp_frame, text="Value").grid(row=0, column=2, padx=5, pady=(10,0))

        # EMA - TP
        ttk.Label(tp_frame, text="EMA").grid(row=1, column=0, padx=5)

        self.tp_ema_use_var = tk.BooleanVar()
        self.tp_ema_use_var.set(config_data["TP_EMA_USE"])
        toggle_tp_ema_use = ttk.Checkbutton(tp_frame, variable=self.tp_ema_use_var, command=self.toggle_tp_ema_use)
        toggle_tp_ema_use.grid(row=1, column=1, padx=10, pady=5)

        self.tp_ema_value_var = tk.StringVar()
        self.tp_ema_value_var.set(config_data["TP_EMA_VALUE"])
        self.tp_ema_value_var.trace("w", self.update_tp_ema_value)
        tp_ema_value = ttk.Spinbox(tp_frame, width=8, from_=5, to=300, increment=1, textvariable=self.tp_ema_value_var)
        tp_ema_value.grid(row=1, column=2, padx=10, pady=5)

        # RSI - TP
        ttk.Label(tp_frame, text="RSI").grid(row=2, column=0, padx=5)

        self.tp_rsi_use_var = tk.BooleanVar()
        self.tp_rsi_use_var.set(config_data["TP_RSI_USE"])
        toggle_tp_rsi_use = ttk.Checkbutton(tp_frame, variable=self.tp_rsi_use_var, command=self.toggle_tp_rsi_use)
        toggle_tp_rsi_use.grid(row=2, column=1, padx=10, pady=5)

        self.tp_rsi_value_var = tk.StringVar()
        self.tp_rsi_value_var.set(config_data["TP_RSI_VALUE"])
        self.tp_rsi_value_var.trace("w", self.update_tp_rsi_value)
        tp_rsi_value = ttk.Spinbox(tp_frame, width=8, from_=0, to=100, increment=1, textvariable=self.tp_rsi_value_var)
        tp_rsi_value.grid(row=2, column=2, padx=10, pady=5)

        # ATR - TP
        ttk.Label(tp_frame, text="ATR").grid(row=3, column=0, padx=5)

        self.tp_atr_use_var = tk.BooleanVar()
        self.tp_atr_use_var.set(config_data["TP_ATR_USE"])
        toggle_tp_atr_use = ttk.Checkbutton(tp_frame, variable=self.tp_atr_use_var, command=self.toggle_tp_atr_use)
        toggle_tp_atr_use.grid(row=3, column=1, padx=10, pady=5)

        self.tp_atr_value_var = tk.StringVar()
        self.tp_atr_value_var.set(config_data["TP_ATR_VALUE"])
        self.tp_atr_value_var.trace("w", self.update_tp_atr_value)
        tp_atr_value = ttk.Spinbox(tp_frame, width=8, from_=1, to=10, increment=0.1, textvariable=self.tp_atr_value_var)
        tp_atr_value.grid(row=3, column=2, padx=10, pady=5)

        # Pct Gain - TP
        ttk.Label(tp_frame, text="Percent Gain").grid(row=4, column=0, padx=5)

        self.pct_gain_use_var = tk.BooleanVar()
        self.pct_gain_use_var.set(config_data["PCT_GAIN_USE"])
        toggle_pct_gain_use = ttk.Checkbutton(tp_frame, variable=self.pct_gain_use_var, command=self.toggle_pct_gain_use)
        toggle_pct_gain_use.grid(row=4, column=1, padx=10, pady=5)

        self.pct_gain_value_var = tk.StringVar()
        self.pct_gain_value_var.set(config_data["PCT_GAIN_VALUE"])
        self.pct_gain_value_var.trace("w", self.update_pct_gain_value)
        pct_gain_value = ttk.Spinbox(tp_frame, width=8, from_=1.001, to=2.000, increment=0.001, textvariable=self.pct_gain_value_var)
        pct_gain_value.grid(row=4, column=2, padx=10, pady=10)


        ### STOP LOSS FRAME ###
        sl_frame = ttk.LabelFrame(exit_frame, text="Stop Loss", labelanchor="n")
        sl_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        sl_frame.columnconfigure(1, weight=1)

        ttk.Label(sl_frame, text="Indicator").grid(row=0, column=0, padx=5, pady=(10,0))
        ttk.Label(sl_frame, text="Use").grid(row=0, column=1, padx=5, pady=(10,0))
        ttk.Label(sl_frame, text="Value").grid(row=0, column=2, padx=5, pady=(10,0))
   
        # EMA - SL
        ttk.Label(sl_frame, text="EMA").grid(row=1, column=0, padx=5)

        self.sl_ema_use_var = tk.BooleanVar()
        self.sl_ema_use_var.set(config_data["SL_EMA_USE"])
        toggle_sl_ema_use = ttk.Checkbutton(sl_frame, variable=self.sl_ema_use_var, command=self.toggle_sl_ema_use)
        toggle_sl_ema_use.grid(row=1, column=1, padx=10, pady=10)

        self.sl_ema_value_var = tk.StringVar()
        self.sl_ema_value_var.set(config_data["SL_EMA_VALUE"])
        self.sl_ema_value_var.trace("w", self.update_sl_ema_value)
        sl_ema_value = ttk.Spinbox(sl_frame, width=8, from_=5, to=300, increment=1, textvariable=self.sl_ema_value_var)
        sl_ema_value.grid(row=1, column=2, padx=10, pady=10)

        # RSI - SL
        ttk.Label(sl_frame, text="RSI").grid(row=2, column=0, padx=5)

        self.sl_rsi_use_var = tk.BooleanVar()
        self.sl_rsi_use_var.set(config_data["SL_RSI_USE"])
        toggle_sl_rsi_use = ttk.Checkbutton(sl_frame, variable=self.sl_rsi_use_var, command=self.toggle_sl_rsi_use)
        toggle_sl_rsi_use.grid(row=2, column=1, padx=10, pady=10)

        self.sl_rsi_value_var = tk.StringVar()
        self.sl_rsi_value_var.set(config_data["SL_RSI_VALUE"])
        self.sl_rsi_value_var.trace("w", self.update_sl_rsi_value)
        sl_rsi_value = ttk.Spinbox(sl_frame, width=8, from_=0, to=100, increment=1, textvariable=self.sl_rsi_value_var)
        sl_rsi_value.grid(row=2, column=2, padx=10, pady=10)

        # ATR - SL
        ttk.Label(sl_frame, text="ATR").grid(row=3, column=0, padx=5)

        self.sl_atr_use_var = tk.BooleanVar()
        self.sl_atr_use_var.set(config_data["SL_ATR_USE"])
        toggle_sl_atr_use = ttk.Checkbutton(sl_frame, variable=self.sl_atr_use_var, command=self.toggle_sl_atr_use)
        toggle_sl_atr_use.grid(row=3, column=1, padx=10, pady=5)

        self.sl_atr_value_var = tk.StringVar()
        self.sl_atr_value_var.set(config_data["SL_ATR_VALUE"])
        self.sl_atr_value_var.trace("w", self.update_sl_atr_value)
        sl_atr_value = ttk.Spinbox(sl_frame, width=8, from_=1, to=10, increment=0.1, textvariable=self.sl_atr_value_var)
        sl_atr_value.grid(row=3, column=2, padx=10, pady=5)

        # Pct Gain - SL
        ttk.Label(sl_frame, text="Percent Loss").grid(row=4, column=0, padx=5)

        self.pct_loss_use_var = tk.BooleanVar()
        self.pct_loss_use_var.set(config_data["PCT_LOSS_USE"])
        toggle_pct_loss_use = ttk.Checkbutton(sl_frame, variable=self.pct_loss_use_var, command=self.toggle_pct_loss_use)
        toggle_pct_loss_use.grid(row=4, column=1, padx=10, pady=5)

        self.pct_loss_value_var = tk.StringVar()
        self.pct_loss_value_var.set(config_data["PCT_LOSS_VALUE"])
        self.pct_loss_value_var.trace("w", self.update_pct_loss_value)
        pct_loss_value = ttk.Spinbox(sl_frame, width=8, from_=0.01, to=0.999, increment=0.001, textvariable=self.pct_loss_value_var)
        pct_loss_value.grid(row=4, column=2, padx=10, pady=10)


    def setup_right_frame(self):

        ### RIGHT FRAME ###
        right_frame = ttk.Frame(self, borderwidth=2, relief="solid")
        right_frame.grid(row=0, column=2, padx=(0,20))
        right_frame.columnconfigure(index=0, weight=1)
        right_frame.rowconfigure(index=0, weight=1)
        right_frame.rowconfigure(index=1, weight=1)

        ### CONTROL PANEL FRAME ###
        control_frame = ttk.LabelFrame(right_frame, text="Control Panel", labelanchor="n")
        control_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        control_frame.columnconfigure(1, weight=1)

        ### Start and Stop Buttons ###
        self.start_button = ttk.Button(control_frame, text="Start", width=12, style="Accent.TButton", command=self.start_bot_thread)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(control_frame, text="Stop", width=12, style="Accent.TButton", command=self.stop_bot_thread)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        ### Settings ###
        self.mode_var = tk.StringVar()
        self.mode_var.set(config_data["MODE"])
        testnet_radio = ttk.Radiobutton(control_frame, text="Testnet", variable=self.mode_var, value="DEVELOPMENT", command=self.toggle_mode)
        testnet_radio.grid(row=1, column=0)
        mainnet_radio = ttk.Radiobutton(control_frame, text="Mainnet", variable=self.mode_var, value="PRODUCTION", command=self.toggle_mode)
        mainnet_radio.grid(row=1, column=1)

        self.entry_var = tk.BooleanVar()
        self.entry_var.set(config_data["ENTER_TRADES"])
        entry_toggle = ttk.Checkbutton(control_frame, text="Enter Trades", variable=self.entry_var, command=self.toggle_enter_trades)
        entry_toggle.grid(row=2, column=0, columnspan=2, padx=10, pady=(10,5), sticky='w')

        self.exit_var = tk.BooleanVar()
        self.exit_var.set(config_data["EXIT_TRADES"])
        exit_toggle = ttk.Checkbutton(control_frame, text="Exit Trades", variable=self.exit_var, command=self.toggle_exit_trades)
        exit_toggle.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky='w')

        self.theme_var = tk.BooleanVar()
        self.theme_var.set(True)
        theme_toggle = ttk.Checkbutton(control_frame, text="Dark Mode", style="Switch.TCheckbutton", variable=self.theme_var, command=self.toggle_theme)
        theme_toggle.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


# ---------------- Functionality ----------------

    ### LEFT FRAME FUNCTIONS ###

    # Saves users personal information entered to .env file. LEFT FRAME.
    def save_persoanl_info(self):
        self.lines = [1, 2, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20]  
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        env_path = os.path.join(project_root, '.env')

        with open(env_path, 'r') as f:
            lines = f.readlines()

        for line_num, (text_var, env_label) in zip(self.lines, zip(self.env_entry_vars, self.env_labels)):
            if not text_var.get().strip():
                continue # Skip if the entry is blank
            parts = lines[line_num].split('=')
            if len(parts) >= 2:  # Make sure there is an "=" to split on
                lines[line_num] = f"{parts[0]}= \"{text_var.get()}\"\n"

        with open(env_path, 'w') as f:
            f.writelines(lines)


    ### RIGHT FRAME FUNCTIONS ###

    def start_bot_thread(self):
        self.bot_thread = Thread(target=start_bot)
        self.bot_thread.start()

    def stop_bot_thread(self):
        stop_bot()

    def toggle_enter_trades(self):
        current = self.entry_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTER_TRADES'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_exit_trades(self):
        current = self.exit_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['EXIT_TRADES'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_theme(self):
        if self.theme_var.get():
            self.master.tk.call("set_theme", "dark")
        else:
            self.master.tk.call("set_theme", "light")

    def toggle_mode(self):
        current = self.mode_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['MODE'] = current 
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)


    ### MIDDLE FRAME FUNCTIONS ###

    # Entry Functions
    def toggle_side(self):
        current = self.side_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SIDE'] = current 
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_position_size(self, *args):
        current = self.position_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['POSITION_SIZE_USD'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_time_frame(self, *args):
        current = self.time_frame_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['RESOLUTION_STR'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)            

    def toggle_entry_ema_use(self):
        current = self.entry_ema_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTRY_EMA_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_entry_rsi_use(self):
        current = self.entry_rsi_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTRY_RSI_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_entry_ema_value(self, *args):
        current = self.entry_ema_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTRY_EMA_VALUE'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_entry_rsi_value(self, *args):
        current = self.entry_rsi_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTRY_RSI_VALUE'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_entry_ema_above(self):
        current = self.entry_ema_above_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTRY_EMA_ABOVE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_entry_rsi_above(self):
        current = self.entry_rsi_above_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['ENTRY_RSI_ABOVE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)


    # Exit TP Functions
    def toggle_tp_ema_use(self):
        current = self.tp_ema_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['TP_EMA_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_tp_ema_value(self, *args):
        current = self.tp_ema_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['TP_EMA_VALUE'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_tp_rsi_use(self):
        current = self.tp_rsi_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['TP_RSI_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_tp_rsi_value(self, *args):
        current = self.tp_rsi_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['TP_RSI_VALUE'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_tp_atr_use(self):
        current = self.tp_atr_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['TP_ATR_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_tp_atr_value(self, *args):
        current = self.tp_atr_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['TP_ATR_VALUE'] = float(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)
    
    def toggle_pct_gain_use(self):
        current = self.pct_gain_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['PCT_GAIN_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)
    
    def update_pct_gain_value(self, *args):
        current = self.pct_gain_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['PCT_GAIN_VALUE'] = float(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    # Exit SL Functions
    def toggle_sl_ema_use(self):
        current = self.sl_ema_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SL_EMA_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_sl_ema_value(self, *args):
        current = self.sl_ema_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SL_EMA_VALUE'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_sl_rsi_use(self):
        current = self.sl_rsi_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SL_RSI_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_sl_rsi_value(self, *args):
        current = self.sl_rsi_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SL_RSI_VALUE'] = int(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def toggle_sl_atr_use(self):
        current = self.sl_atr_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SL_ATR_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)

    def update_sl_atr_value(self, *args):
        current = self.sl_atr_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['SL_ATR_VALUE'] = float(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)
    
    def toggle_pct_loss_use(self):
        current = self.pct_loss_use_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['PCT_LOSS_USE'] = current
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)
    
    def update_pct_loss_value(self, *args):
        current = self.pct_loss_value_var.get()
        with open('configs.json', 'r') as f:
            config_data = json.load(f)
        config_data['PCT_LOSS_VALUE'] = float(current)
        with open('configs.json', 'w') as f:
            json.dump(config_data, f, indent=4)


# ---------------- Launch Window ----------------
if __name__ == "__main__":

    root = tk.Tk()
    root.title("DYDX Bot Interface")

    tksvg.load(root)
    sun_valley_path = resource_path("sun-valley.tcl")
    root.tk.call("source", sun_valley_path)
    root.tk.call("set_theme", "dark")

    app = Window(root)
    app.pack(fill=tk.BOTH, expand=True)
    root.update()
    root.minsize(1600,900)
    root.geometry("1600x900")
    root.mainloop()
