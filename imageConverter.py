from PIL import Image
import os

input_folder = r"E:\GitHub\PykachuGame\background"
output_folder = r"E:\GitHub\PykachuGame\background\converted"

# Tạo thư mục đích nếu chưa tồn tại
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith(".png"):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        new_filename = os.path.splitext(filename)[0] + ".jpg"
        img = img.convert("RGB")  # Đảm bảo chuyển đổi thành RGB để lưu thành JPEG
        img.save(os.path.join(output_folder, new_filename), "JPEG")
        print(f"Đã chuyển {filename} thành {new_filename}")
