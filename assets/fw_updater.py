import subprocess

instructions = ''

exe = 'assets/TerminalBatchUpgrade_Subscribe_TO_V9.02.04.001.iM/TerminalBatchUpgrade.exe'
subprocess.run(exe, shell=True, check=True)
serial = input("Scan Barcode or enter 4 Digit ID:\n")
if len(serial) == 4:
    ...
