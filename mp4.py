import ffmpeg
import os
from pathlib import Path


def convert_video(input_path, output_path=None):
    """
    将视频转换为 H.264 编码的 MP4 格式

    参数:
        input_path: 输入视频的路径
        output_path: 输出视频的路径（可选，默认在原文件名后加上 "_converted"）

    返回:
        output_path: 转换后视频的路径
    """
    try:
        # 确保输入文件存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"找不到输入文件: {input_path}")

        # 如果没有指定输出路径，在原文件名后加上"_converted"
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(input_file.parent / f"{input_file.stem}_converted.mp4")

        # 设置转码参数
        stream = ffmpeg.input(input_path)

        # 使用 H.264 编码，设置较好的兼容性参数
        stream = ffmpeg.output(
            stream,
            output_path,
            vcodec="libx264",  # 视频编码器
            acodec="aac",  # 音频编码器
            preset="medium",  # 编码速度和质量的平衡
            crf=23,  # 视频质量参数，范围0-51，越小质量越好
            movflags="+faststart",  # 支持边下载边播放
        )

        # 开始转码，覆盖已存在的输出文件
        ffmpeg.run(stream, overwrite_output=True)

        print(f"转换完成！输出文件: {output_path}")
        return output_path

    except ffmpeg.Error as e:
        print(f"FFmpeg 错误: {e.stderr.decode()}")
        raise
    except Exception as e:
        print(f"发生错误: {str(e)}")
        raise


if __name__ == "__main__":
    # 使用示例
    input_video = "mikuchan.mp4"  # 替换为你的视频路径
    try:
        converted_path = convert_video(input_video)
        print(f"视频已成功转换为通用格式：{converted_path}")
    except Exception as e:
        print(f"转换失败：{str(e)}")
