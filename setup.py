import sys
from cx_Freeze import setup, Executable

includefiles = ["Translate_data.json", "Pilot_Report_Config.ini"]
build_exe_options = {"packages":[], "include_files": includefiles}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "Pilot Report Tool",
    description = "RPT",
    options = {"build_exe": build_exe_options},
    executables = [Executable("DataFramePlayground.pyw", base=base)]
)