from PIL import Image
import numpy as np

def bilinear_interpolation(input_image_array, scale_factor):
    original_height, original_width, num_channels = input_image_array.shape

    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    scaled_img_array = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)

    for y in range(new_height):
        for x in range(new_width):
            src_x = x / scale_factor
            src_y = y / scale_factor

            x0 = int(np.floor(src_x))
            x1 = min(x0 + 1, original_width - 1)
            y0 = int(np.floor(src_y))
            y1 = min(y0 + 1, original_height - 1)

            dx = src_x - x0
            dy = src_y - y0

            for c in range(num_channels):
                top_left = input_image_array[y0, x0, c]
                top_right = input_image_array[y0, x1, c]
                bottom_left = input_image_array[y1, x0, c]
                bottom_right = input_image_array[y1, x1, c]

                top = (1 - dx) * top_left + dx * top_right
                bottom = (1 - dx) * bottom_left + dx * bottom_right
                pixel = (1 - dy) * top + dy * bottom

                scaled_img_array[y, x, c] = int(pixel)

    return scaled_img_array

def sss(input_image_path, output_image_path, scale_factor, num_samples):
    img = Image.open(input_image_path)
    img_array = np.array(img)

    scaled_img_array = bilinear_interpolation(img_array, scale_factor)
    original_height, original_width, _ = img_array.shape

    final_img_array = np.zeros((original_height, original_width, 3), dtype=np.uint8)

    for y in range(original_height):
        for x in range(original_width):
            sum_r = 0
            sum_g = 0
            sum_b = 0

            for _ in range(num_samples):
                i = np.random.randint(0, scale_factor)
                j = np.random.randint(0, scale_factor)
                pixel = scaled_img_array[y * scale_factor + i, x * scale_factor + j]
                sum_r += pixel[0]
                sum_g += pixel[1]
                sum_b += pixel[2]

            averaged_pixel = [sum_r // num_samples, sum_g // num_samples, sum_b // num_samples]
            final_img_array[y, x] = averaged_pixel

    final_img = Image.fromarray(final_img_array)
    final_img.save(output_image_path)

# Uso del método SSS
input_image_path = 'image1.jpg'
output_image_path = 'SSS.jpg'
scale_factor = 6  # Factor de supermuestreo
num_samples = 4  # Número de muestras aleatorias por píxel

sss(input_image_path, output_image_path, scale_factor, num_samples)
