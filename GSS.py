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

def gss(input_image_path, output_image_path, scale_factor):
    # Abrir la imagen original
    img = Image.open(input_image_path)
    img_array = np.array(img)

    # Interpolación bilineal para escalar la imagen
    img_super_array = bilinear_interpolation(img_array, scale_factor)

    original_height, original_width, _ = img_array.shape

    # Inicializar el array para la imagen final
    final_img_array = np.zeros((original_height, original_width, 3), dtype=np.uint8)

    # Realizar el supermuestreo en una cuadrícula promediando bloques de píxeles manualmente
    for y in range(original_height):
        for x in range(original_width):
            sum_r = 0
            sum_g = 0
            sum_b = 0

            # Calcular las sumas de los valores RGB en el bloque
            for i in range(scale_factor):
                for j in range(scale_factor):
                    pixel = img_super_array[y * scale_factor + i, x * scale_factor + j]
                    sum_r += pixel[0]
                    sum_g += pixel[1]
                    sum_b += pixel[2]

            # Calcular el promedio de los valores RGB
            num_pixels = scale_factor * scale_factor
            averaged_pixel = [sum_r // num_pixels, sum_g // num_pixels, sum_b // num_pixels]

            # Asignar el valor promedio al píxel final
            final_img_array[y, x] = averaged_pixel

    # Convertir el array numpy de la imagen final a una imagen Pillow
    final_img = Image.fromarray(final_img_array)

    # Guardar la imagen final
    final_img.save(output_image_path)

# Uso del método GSS
input_image_path = 'image1.jpg'
output_image_path = 'GSS.jpg'
scale_factor = 2  # Factor de supermuestreo

gss(input_image_path, output_image_path, scale_factor)
