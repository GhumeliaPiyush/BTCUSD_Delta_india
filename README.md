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
2. **Create and Activate a Conda Environment (recommended for using TA-Lib)**:
    ```bash
    conda create -n trading-signals python=3.x
    conda activate trading-signals
3. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
  Note: Ensure to install TA-Lib within the conda environment for compatibility:
   ```bash
   conda install -c conda-forge ta-lib
   ```
## Usage
1.  **Run the Application:**
    ```bash
    python main.py
2.  **Select Time Frame:** Choose the desired time frame from the ComboBox.
3.  **Generate Trading Signals:** Click the "Start" button to generate trading signals based on selected indicators.
4.  **Receive Notifications:** Trading signals will be displayed as desktop notifications.

## Disclaimer
This project is intended for study and educational purposes only. The use of this project for actual trading is at your own risk. 
The author is not responsible for any financial gains or losses resulting from the use of this project. 
Please exercise caution and perform your own due diligence before engaging in trading activities.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
