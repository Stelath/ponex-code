import board
import busio
import adafruit_mlx90640

import numpy as np

import heatmap
import messager

def main():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

    mlx = adafruit_mlx90640.MLX90640(i2c)
    print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

    # if using higher refresh rates yields a 'too many retries' exception,
    # try decreasing this value to work with certain pi/camera combinations
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

    frame = np.zeros(768)

    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        # continue
        print('Error')
    
    detection_temp = 60
    for temp in frame:
        if temp > detection_temp:
            # start_time = gettime in millis
            #  while start_time + wait time (in millis) > current_time then check for movement, if movement set movment to true and cancel loop
            # if movement isnt true send message
            data = frame.reshape((24, 32))
            heatmap.save_heatmap_to_img(data, 'heatmap.png')
            messager.send_message_with_image('Alert your house is burning down!', 'heatmap.png', '+12102130107')
            break

if __name__ == '__main__':
    main()