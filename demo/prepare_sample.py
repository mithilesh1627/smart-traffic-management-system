"""Prepare a short rehearsal clip from the user's existing annotated output."""
import shutil,subprocess
from pathlib import Path
from local_env import configure,STATE
configure()
import imageio_ffmpeg
ffmpeg=Path(imageio_ffmpeg.get_ffmpeg_exe())
target=STATE/'bin/ffmpeg.exe'
if not target.exists():shutil.copy2(ffmpeg,target)
source=STATE.parent/'raw_video/unprocessed_traffic_video.mp4'
if not source.exists():raise SystemExit('Existing sample unavailable. Supply an unprocessed video to Run_Demo_Video.ps1 -Video PATH.')
subprocess.run([str(target),'-y','-ss','5','-i',str(source),'-t','6','-an','-vf','scale=640:-2,fps=10','-c:v','libx264','-pix_fmt','yuv420p',str(STATE/'panel_sample.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
(STATE/'SAMPLE_SOURCE.txt').write_text('Six-second excerpt of the user-supplied unprocessed clip: '+str(source)+'. Resized to 640 pixels wide and sampled at 10 FPS for a quick CPU demonstration. This is not a ground-truth counting benchmark.')
print(STATE/'panel_sample.mp4')
