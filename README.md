# APSIM Next Generation: Data Extraction & Visualization

A tool for the basic extraction and visualization of data using the APSIM Next Generation simulator. This project automates the retrieval and plotting of simulation results by interfacing directly with the APSIM source code.

> **Note:** This project utilizes the official ApsimNG source code repository: [APSIMInitiative/ApsimX](https://github.com/APSIMInitiative/ApsimX)

---

## ⚙️ Prerequisites

Ensure you have the following installed before getting started:
* Git
* Python (dependencies are managed via `pyproject.toml`)

## 🚀 Installation & Setup

**1. Clone the repositories**
You will need to clone both the APSIM source code and this repository. Keep track of the local directories where these are stored, as you will need the paths for configuration.

```bash
git clone https://github.com/APSIMInitiative/ApsimX.git
git clone https://github.com/joaosuwa/DataExtractionAPSIMNG.git
cd your-repo-name
```

**2. Install Dependencies**
Install all necessary libraries required to execute the program. The required packages are defined in the `pyproject.toml` file.

## 🔧 Configuration

Update the environment directories in the `constants.py` file to point to your local setup:

* `APSIM_DIR`: The path where the ApsimNG source code is stored.
* `SIMULATION_DIR`: The path where your `.apsimx` simulation files are stored.
* `FIELDS_FILE`: *(Optional)* Point to and update the report fields that you wish to extract and visualize.

> ⚠️ **Important:** When setting up your environment, keep in mind that you may have to manually change the directory of where your `.met` file is located using the `[Weather]` manager within your ApsimNG simulations. The simulator does not update this path automatically when moved.

## 💻 Usage

Once your constants are configured and dependencies are installed, simply run the main script:

```bash
python main.py
```

## 📊 Output

All resulting data extractions and visualizations will be automatically generated and saved in the `output/` directory.