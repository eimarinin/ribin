import random
import time
import csv
from datetime import datetime

# Тест


# Эмулятор датчика
def emulate_sensor(min_value, max_value, metric_name, unit, filename="sensor_data.csv"):
    values = []
    start_time = time.time()

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Записываем заголовки в файл
        writer.writerow(
            ["Дата и время", "Название метрики", "Значение", "Единица измерения"]
        )

        while True:
            current_time = time.time()
            # Генерируем случайное значение в заданном интервале каждую секунду
            value = random.uniform(min_value, max_value)
            values.append(value)
            time.sleep(1)

            # Усредняем и сохраняем данные раз в минуту
            if current_time - start_time >= 60:
                average_value = sum(values) / len(values)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # Сохраняем данные в файл
                writer.writerow([timestamp, metric_name, f"{average_value:.2f}", unit])
                print(f"{timestamp} | {metric_name}: {average_value:.2f} {unit}")

                # Очищаем список значений и обновляем стартовое время
                values.clear()
                start_time = current_time


# Пример использования
emulate_sensor(min_value=20, max_value=25, metric_name="Температура", unit="°C")
