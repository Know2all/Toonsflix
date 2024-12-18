import subprocess

log_file_path = "server.log" 

try:
    with open(log_file_path, "w") as log_file:
        process = subprocess.Popen(
            ["python", "manage.py", "refresh"],
            stdout=log_file,
            stderr=log_file,
            text=True
        )
        print(f"Server is running. Logs are being written to {log_file_path}")
        process.wait()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Process Completed ..!")
