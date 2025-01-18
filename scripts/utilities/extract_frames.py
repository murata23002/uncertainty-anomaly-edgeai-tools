import cv2
import os
import argparse
from tqdm import tqdm

def extract_frames(video_path, output_dir, interval=5):
    """
    MP4動画から指定間隔でフレームを抽出し、JPG形式で保存。

    Args:
        video_path (str): 動画ファイルのパス。
        output_dir (str): フレーム画像を保存するディレクトリ。
        interval (int): 抽出間隔（秒単位）。
    """
    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)

    # 動画ファイル名を取得
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    # 動画を読み込む
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return

    # 動画情報を取得
    fps = video_capture.get(cv2.CAP_PROP_FPS)  # フレームレート (frames per second)
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))  # 総フレーム数
    duration = total_frames / fps  # 動画の長さ（秒）
    interval_frames = int(fps * interval)  # 指定間隔（秒）をフレーム数に変換

    print(f"Video: {video_path}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"FPS: {fps:.2f}")
    print(f"Total frames: {total_frames}")
    print(f"Extracting frames every {interval} seconds ({interval_frames} frames)")

    # フレーム抽出ループ
    frame_number = 0
    saved_count = 0
    while True:
        # 指定フレームを読み込む
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video_capture.read()

        # 読み込みが成功しない場合（動画終了など）は終了
        if not ret:
            break

        # 出力ファイル名を生成（動画ファイル名を組み込み）
        output_file = os.path.join(output_dir, f"{video_filename}_frame_{frame_number:06d}.jpg")

        # フレームを保存
        cv2.imwrite(output_file, frame)
        saved_count += 1

        # 次のフレーム番号を計算
        frame_number += interval_frames

    video_capture.release()
    print(f"Extraction complete: {saved_count} frames saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from MP4 video at regular intervals.")
    parser.add_argument('--video_path', required=True, help="Path to the MP4 video file.")
    parser.add_argument('--output_dir', required=True, help="Directory to save extracted frames.")
    parser.add_argument('--interval', type=int, default=5, help="Frame extraction interval in seconds (default: 5 seconds).")

    args = parser.parse_args()

    extract_frames(
        video_path=args.video_path,
        output_dir=args.output_dir,
        interval=args.interval
    )
