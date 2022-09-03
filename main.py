import obd
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ports = obd.scan_serial()
print(ports)
obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.OBD(ports[0], baudrate=None)

cmd = obd.commands.SPEED

x_vals = []
y_vals = []

index = count()

def animate(i):
    response = connection.query(cmd)
    x_vals.append(next(index))
    y_vals.append(float(response.value.magnitude))
    plt.cla()
    plt.plot(x_vals, y_vals)

ani = FuncAnimation(plt.gcf(), animate, interval=10)

plt.tight_layout()
plt.show()

##for i in range(100):
##    response = connection.query(cmd)
##
##    print(response.value)
