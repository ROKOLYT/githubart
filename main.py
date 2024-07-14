import json
import os
from datetime import datetime
from PIL import Image
import numpy as np

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def make_commits(commit_count):
    for _ in range(commit_count):
        with open('dummy_file.txt', 'a') as file:
            file.write(f'Commit made on {datetime.now()}\n')
        os.system('git add dummy_file.txt')
        os.system('git commit -m "Pixel art commit"')
        
def load_and_process_image(image_path):
    # Load the image and convert to grayscale
    image = Image.open(image_path).convert('L')
    # Convert the image to a NumPy array
    image_array = np.array(image)
    # Normalize the array to a scale of 0 to 4 and invert the values
    normalized_array = 5 - np.round(image_array / 255 * 5).astype(np.uint8)
    return normalized_array

def get_next_pixel(normalized_array, last_pixel):
    normalized_array = load_and_process_image(normalized_array)
    height, width = normalized_array.shape
    x, y = last_pixel['x'], last_pixel['y']
    next_y = y + 1
    next_x = x
    if next_y >= height:
        next_y = 0
        next_x = x + 1

    if next_x >= width:
        return None
    commit_count = normalized_array[next_y, next_x]
    return {'x': next_x, 'y': next_y, 'color': commit_count}

def main():
    config = load_json('config.json')
    current = load_json('current.json')
    
    today = datetime.today()
    if today.weekday() != 6 and current['x'] == 0 and current['y'] == -1:
        print("The first pixel of a new pixel art can only be placed on Sundays.")
        return
    
    if not current['pixel_art']:
        print("No pixel art is currently being processed.")
        current['pixel_art'] = config['queue'].pop(0)
        current['x'], current['y'] = 0, -1
        save_json('config.json', config)
    
    last_pixel = {'x': current['x'], 'y': current['y']}
    next_pixel = get_next_pixel(current['pixel_art'], last_pixel)
    
    if next_pixel is None:
        print("Completed the current pixel art.")
        current['pixel_art'] = None
        save_json('current.json', current)
        return
    
    # make_commits(next_pixel['color'])
    print(next_pixel['color'])
    
    current['x'], current['y'] = next_pixel['x'], next_pixel['y']
    save_json('current.json', current)

if __name__ == '__main__':
    main()