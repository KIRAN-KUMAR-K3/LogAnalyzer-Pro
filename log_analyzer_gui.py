import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from threading import Thread  # Import threading here
import logging
import os
import threading

# Regular expression for parsing logs (add different formats)
log_format_dict = {
    "Common Access Log": r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<timestamp>[^\]]+)\] "(?P<action>[^"]+)" (?P<status>\d+)',
    "Custom Log Format": r'(?P<ip>\d+\.\d+\.\d+\.\d+) (?P<timestamp>[^\[]+) \[(?P<action>[^\]]+)\] (?P<status>\d+)',  # Example pattern
}

# Set up logging
logging.basicConfig(level=logging.INFO)

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()

class LogAnalyzer:
    def __init__(self):
        self.data = pd.DataFrame()

    def parse_log(self, file_path, log_format):
        """ Parse the log file and extract data into a DataFrame based on selected format """
        logs = []
        try:
            log_regex = log_format_dict.get(log_format, log_format_dict["Common Access Log"])
            with open(file_path, 'r') as file:
                for line in file:
                    match = re.match(log_regex, line)
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
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Log Analyzer instance
        self.analyzer = LogAnalyzer()

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        """ Create the UI components """
        style = ttk.Style()
        style.configure('TButton', font=("Helvetica", 12), width=20)
        style.configure('TLabel', font=("Helvetica", 14))

        # Title Label
        self.label = ttk.Label(self.root, text="Log Analyzer", font=("Helvetica", 18, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        # Log Format selection
        self.format_label = ttk.Label(self.root, text="Select Log Format:")
        self.format_label.grid(row=1, column=0, padx=20, pady=10, sticky="e")

        self.log_format_combobox = ttk.Combobox(self.root, values=["Common Access Log", "Custom Log Format"])  # Add more formats
        self.log_format_combobox.grid(row=1, column=1, padx=20, pady=10)
        self.log_format_combobox.set("Common Access Log")  # Set default format

        # File selection
        self.browse_button = ttk.Button(self.root, text="Browse Log File", command=self.browse_file)
        self.browse_button.grid(row=2, column=0, padx=20, pady=10)

        # Threshold entry for multiple access attempts
        self.threshold_label = ttk.Label(self.root, text="Threshold (default 5):")
        self.threshold_label.grid(row=3, column=0, padx=20, pady=10, sticky="e")

        self.threshold_entry = ttk.Entry(self.root)
        self.threshold_entry.grid(row=3, column=1, padx=20, pady=10)
        self.threshold_entry.insert(0, "5")

        # Analyze Button
        self.analyze_button = ttk.Button(self.root, text="Analyze Log File", command=self.analyze_logs, state=tk.DISABLED)
        self.analyze_button.grid(row=4, column=0, padx=20, pady=10, columnspan=2)

        # Generate Report Button
        self.report_button = ttk.Button(self.root, text="Generate Report", command=self.generate_report, state=tk.DISABLED)
        self.report_button.grid(row=5, column=0, padx=20, pady=10, columnspan=2)

        # Visualize Requests Button
        self.visualize_button = ttk.Button(self.root, text="Visualize Requests", command=self.visualize_requests, state=tk.DISABLED)
        self.visualize_button.grid(row=6, column=0, padx=20, pady=10, columnspan=2)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="indeterminate")
        self.progress.grid(row=7, column=0, padx=20, pady=20, columnspan=2)

        # Suspicious Entries Label (Added)
        self.suspicious_count_label = ttk.Label(self.root, text="Suspicious Entries: 0")
        self.suspicious_count_label.grid(row=8, column=0, padx=20, pady=10, columnspan=2)

        # Exit Button
        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.quit, style="TButton")
        self.exit_button.grid(row=9, column=0, padx=20, pady=20, columnspan=2)

        # Add Tooltips
        self.add_tooltips()

    def add_tooltips(self):
        """ Add tooltips to buttons for better user guidance """
        ToolTip(self.browse_button, "Browse and select the log file.")
        ToolTip(self.analyze_button, "Analyze the selected log file for suspicious activity.")
        ToolTip(self.report_button, "Generate a CSV report of suspicious activity.")
        ToolTip(self.visualize_button, "Visualize the top 10 IPs by number of requests.")
        ToolTip(self.exit_button, "Exit the application.")

    def browse_file(self):
        """ Open file dialog to select log file """
        file_path = filedialog.askopenfilename(title="Select Log File", filetypes=[("Text Files", "*.log")])
        if file_path:
            self.selected_file = file_path
            messagebox.showinfo("File Selected", f"File selected: {file_path}")
            self.analyze_button.config(state=tk.NORMAL)

    def analyze_logs(self):
        """ Analyze the selected log file """
        self.progress.start()
        threading.Thread(target=self._analyze_logs, daemon=True).start()

    def _analyze_logs(self):
        """ Analyze logs in a separate thread to keep the UI responsive """
        try:
            threshold = int(self.threshold_entry.get())
            log_format = self.log_format_combobox.get()
            if self.analyzer.parse_log(self.selected_file, log_format):
                messagebox.showinfo("Analysis Complete", "Log file has been analyzed successfully.")
                self.report_button.config(state=tk.NORMAL)
                self.visualize_button.config(state=tk.NORMAL)

                # Show suspicious activity count
                failed_logins = self.analyzer.detect_failed_logins()
                multiple_access_attempts = self.analyzer.detect_multiple_access_attempts(threshold)
                suspicious_entries = pd.concat([failed_logins, multiple_access_attempts]).drop_duplicates()
                self.suspicious_count_label.config(text=f"Suspicious Entries: {len(suspicious_entries)}")

        except ValueError:
            messagebox.showerror("Invalid Threshold", "Please enter a valid number for the threshold.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze the log file. Error: {e}")
        finally:
            self.progress.stop()

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
