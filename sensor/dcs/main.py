import random
import time
import csv
from datetime import datetime

#все клево
class SensorEmulator:
    def __init__(self, metric_name, unit, value_range, output_file):
        self.metric_name = metric_name
        self.unit = unit
        self.value_range = value_range
        self.output_file = output_file

    def generate_value(self):
        return random.uniform(self.value_range[0], self.value_range[1])

    def run(self):
        while True:
            # Генерация значения каждую секунду
            value = self.generate_value()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Сохранение данных в файл CSV каждую секунду
            with open(self.output_file, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([current_time, self.metric_name, value, self.unit])

            # Ожидание 1 секунду
            time.sleep(1)


# Пример использования
emulator = SensorEmulator(
    metric_name="Temperature",
    unit="Celsius",
    value_range=(20, 30),
    output_file="sensor_data.csv",
)
emulator.run()
