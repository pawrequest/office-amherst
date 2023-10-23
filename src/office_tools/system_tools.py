import asyncio
import os
import winreg as reg
from functools import lru_cache
from pathlib import Path


def print_file(file_path: Path):
    try:
        os.startfile(str(file_path), "print")
        return True
    except Exception as e:
        print(f"Failed to print: {e}")
        return False


async def wait_for_process(process):
    while True:
        res = process.poll()
        if res is not None:
            break
        await asyncio.sleep(3)
    print("Process has finished.")


@lru_cache(maxsize=None)
def check_registry(reg_path: str) -> bool:
    try:
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path)
        reg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
