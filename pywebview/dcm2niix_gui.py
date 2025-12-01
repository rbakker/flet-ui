import os
import subprocess
import threading
import webview

html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>DICOM to NIfTI Converter</title>
</head>
<body>
  <h2>DICOM to NIfTI Converter (dcm2niix)</h2>
  <button onclick="pywebview.api.select_input()">Select Input Folder</button>
  <button onclick="pywebview.api.select_output()">Select Output Folder</button>
  <progress id="progress" value="0" max="100" style="width:100%"></progress>
  <pre id="console" style="height:300px;overflow:auto;border:1px solid #ccc;"></pre>
</body>
</html>
"""

class Api:
    def __init__(self, window):
        self.window = window
        self.input_folder = ""
        self.output_folder = ""

    def log(self, msg):
        self.window.evaluate_js(
            f"document.getElementById('console').textContent += `{msg}\\n`;"
        )

    def set_progress(self, val):
        self.window.evaluate_js(
            f"document.getElementById('progress').value = {val};"
        )

    def select_input(self):
        folder = self.window.create_file_dialog(webview.FileDialog.FOLDER)
        if folder:
            self.input_folder = folder[0]
            self.log(f"Input folder: {self.input_folder}")
            self.try_run()

    def select_output(self):
        folder = self.window.create_file_dialog(webview.FileDialog.FOLDER)
        if folder:
            self.output_folder = folder[0]
            self.log(f"Output folder: {self.output_folder}")
            self.try_run()

    def try_run(self):
        if self.input_folder and self.output_folder:
            self.log("Starting conversion...")
            self.set_progress(0)
            threading.Thread(target=self.run_dcm2niix, daemon=True).start()

    def run_dcm2niix(self):
        cmd = ["dcm2niix", "-o", self.output_folder, self.input_folder]
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
            )
            progress = 0
            for line in process.stdout:
                self.log(line.strip())
                progress = min(progress + 5, 95)
                self.set_progress(progress)
            process.wait()
            self.set_progress(100)
            self.log("Conversion finished.")
        except FileNotFoundError:
            self.log("Error: dcm2niix not found in PATH.")

if __name__ == "__main__":
    # Create the API first
    api = Api(None)
    # Bind it directly when creating the window
    window = webview.create_window(
        "DICOM to NIfTI Converter",
        html=html,
        width=700,
        height=500,
        js_api=api,
    )
    # Give the API a reference to the window
    api.window = window
    webview.start(debug=False)
