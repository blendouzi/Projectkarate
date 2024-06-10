from HCSR04_python_lib import HCSR04
from time import sleep, now
import datetime
import serial.tools.list_ports

# List available ports
ports = serial.tools.list_ports.comports()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

# Prompt user to select the port
com = input("Select Arduino Port (e.g., COM3): ")

# Find the selected port in the list
use = None
for i in range(len(portsList)):
    if portsList[i].startswith("COM" + com):
        use = "COM" + com
        print(f"Using port: {use}")
        break

if use is None:
    print("Selected port not found.")
    exit()

# Configure the serial connection
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()
hcsr_sensor = HCSR04(trigger_pin=18, echo_pin=24)
# Constants
k = 2.6

def readForce(sensor_data = []):
    # Read and process data from the serial port
    valid = False
    try:
        distanceUltrasound = hcsr_sensor.get_distance(sample_size=5, decimal_places=2)
        # distanceUltrasound = float(serialInst.readline().decode('utf-8').strip()) # if using generic reader
        distanceMagneticSensors = float(serialInst.readline().decode('utf-8').strip())
        F = k * distanceUltrasound
        if distanceMagneticSensors > 0 and distanceMagneticSensors <= 5:
            valid =  True
            print(f'Valid Point -- Distance = {str(distanceUltrasound)} [cm]')
        elif distanceMagneticSensors == 0:
            if F <= 30:
                print(f'Valid Point -- Distance = {str(distanceUltrasound)} [cm]')
                valid =  True
            else:
                print(f'Invalid Point -- Distance = {str(distanceUltrasound)} [cm] | Force recorded: {str(F)} [N]')
                valid =  False
        sensor_data.push({
            "distance": distanceMagneticSensors,
            "t": now(),
            "valid": valid
        })
    except ValueError:
        print("Invalid data received, skipping...")
    except serial.SerialException:
        print("Serial connection error.")
        break
    except TimeoutError as ex:
        print(f'ERROR getting distance: {ex}')

    except OSError as ex:
        print(f'ERROR getting distance: {ex}')

    except KeyboardInterrupt:
        print('Measurement stopped.')


def main():
    while True:
        sensor_data = []
        results = readForce(sensor_data)
        for result in results:
            print(result)
        sleep(0.5)

if __name__ == "__main__":
    main()