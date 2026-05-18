import math

def calculate_path_length(points):
    length = 0.0
    for i in range(len(points) - 1):
        dx = points[i + 1][0] - points[i][0]
        dy = points[i + 1][1] - points[i][1]
        length += math.hypot(dx, dy)
    return length

def calculate_rmse(planned_path, actual_trajectory):
    if not planned_path or not actual_trajectory:
        return float('inf')

    total_error = 0.0
    for actual_point in actual_trajectory:
        ax, ay, _ = actual_point
        min_dist = float('inf')
        for planned_point in planned_path:
            px, py = planned_point
            dist = math.hypot(ax - px, ay - py)
            if dist < min_dist:
                min_dist = dist
        total_error += min_dist ** 2

    return math.sqrt(total_error / len(actual_trajectory))


def calculate_r2(planned_path, actual_trajectory):
    """
    Расчет коэффициента детерминации R² для сравнения реальной траектории с планируемой.
    R² показывает, какую долю вариации реальной траектории объясняет планируемая.
    R² = 1 - (SS_res / SS_tot)
    где:
    SS_res - сумма квадратов расстояний от реальных точек до планируемого пути
    SS_tot - сумма квадратов расстояний от реальных точек до среднего положения реального пути
    """
    if not planned_path or not actual_trajectory or len(actual_trajectory) < 2:
        return 0.0

    # Для каждой реальной точки находим ближайшее расстояние до планируемого пути
    distances_to_planned = []
    for actual_point in actual_trajectory:
        ax, ay, _ = actual_point
        min_dist = float('inf')
        for planned_point in planned_path:
            px, py = planned_point
            dist = math.hypot(ax - px, ay - py)
            if dist < min_dist:
                min_dist = dist
        distances_to_planned.append(min_dist)

    # SS_res - сумма квадратов расстояний до планируемого пути
    ss_res = sum(d ** 2 for d in distances_to_planned)

    # Вычисляем среднее положение реальной траектории
    avg_x = sum(p[0] for p in actual_trajectory) / len(actual_trajectory)
    avg_y = sum(p[1] for p in actual_trajectory) / len(actual_trajectory)

    # SS_tot - сумма квадратов расстояний от реальных точек до их среднего положения
    ss_tot = 0.0
    for actual_point in actual_trajectory:
        ax, ay, _ = actual_point
        dist_to_center = math.hypot(ax - avg_x, ay - avg_y)
        ss_tot += dist_to_center ** 2

    if ss_tot == 0:
        return 1.0

    # R² может быть отрицательным, если модель хуже, чем просто среднее значение
    # Но в нашем случае мы ограничиваем снизу нулем, так как отрицательное значение не имеет смысла
    r2 = 1 - (ss_res / ss_tot)

    # Ограничиваем R² диапазоном [0, 1]
    return max(0.0, min(1.0, r2))

def save_results(filename, planned_path, actual_trajectory, search_time_ms, travel_time_sec, max_speed_cm_s,
                 avg_speed_cm_s):
    planned_length = calculate_path_length(planned_path) if planned_path else 0.0
    rmse = calculate_rmse(planned_path, actual_trajectory)
    r2 = calculate_r2(planned_path, actual_trajectory)

    with open(filename, 'w', encoding='utf-8') as f:

        f.write("РЕЗУЛЬТАТЫ ПРОХОЖДЕНИЯ МАРШРУТА\n")
        f.write(f"Длина спланированного пути: {planned_length:.1f} см\n")
        f.write(f"Время поиска пути: {search_time_ms:.2f} мс\n")
        f.write(f"Время прохождения пути: {travel_time_sec:.2f} сек\n")
        f.write(f"Средняя скорость: {avg_speed_cm_s:.2f} см/с\n")
        f.write(f"Среднеквадратичная ошибка (RMSE): {rmse:.2f} см\n")
        f.write(f"Коэффициент детерминации (R²): {r2:.4f}\n")