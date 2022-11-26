class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: int) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = self.__class__.__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        self.speed = self.get_distance() / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        self.training_info = InfoMessage(self.training_type,
                                         self.duration,
                                         self.get_distance(),
                                         self.get_mean_speed(),
                                         self.get_spent_calories())
        return self.training_info


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получение количества потраченных калорий."""

        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / self.M_IN_KM
                         * (self.duration
                         * self.MIN_IN_H))
        return self.calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получение количества потраченных калорий."""

        mean_speed_msec = self.get_mean_speed() * self.KMH_IN_MSEC
        height_in_m = self.height / self.CM_IN_M
        duration_in_m = self.duration * self.MIN_IN_H
        self.calories = ((self.CALORIES_WEIGHT_MULTIPLIER
                         * self.weight
                         + (mean_speed_msec**2
                            / height_in_m)
                         * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                         * self.weight)
                         * duration_in_m)
        return self.calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SWIMMING_1: float = 1.1
    CALORIES_MEAN_SPEED_SWIMMING_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получение средней скорости плавания в км/ч."""

        self.speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """Получение количества потраченных калорий."""

        self.calories = ((self.get_mean_speed()
                          + self.CALORIES_MEAN_SPEED_SWIMMING_1)
                         * self.CALORIES_MEAN_SPEED_SWIMMING_2
                         * self.weight
                         * self.duration)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dictory = {'RUN': Running,
                        'WLK': SportsWalking,
                        'SWM': Swimming}

    if workout_type in training_dictory:
        training = training_dictory[workout_type](*data)
        return training


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
