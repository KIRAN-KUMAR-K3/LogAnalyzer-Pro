# LogAnalyzer-Pro

**LogAnalyzer-Pro** is an advanced Python-based tool designed to analyze network log files, detect suspicious activities, and generate detailed reports. The tool is equipped with a user-friendly graphical interface built with `tkinter`, making it accessible to both technical and non-technical users. This tool helps in monitoring network traffic, identifying potential security issues, and visualizing key data points like failed login attempts and excessive requests from specific IP addresses.

### Key Features
- **Multiple Log Format Support**: Supports the parsing of various log formats. The user can select the log format from a dropdown menu, making the tool flexible for different network logs.
- **Suspicious Activity Detection**: Automatically detects suspicious activities such as failed login attempts and flags excessive requests from the same IP address.
- **CSV Report Generation**: Easily generates CSV reports summarizing suspicious activities like failed logins, multiple access attempts, and more.
- **Data Visualization**: Generates a bar chart visualization of the top 10 most active IP addresses based on the number of requests.
- **Real-Time Progress Updates**: Provides real-time progress updates during log file analysis, including intermediate progress feedback for large log files.
- **Interactive and Easy-to-Use GUI**: A modern, interactive graphical interface for loading logs, analyzing them, generating reports, and visualizing the results. The UI also displays counts of suspicious entries.

## Table of Contents
- [Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Installation

Follow these steps to get **LogAnalyzer-Pro** up and running on your system:

### Prerequisites
- **Python 3.x** (Python 3.6 or higher is recommended)
- **pip** (Python package manager)

### Step 1: Clone the repository
Clone the repository to your local machine using Git:

```bash
git clone https://github.com/KIRAN-KUMAR-K3/LogAnalyzer-Pro.git
cd LogAnalyzer-Pro
```

### Step 2: Install the required Python dependencies
Install the necessary Python libraries via `pip`:

```bash
pip install pandas matplotlib
```

> **Note:** `tkinter` is included by default in most Python installations, so no extra installation is needed for the GUI.

### Step 3: Run the Application
After the dependencies are installed, you can launch the tool by running the following command:

```bash
python log_analyzer_gui.py
```

This will open the **LogAnalyzer-Pro** graphical user interface (GUI) where you can interact with the tool.

## Usage

### 1. **Load Log File**
   - Click the **"Browse Log File"** button to open a file dialog and select the log file you wish to analyze. The tool supports `.log` files with various common access log formats. You can select the log format from a dropdown menu.

### 2. **Select Log Format**
   - Choose the log format that matches your log file from a dropdown menu. The available formats include the default common access log format and other custom formats supported by the tool.

### 3. **Analyze the Logs**
   - Once the log file is loaded and the log format is selected, click the **"Analyze Log File"** button to parse the log data.
   - The tool will process the log file, extracting key data points like IP addresses, timestamps, actions (e.g., login attempts), and HTTP status codes. The progress bar will update in real-time, especially for large log files.

### 4. **Generate Suspicious Activity Report**
   - After the log file is successfully analyzed, the **"Generate Report"** button will be enabled.
   - Click **"Generate Report"** to create a **CSV report** containing all suspicious activities (e.g., failed login attempts, IPs with excessive requests).
   - The report will be saved as `suspicious_activity_report.csv`.

### 5. **Visualize IP Request Data**
   - Click the **"Visualize Requests"** button to generate a **bar chart** showing the top 10 IP addresses based on the number of requests they made.
   - The bar chart helps quickly identify the most active IPs and potential misuse of the network.

### 6. **View Suspicious Activity Count**
   - The tool displays a count of suspicious activities detected, such as the number of failed logins and excessive access attempts, making it easy for users to get a summary of the analysis.

## Example Output

### CSV Report
The generated **CSV report** will contain columns such as:
- **IP Address**: The source IP involved in the suspicious activity.
- **Timestamp**: The exact time when the activity occurred.
- **Action**: The type of request or action (e.g., "failed login").
- **Status Code**: HTTP status code indicating the result of the request (e.g., 404, 403).

**Example CSV Output:**
```csv
IP Address, Timestamp, Action, Status Code
192.168.1.1, 2025-03-17 10:15:00, Failed Login, 403
192.168.1.2, 2025-03-17 10:16:00, Failed Login, 404
192.168.1.3, 2025-03-17 10:17:00, Excessive Requests, 200
```

### Bar Chart Visualization
The **bar chart** will display the top 10 IPs with the highest number of requests, helping users easily spot the most active IPs.

## Contributing

Contributions to **LogAnalyzer-Pro** are always welcome! If you find any bugs or have suggestions for new features, feel free to submit an issue or open a pull request.

### How to Contribute
1. **Fork the Repository**: Create a fork of the repository on GitHub.
2. **Create a Branch**: Create a new branch for your changes.
3. **Make Changes**: Implement your changes or fixes.
4. **Submit a Pull Request**: After making your changes, open a pull request to merge them into the main repository.

### Code Style
- Use PEP 8 guidelines for Python code.
- Write clear and concise commit messages.

## License

**LogAnalyzer-Pro** is open-source software licensed under the **MIT License**. You are free to modify, distribute, and use it in your projects, provided that the original author is credited and the license is included in the distribution.

For more details, see the [LICENSE](LICENSE) file.

## Acknowledgments

- Thanks to the contributors of **tkinter**, **pandas**, and **matplotlib**, which provide the core functionality for the tool.
- Special thanks to all open-source developers whose tools and libraries made this project possible.

---

### **Contact**

If you have any questions, suggestions, or feedback about **LogAnalyzer-Pro**, feel free to reach out to me via GitHub issues or through my contact email.
