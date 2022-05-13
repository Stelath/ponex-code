import board
import busio
import adafruit_mlx90640
from gpiozero import MotionSensor

import numpy as np

import time
import heatmap
import messager

def main():
    wait_time = 15 # Minutes
    last_detection = time.time()
    pir = MotionSensor(4)
    
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

    mlx = adafruit_mlx90640.MLX90640(i2c)
    print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

    # if using higher refresh rates yields a 'too many retries' exception,
    # try decreasing this value to work with certain pi/camera combinations
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
    
    while True:
        if pir.motion_detected:
            print("Motion detected!")
            last_detection = time.time()
        elif time.time() - last_detection > wait_time * 60:
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
                    messager.send_message_with_image('Alert your house is burning down! Your cats going up in flames please turn your stove off before your stove turns you off... like your life cause its gonna get extinguished like you should extinguish your stove... its a good joke now stop reading this and turn your stove off!!!', '+18438342997')
                    break
            last_detection = time.time()
        

if __name__ == '__main__':
    main()