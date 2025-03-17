import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
import threading
import logging

# Regular expression for parsing logs (assuming common access log format)
log_format = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<action>[^"]+)" (?P<status>\d+)'

# Set up logging
logging.basicConfig(level=logging.INFO)

class LogAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()

    def parse_log(self, file_path):
        """ Parse the log file and extract data into a DataFrame """
        logs = []
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    match = re.match(log_format, line)
                    if match:
                        logs.append(match.groupdict())
            self.data = pd.DataFrame(logs)
            logging.info(f"Successfully parsed {len(logs)} log entries from {file_path}.")
            return True
        except Exception as e:
            logging.error(f"Error parsing log file: {e}")
            return False

    def detect_failed_logins(self):
        """ Detect failed login attempts (status 404 or 403 for login) """
        failed_logins = self.data[(self.data['action'].str.contains('login')) & (self.data['status'].isin(['404', '403']))]
        return failed_logins

    def detect_multiple_access_attempts(self, threshold=5):
        """ Detect IPs with more than 'threshold' requests """
        ip_counts = self.data['ip'].value_counts()
        suspicious_ips = ip_counts[ip_counts > threshold].index
        return self.data[self.data['ip'].isin(suspicious_ips)]

    def generate_report(self, filename="suspicious_activity_report.csv"):
        """ Generate a CSV report of suspicious activities """
        try:
            suspicious_activities = pd.concat([self.detect_failed_logins(), self.detect_multiple_access_attempts()]).drop_duplicates()
            suspicious_activities.to_csv(filename, index=False)
            logging.info(f"Suspicious activity report generated: {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error generating report: {e}")
            return None

    def visualize_requests(self):
        """ Visualize the number of requests per IP (bar chart) """
        ip_counts = self.data['ip'].value_counts().head(10)
        ip_counts.plot(kind='bar', color='skyblue')
        plt.title('Top 10 IPs by Number of Requests')
        plt.xlabel('IP Address')
        plt.ylabel('Number of Requests')
        plt.show()

class LogAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Analyzer Tool")
        self.root.geometry("600x500")
        
        # Log Analyzer instance
        self.analyzer = LogAnalyzer()

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        """ Create the UI components """
        self.label = ttk.Label(self.root, text="Log Analyzer", font=("Helvetica", 18))
        self.label.pack(pady=20)

        self.browse_button = ttk.Button(self.root, text="Browse Log File", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.analyze_button = ttk.Button(self.root, text="Analyze Log File", command=self.analyze_logs, state=tk.DISABLED)
        self.analyze_button.pack(pady=10)

        self.report_button = ttk.Button(self.root, text="Generate Report", command=self.generate_report, state=tk.DISABLED)
        self.report_button.pack(pady=10)

        self.visualize_button = ttk.Button(self.root, text="Visualize Requests", command=self.visualize_requests, state=tk.DISABLED)
        self.visualize_button.pack(pady=10)

    def browse_file(self):
        """ Open file dialog to select log file """
        file_path = filedialog.askopenfilename(title="Select Log File", filetypes=[("Text Files", "*.log")])
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo("File Selected", f"File selected: {file_path}")
            self.analyze_button.config(state=tk.NORMAL)

    def analyze_logs(self):
        """ Analyze the selected log file """
        threading.Thread(target=self._analyze_logs, daemon=True).start()

    def _analyze_logs(self):
        """ Analyze logs in a separate thread to keep the UI responsive """
        if self.analyzer.parse_log(self.selected_file):
            messagebox.showinfo("Analysis Complete", "Log file has been analyzed successfully.")
            self.report_button.config(state=tk.NORMAL)
            self.visualize_button.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Failed to analyze the log file.")

    def generate_report(self):
        """ Generate the suspicious activity report """
        report = self.analyzer.generate_report()
        if report:
            messagebox.showinfo("Report Generated", f"Suspicious activity report generated: {report}")
        else:
            messagebox.showerror("Error", "Failed to generate the report.")

    def visualize_requests(self):
        """ Visualize IP request data """
        self.analyzer.visualize_requests()

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    gui = LogAnalyzerGUI(root)
    root.mainloop()
