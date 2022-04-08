import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import board
import busio
import adafruit_mlx90640

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

# if using higher refresh rates yields a 'too many retries' exception,
# try decreasing this value to work with certain pi/camera combinations
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = np.zeros(768)
while True:
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    
    data = frame.reshape((24, 32))
    heatmap = sns.heatmap( data, square=True, vmin=0, vmax=1 )
    heatmap.axis('off')
    heatmap.savefig('heatmap.png')
    