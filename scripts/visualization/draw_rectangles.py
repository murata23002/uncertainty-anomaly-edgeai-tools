import argparse
import os
import cv2
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Draw rectangles on target images.")
    parser.add_argument("--target_file_list", type=str, required=True, help="Path to the target file list CSV.")
    parser.add_argument("--file_list", type=str, required=True, help="Path to the file list CSV.")
    parser.add_argument("--base_dir", type=str, required=True, help="Base directory containing image directories.")
    parser.add_argument("--output_dir", type=str, required=True, help="Output directory for processed images.")
    return parser.parse_args()

def draw_rectangles(target_file_list_path, file_list_path, base_dir, output_dir):
    # Load CSVs
    print(target_file_list_path)
    target_file_list = pd.read_csv(target_file_list_path)
    file_list = pd.read_csv(file_list_path)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Extract target files
    target_file_list["category"] = target_file_list["combined_filename"].str.split("_detect").str[0]
    target_file_list["filename"] = target_file_list["combined_filename"].str.split("_detect").str[1].str[1:]
        
    for _, target_row in target_file_list.iterrows():
        category = target_row["category"]
        filename = target_row["filename"]

        # Locate corresponding rows in file_list
        matched_rows = file_list[(file_list["category"] == category) & (file_list["filename"] ==  ("detect_" + filename))]
        if matched_rows.empty:
            print(f"Skipping: {category}:::{filename} (No match in file_list)")
            continue

        # 拡張子を切り替えて画像パスを探索
        filename_base = filename.rsplit('.', 1)[0]  # 拡張子を除去
        image_found = False
        for ext in ['jpg', 'png']:
            image_path = os.path.join(base_dir, category, "images", f"frame_{filename_base}.{ext}")
            if os.path.exists(image_path):
                image_found = True
                break

        if image_found is False:
            print(f"Image not found: {image_path}")
            continue

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Could not read image: {image_path}")
            continue

        # Draw rectangles for all matched rows
        for _, matched_row in matched_rows.iterrows():
            box_x1, box_y1, box_x2, box_y2 = (
                int(matched_row["box_x1"]),
                int(matched_row["box_y1"]),
                int(matched_row["box_x2"]),
                int(matched_row["box_y2"]),
            )
            cv2.rectangle(image, (box_x1, box_y1), (box_x2, box_y2), (0, 255, 0), 2)

        # Save the result
        output_path = os.path.join(output_dir, f"{category}_{filename_base}.jpg")
        cv2.imwrite(output_path, image)
        print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    args = parse_args()
    draw_rectangles(args.target_file_list, args.file_list, args.base_dir, args.output_dir)
