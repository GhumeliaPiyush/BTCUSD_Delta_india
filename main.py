import threading
import time
import requests
import pandas as pd
import numpy as np
import talib
from tkinter import messagebox
import customtkinter as ctk
import tkinter as ttk
from tkinter import *
from plyer import notification
from datetime import datetime, timedelta,timezone

# Replace with your Binance API URL and parameters for 5-minute candles
URL = "https://cdn.india.deltaex.org/v2/history/candles"

class TradingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Signal Generator")
        self.geometry("350x200")
        self.resizable(0,0)
        self.is_trading_active = False
        self.start_btn = ctk.CTkButton(self,text="Start",font=("Cambria",16),command=lambda:self.start_trading())
        self.start_btn.grid(row=0,column=0,pady=5)
        self.stop_btn = ctk.CTkButton(self,text="Stop",font=("Cambria",16),command=lambda:self.stop_trading())
        self.stop_btn.grid(row=0,column=1,pady=5)
        self.time_lable= ctk.CTkLabel(self,text="SELECT TIME FRAME:",font=("Cambria",16,"bold"))
        self.time_lable.grid(row=1,column=0,padx=5,pady=5)
        self.current_span = "5m"
        span_var = ctk.StringVar(value="5m")
        span_menu = ctk.CTkComboBox(self, variable =span_var, values=["5m", "15m", "30m", "1h", "4h", "1D", "1W"], command=lambda s: self.change_span(s))
        span_menu.grid(row=1,column=1,padx=5,pady=5)


    def notify(self, message):
        """Send a notification to the phone."""
        notification.notify(
            title="Trading Signal",
            message=message,
            timeout=5
        )

    def change_span(self, span):
        if not self.is_trading_active:
            self.current_span = span
        else:
            messagebox.showinfo("Error", "Current Cycle is Running\n please stop the cycel to change time frame")


    

    def fetch_data(self):
        """Fetch data from Binance API."""
        # Function to get Unix timestamp in seconds
        def get_unix_timestamp(dt):
            return int(dt.timestamp())
        
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=500)
        start_timestamp = get_unix_timestamp(start_time)
        end_timestamp = get_unix_timestamp(end_time)
        params = {
                'resolution': f"{self.current_span}",
                'symbol': "BTCUSD",
                'start': start_timestamp,
                'end': end_timestamp,
        }
        response = requests.get(URL, params=params)
        data = response.json()
        # Extract the list of candle data from the response:
        candle_data = data['result']

        # Convert the list of dictionaries into a Pandas DataFrame:
        df = pd.DataFrame(candle_data)
        
        # Convert the Unix timestamp (in seconds) to a human-readable datetime format in UTC:
        df['time'] = pd.to_datetime(df['time'], unit='s', utc=True)

        # Sort the DataFrame by the 'time' column in ascending order
        df = df.sort_values(by='time', ascending=True).reset_index(drop=True)

        # Arrange the DataFrame columns in the desired order:
        df = df[['time', 'open', 'high', 'low', 'close', 'volume']]

        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['volume'] = df['volume'].astype(float)

        # Calculate indicators
        context = {
            'ema_period': 8,
            'acc': 0.04,
            'max_step': 0.2
        }

        # Calculate EMA
        df['EMA'] = talib.EMA(np.array(df['close']), timeperiod=context['ema_period'])

        # Calculate Stochastic Oscillator
        df['STOCHF'], df['STOCHS'] = talib.STOCH(
            np.array(df['high']),
            np.array(df['low']),
            np.array(df['close']),
            fastk_period=14,
            slowk_period=5,
            slowk_matype=0,
            slowd_period=5,
            slowd_matype=0
        )

        # Calculate Parabolic SAR
        df['PSAR'] = talib.SAR(
            np.array(df['high']),
            np.array(df['low']),
            acceleration=context['acc'],
            maximum=context['max_step']
        )
        return df

    def analyze_data(self, df):
        # Ensure df has enough data
        if len(df) > 1:  # Ensure df has more than 1 row
            long_entry = (
                (df['EMA'].shift(1) > df['close'].shift(1)) &
                (df['EMA'] < df['close']) &
                (df['PSAR'] < df['close']) &
                (df['STOCHF'] > df['STOCHS']) &
                (df['STOCHF'] < 80)
            ).iloc[-1]

            short_entry = (
                (df['EMA'].shift(1) < df['close'].shift(1)) &
                (df['EMA'] > df['close']) &
                (df['PSAR'] > df['close']) &
                (df['STOCHF'] < df['STOCHS']) &
                (df['STOCHF'] > 20)
            ).iloc[-1]

            # Trigger notifications based on signals
            if long_entry:
                # Send long entry notification
                self.notify("Long Entry Signal Detected!")

            if short_entry:
                # Send short entry notification
                self.notify("Short Entry Signal Detected!")
        else:
            self.notify("Not enough data to analyze.")

    
    def start_trading(self):
        """Start the trading loop."""
        if not self.is_trading_active:
            self.is_trading_active = True
            self.start_btn.configure(text="Running")
            self.trading_thread = threading.Thread(target=self.trading_loop)
            self.trading_thread.start()
    
    def stop_trading(self):
        """Stop the trading loop."""
        if self.is_trading_active:
            self.is_trading_active = False
            self.start_btn.configure(text="Start")
            if self.trading_thread is not None:
                self.trading_thread.join()

    def trading_loop(self):
        """Continuously fetch and analyze data."""
        while self.is_trading_active:
            df = self.fetch_data()
            if df is not None:
                self.analyze_data(df)
            time.sleep(10)  # Sleep for 10 sec between checks

if __name__ == '__main__':
    app=TradingApp()
    app.mainloop()