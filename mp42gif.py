import subprocess
import os
from typing import Optional


def convert_mp4_to_gif(
    input_path: str,
    output_path: Optional[str] = None,
    fps: int = 15,
    scale: int = -1,
    quality: int = 5,
) -> str:
    """
    Convert MP4 video to GIF using FFmpeg.

    Args:
        input_path: Path to input MP4 file
        output_path: Path for output GIF file (optional, will derive from input if not provided)
        fps: Frames per second for output GIF (default: 15)
        scale: Width to scale the output to. Height will scale proportionally. -1 means keep original size
        quality: Quality of output GIF (1-31, lower means better quality but larger file, default: 5)

    Returns:
        Path to the output GIF file

    Raises:
        FileNotFoundError: If input file doesn't exist
        subprocess.CalledProcessError: If FFmpeg command fails
        RuntimeError: If FFmpeg is not installed
    """
    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Check if ffmpeg is installed
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        raise RuntimeError("FFmpeg is not installed. Please install FFmpeg first.")
    except FileNotFoundError:
        raise RuntimeError("FFmpeg is not installed or not in PATH. Please install FFmpeg first.")

    # Generate output path if not provided
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".gif"

    # Prepare scaling filter
    scale_filter = f"scale={scale}:-1:flags=lanczos" if scale != -1 else "scale=trunc(iw/2)*2:trunc(ih/2)*2"

    # Build the FFmpeg command
    # Using palettegen and paletteuse for better quality
    palette_path = os.path.splitext(output_path)[0] + "_palette.png"

    # Generate palette
    palette_cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-vf",
        f"{scale_filter},fps={fps},palettegen=stats_mode=diff",
        "-y",
        palette_path,
    ]

    # Generate GIF using the palette
    gif_cmd = [
        "ffmpeg",
        "-i",
        input_path,
        "-i",
        palette_path,
        "-lavfi",
        f"{scale_filter},fps={fps}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale={quality}",
        "-y",
        output_path,
    ]

    try:
        # Run commands
        subprocess.run(palette_cmd, check=True, capture_output=True)
        subprocess.run(gif_cmd, check=True, capture_output=True)

        # Clean up palette file
        os.remove(palette_path)

        return output_path

    except subprocess.CalledProcessError as e:
        if os.path.exists(palette_path):
            os.remove(palette_path)
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr.decode()}")


if __name__ == "__main__":

    # 自定义参数
    convert_mp4_to_gif("1.mp4", output_path="1.gif", fps=12, scale=520, quality=2)
