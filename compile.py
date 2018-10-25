
import subprocess
import os

# Create build directory
directory = "build"
if not os.path.exists(directory):
    os.makedirs(directory)
os.chdir(directory)

# build project with cmake
cmakeCmd = ["cmake.exe", "-G", "Visual Studio 15 2017 Win64", ".."]
cmakeRetCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=True)
os.chdir("..")

# build .exe with msbuild
msbuildCmd = ["build.cmd", "Release", directory + "/pbrain-PARIS-Florian-Bacho.vcxproj"]
msbuildRetCode = subprocess.check_call(msbuildCmd, stderr=subprocess.STDOUT, shell=True)

# cp files to the root of the project
os.system('copy "Release/." .')