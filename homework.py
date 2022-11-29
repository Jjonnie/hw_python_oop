class InfoMessage:
    """
    Класс который формирует информационное
    сообщение о пройденной тренировке.

    Методы:
        'def __init__()' - Устанавливает необходимые параметры для
    класса 'InfoMessage'.
        'def get_message()' - Возвращает информационное сообщение
    о тренировке.
    """

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: int) -> None:
        """
        Устанавливает все необходимые атрибуты для объекта InfoMessage.

        Параметры:
            'training_type: str' - Тип тренировки в виде строки
            'duration: float' - Длительность тренировки в часах
            'distance: float' - Пройденная дистанция в километрах
            'speed: float' - Средняя скорость в км/ч
            'calories: int' - Количество потраченных калорий
        """
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """
        Возвращает сообщение о проделанной тренировке
        в виде строки с текстом(пример):

        Тип тренировки: Running;
        Длительность: 12.000 ч.;
        Дистанция: 0,784 км;
        Ср. скорость: 5.850 км/ч;
        Потрачено ккал: 364.084.

        Значения округляются до трех символов после точки.
        """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """
    Родительский класс от которого наследуются остальные
    классы тренировки.

    Константы:
        'LEN_STEP: float' - Длина шага при хотьбе/беге в метрах
        'M_IN_KM: int' - Констана для перевода значений из м. в км.
        'MIN_IN_H: int' - Константа для перевода часов в минуты

    Методы:
        'def __init__()' - Устанавливает все необходимые параметры
    для класса 'Training'
        'def get_distance()' - Метод для получения пройденной дистанции в км.
    во время тренировки
        'def get_mean_speed()'- Метод для получения средней скорости движения
    во время тренировки
        'def get_spent_calories()' - Метод для получения потраченных калорий
    во время тренировки
        'def show_training_info()' - Метод для формирования информационного
    сообщения о пройденной тренировки
    """
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        """Метод устанавливает необходимые параметры
        для объекта 'Training'

        Параметры:
        'action: int' - Количество совершенных действий(шагов/гребков)
        'duration: float' - Длительность тренировки в часах
        'weight: float' - Вес спортсмена в килограммах
        'training_type: str' - Название тренировки в виде строки
        """
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = self.__class__.__name__

    def get_distance(self) -> float:
        """
        Метод рассчитывает расстояние по формуле:
        (кол._совершенных действий * длина_шага / количество_минут(конст.)

        Возвращает полученный результат в километрах.
        """
        self.distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        """
        Метод рассчитывает среднюю скорость движения по формуле:
        (преодолённая_дистанция_за_тренировку / время_тренировки)

        Возвращает полученный результат в км/ч.
        """
        self.speed: float = self.get_distance() / self.duration
        return self.speed

    def get_spent_calories(self) -> float:
        """
        Данный метод расчитывает потраченные калории во время
        тренировки. Логика подсчёта калорий для каждого вида
        тренировки будет описываться отдельно в своих классах.
        """
        pass

    def show_training_info(self) -> InfoMessage:
        """
        Метод формирует информационное сообщение и возвращает
        полученный результат.
        """
        self.training_info = InfoMessage(self.training_type,
                                         self.duration,
                                         self.get_distance(),
                                         self.get_mean_speed(),
                                         self.get_spent_calories())
        return self.training_info


class Running(Training):
    """
    Тренировка: бег.

    Константы:
        'CALORIES_MEAN_SPEED_MULTIPLIER: float' - Множитель
        'CALORIES_MEAN_SPEED_SHIFT: float' - Сдвиг

    Методы:
        'def __init__()' - Метод устанавливает необходимые параметры
    для объекта 'Running'
        'def get_spent_calories()' - Метод рассчитывает количество
    потраченных калорий

    """
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,) -> None:
        """Метод устанавливает необходимые параметры для объекта 'Running',
        наследуя их у родительского класса 'Training'
        """
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """
        Метод рассчитывает количество портаченных калорий
        по формуле:
        [(18(конст.) * средняя_скорость + 1.79(конст.)) * вес_спортсмена
        / M_IN_KM * время_тренировки_в_минутах]

        Возвращает полученный результат дробным числом.
        """
        self.calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                         * self.get_mean_speed()
                         + self.CALORIES_MEAN_SPEED_SHIFT)
                         * self.weight / self.M_IN_KM
                         * (self.duration
                         * self.MIN_IN_H))
        return self.calories


