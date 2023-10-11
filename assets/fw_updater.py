import subprocess

from assets.manager import ManagerContext

instructions = ''

exe = 'assets/TerminalBatchUpgrade_Subscribe_TO_V9.02.04.001.iM/TerminalBatchUpgrade.exe'
subprocess.run(exe, shell=True, check=True)

while True:
    serial_or_id = input("Scan Barcode or enter 4 Digit ID:\n")
    with ManagerContext as cmc:
        ...
