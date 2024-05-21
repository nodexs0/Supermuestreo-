from PIL import Image
import numpy as np

def sss(input_image_path, output_image_path, scale_factor, num_samples):
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

    # Realizar el supermuestreo estocástico
    for y in range(original_height):
        for x in range(original_width):
            # Inicializar sumas de los canales RGB
            sum_r = 0
            sum_g = 0
            sum_b = 0

            # Tomar muestras aleatorias dentro del bloque de píxeles
            for _ in range(num_samples):
                i = np.random.randint(0, scale_factor)
                j = np.random.randint(0, scale_factor)
                pixel = img_super_array[y * scale_factor + i, x * scale_factor + j]
                sum_r += pixel[0]
                sum_g += pixel[1]
                sum_b += pixel[2]

            # Calcular el promedio de los valores RGB
            averaged_pixel = [sum_r // num_samples, sum_g // num_samples, sum_b // num_samples]

            # Asignar el valor promedio al píxel final
            final_img_array[y, x] = averaged_pixel

    # Convertir el array numpy de la imagen final a una imagen Pillow
    final_img = Image.fromarray(final_img_array)

    # Guardar la imagen final
    final_img.save(output_image_path)

# Uso del método SSS
input_image_path = 'image1.jpg'
output_image_path = 'SSS.jpg'
scale_factor = 2  # Factor de supermuestreo
num_samples = 4  # Número de muestras aleatorias por píxel

sss(input_image_path, output_image_path, scale_factor, num_samples)
