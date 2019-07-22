import subprocess

result = subprocess.call(["powershell.exe", "Start-Process", "MyAwezomeApp-1.0.0a2.exe", "-Verb", "runAs"])
print(result)
