import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import shutil

# ===== 設定 =====
input_dir = './A1'  # PNGファイルが保存されているディレクトリを指定
output_file = './A1_combined_roc_curves.png'  # 出力ファイル名を指定
temp_dir = './temp_resized_images'  # 一時保存用ディレクトリ

# ===== 元画像のリサイズ =====
def resize_image(input_path, output_path, scale=2):
    """元画像を拡大して保存"""
    img = Image.open(input_path)
    new_size = (int(img.width * scale), int(img.height * scale))
    resized_img = img.resize(new_size, Image.LANCZOS)
    resized_img.save(output_path)

# 一時ディレクトリを作成
os.makedirs(temp_dir, exist_ok=True)

# 元画像をリサイズして一時ディレクトリに保存
resized_file_paths = []
for file_path in os.listdir(input_dir):
    if file_path.endswith('.png'):
        input_path = os.path.join(input_dir, file_path)
        output_path = os.path.join(temp_dir, file_path)
        resize_image(input_path, output_path, scale=8)
        resized_file_paths.append(output_path)

# ===== ファイルの収集 =====
# リサイズ後の画像を取得
resized_file_paths.sort()  # ファイル名順にソート（必要に応じて変更可能）

# ===== プロット設定 =====
num_files = len(resized_file_paths)
cols = 1      # 1行あたりの列数
rows = (num_files + cols - 1) // cols  # 行数を計算

# 各画像をより大きく表示するためにfigsizeを調整
fig, axes = plt.subplots(rows, cols, figsize=(28, 12 * rows))  # 幅28インチ、高さ6インチ×行数
axes = axes.flatten()  # 1次元配列に変換

# ===== 画像のプロット =====
for i, path in enumerate(resized_file_paths):
    img = mpimg.imread(path)
    axes[i].imshow(img)
    axes[i].axis('off')
    axes[i].set_title(os.path.basename(path), fontsize=20)  # ファイル名をタイトルに設定しフォントサイズを大きく

# 残りの空白セルは非表示
for i in range(num_files, len(axes)):
    axes[i].axis('off')

# 全体タイトル
plt.suptitle("Selected_Anomaly", fontsize=24)  # 全体タイトルをより大きく設定
plt.tight_layout(rect=[0, 0, 1, 0.95])  # 上部の余白を確保

# ===== 保存=====
plt.savefig(output_file, dpi=300)  # 解像度を高めに設定して保存

print(f'Combined image saved at: {output_file}')

# ===== 一時ディレクトリの削除（必要ならコメントアウト）=====
shutil.rmtree(temp_dir)
