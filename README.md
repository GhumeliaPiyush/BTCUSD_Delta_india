# BTCUSD_Delta_india

## Overview

This Python project is designed to fetch data from Delta Exchange India for the BTCUSD pair, allowing users to generate trading signals based on various technical indicators. The application supports multiple time frames and provides trading recommendations using the following indicators:

- Exponential Moving Average (EMA)
- Parabolic SAR (Stop and Reverse)
- Stochastic Oscillator

## Features

- **Data Fetching**: Retrieves BTCUSD trading data from Delta Exchange India.
- **Time Frame Selection**: Choose the desired time frame from a ComboBox, with a default set to 5 minutes.
- **Trading Signals**: Generates buy/sell signals based on EMA, Parabolic SAR, and Stochastic Oscillator.
- **Desktop Notifications**: Notifies users of trading signals using the Plyer library.

## Installation

### Prerequisites

- Python 3.x
- The following Python libraries are required:
  - `requests`
  - `pandas`
  - `numpy`
  - `TA-Lib`
  - `plyer`
  - `customtkinter`

### Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
2.**Create and Activate a Conda Environment (recommended for using TA-Lib)**:
  ```bash
  conda create -n trading-signals python=3.x
  conda activate trading-signals
