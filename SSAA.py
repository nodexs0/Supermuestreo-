from PIL import Image
import numpy as np

def SSAA_supersampling(input_image_path, output_image_path, scale_factor):
    # Abrir la imagen original
    img = Image.open(input_image_path)
    original_width, original_height = img.size

    # Calcular las nuevas dimensiones para el supermuestreo
    super_width = original_width * scale_factor
    super_height = original_height * scale_factor

    # Redimensionar la imagen original a las nuevas dimensiones para el supermuestreo
    img_super = img.resize((super_width, super_height), Image.Resampling.LANCZOS)

    # Convertir la imagen redimensionada a un array numpy
    img_super_array = np.array(img_super)

    # Inicializar el array para la imagen final
    final_img_array = np.zeros((original_height, original_width, 3), dtype=np.uint8)

    # Realizar el supermuestreo estándar promediando bloques de píxeles manualmente
    for y in range(original_height):
        for x in range(original_width):
            # Definir el bloque de píxeles a promediar
            block = img_super_array[y*scale_factor:(y+1)*scale_factor, x*scale_factor:(x+1)*scale_factor]

            # Inicializar sumas de los canales RGB
            sum_r = 0
            sum_g = 0
            sum_b = 0

            # Calcular las sumas de los valores RGB en el bloque
            for i in range(scale_factor):
                for j in range(scale_factor):
                    sum_r += block[i, j, 0]
                    sum_g += block[i, j, 1]
                    sum_b += block[i, j, 2]

            # Calcular el promedio de los valores RGB
            num_pixels = scale_factor * scale_factor
            averaged_pixel = [sum_r // num_pixels, sum_g // num_pixels, sum_b // num_pixels]

            # Asignar el valor promedio al píxel final
            final_img_array[y, x] = averaged_pixel

    # Convertir el array numpy de la imagen final a una imagen Pillow
    final_img = Image.fromarray(final_img_array)

    # Guardar la imagen final
    final_img.save(output_image_path)

# Uso del método average_supersampling
input_image_path = 'image1.jpg'
output_image_path = 'SSAA.jpg'
scale_factor = 6  # Factor de supermuestreo

SSAA_supersampling(input_image_path, output_image_path, scale_factor)
