ffmpeg -framerate 60 -i %04d.jpg -c:v libx264 -preset veryfast -profile:v high -crf 25 -minrate:v 6M -b:v 6M -maxrate:v 6M -bufsize:v 6M -coder 1 -vf scale=w=-2:h=768:force_original_aspect_ratio=decrease -pix_fmt yuv420p -g 120 -bf 2 -f mp4 -movflags +faststart out.mp4