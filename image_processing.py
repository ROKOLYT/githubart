import numpy as np
from PIL import Image

def split_pixel_arts(image_path):
    # Load the image and convert it to grayscale
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    
    # Find the divider columns (where all pixels in a column are the same)
    # Change axis to 0 to find columns instead of rows
    divider_columns = np.where(np.all(image_array == 255, axis=0))[0]
    
    # Initialize variables for splitting
    start_column = 0
    pixel_arts = []
    
    # Iterate through divider columns to split the image
    for divider_column in divider_columns:
        # Slice the image vertically
        if start_column != divider_column:  # Ensure we're not adding empty slices
            pixel_art = image_array[:, start_column:divider_column]
            pixel_arts.append(pixel_art)
        start_column = divider_column + 1  # +1 to skip the divider column itself
    
    # Don't forget the last piece after the final divider
    last_piece = image_array[:, start_column:]
    if last_piece.size > 0:
        pixel_arts.append(last_piece)
    
    # Optionally, save or process the pixel_arts
    for i, art in enumerate(pixel_arts):
        img = Image.fromarray(art)
        img.save(f'images/pixel_art_{i}.png')
        

def convert_to_uniform_grayscale(image_path, output_path):
    # Load the image and convert it to grayscale
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    
    # Normalize pixel values to range between 0 and 5
    # Divide by the max value (255) and multiply by 5, then round to nearest integer
    normalized_array = np.round(image_array / 255 * 5).astype(np.uint8)
    
    # Convert the numpy array back to an image
    new_image = Image.fromarray(normalized_array)
    
    unique_values = np.unique(normalized_array)
    for unique_value in unique_values:
        print(np.sum(normalized_array == unique_value))
    
    # Optionally, save the processed image
    new_image.save(output_path)
    print(f"Processed image saved to {output_path}")

def resize_pixel_art(image_path, output_path, new_block_size=10):
    # Load the image
    image = Image.open(image_path)
    
    # Calculate the new size (downscale by factor of 10)
    new_width = image.width // 10
    new_height = image.height // 10
    
    # Resize the image to the new size
    resized_image = image.resize((new_width, new_height), Image.NEAREST)
    
    # Optionally, upscale the image to a new block size
    if new_block_size != 1:
        upscaled_width = new_width * new_block_size
        upscaled_height = new_height * new_block_size
        resized_image = resized_image.resize((upscaled_width, upscaled_height), Image.NEAREST)
    
    # Save the processed image
    resized_image.save(output_path)
    print(f"Resized image saved to {output_path}")

if __name__ == '__main__':
    image_path = 'images/pixelart.png'  # Example input file
    output_path = 'images/resized_pixel_art.png'  # Example output file
    new_block_size = 1  # Example new block size
    split_pixel_arts(output_path)

    