import subprocess
try:
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print("ffmpeg is installed")
except Exception as e:
    print("ffmpeg is not available via subprocess:", e)