class SportsWalking(Training):
    """
    Тренировка: спортивная ходьба.

    Константы:
        'CALORIES_WEIGHT_MULTIPLIER: float' - Множитель
        'CALORIES_SPEED_HEIGHT_MULTIPLIER: float' - Сдвиг
        'KMH_IN_MSEC: float' - Километры в секунду
        'CM_IN_M: int' - Перевод сантиметров в метры

    Методы:
        'def __init__()' - Метод устанавливает необходимые параметры
    для объекта 'SportsWalking'
        'def get_spent_calories()' - Метод рассчитывает количество
    потраченных калорий
    """
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,) -> None:
        """
        Метод устанавливает необходимые параметры для объекта 'SportsWalking'
        наследуя их у родительского класса 'Training'

        Дополнительные параметры:
            'height' - Рост спортсмена
        """
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """
        Метод рассчитывает количество портаченных калорий
        по формуле:
        [((0.035(конст.) * вес + (средняя_скорость_в_метрах_в_секунду**2
        / рост_в_метрах) * 0.029(конст.) * вес) * время_тренировки_в_минутах)]

        Дополнительные параметры для расчетов:
            'mean_speed_msec' - Средняя скорость в м/с
            'height_in_m' - Рост в метрах
            'duration_in_m' - Расстояние в метрах

        Возвращает полученный результат дробным числом.
        """
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
    """
    Тренировка: плавание.

    Константы:
        'LEN_STEP: float' - Длина гребка в метрах
        'CALORIES_MEAN_SPEED_SWIMMING_1: float = 1.1' - Множитель
        'CALORIES_MEAN_SPEED_SWIMMING_2: int = 2' - Сдвиг
    """
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SWIMMING_1: float = 1.1
    CALORIES_MEAN_SPEED_SWIMMING_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,) -> None:
        """
        Метод устанавливает необходимые параметры для объекта 'Swimming'
        наследуя их у родительского класса 'Training'

        Дополнительные параметры:
            'length_pool' - Длина бассейна в метрах
            'count_pool' - Количество проплытых бассейнов
        """
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Метод рассчитывает среднюю скорость плавания по формуле:
        [длина_бассейна * количество_проплытых_бассейнов
        / M_IN_KM / время_тренировки]

        Возвращает результат в км/ч.
        """

        self.speed: float = (self.length_pool
                             * self.count_pool
                             / self.M_IN_KM
                             / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        """
        Метод рассчитывает количество потраченных калорий при плавании
        по формуле:
        [(средняя_скорость + 1.1(конст.)) * 2(конст.) * вес * время_тренировки]

        Возвращает полученный результат дробным числом.
        """

        self.calories: float = ((self.get_mean_speed()
                                + self.CALORIES_MEAN_SPEED_SWIMMING_1)
                                * self.CALORIES_MEAN_SPEED_SWIMMING_2
                                * self.weight
                                * self.duration)
        return self.calories


def read_package(workout_type: str, data: list) -> Training:
    """
    Метод считывает с датчиков тип тренировки и возвращает входные
    данные о данной тренировки.
    """

    training_dictory = {'RUN': Running,
                        'WLK': SportsWalking,
                        'SWM': Swimming}

    if workout_type in training_dictory:
        training = training_dictory[workout_type](*data)
        return training


def main(training: Training) -> None:
    """
    Главная функция. Запускает программу, если в списке есть информация
    о необходимой тренировке.
    """

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
