from src.backend.Geometry import *
from math import exp


class Animation:
    def __init__(self, duration=1):
        self.duration = duration
        self.time_passed = 0
        self.parametric_functions = []
        self.finished = False
        self.with_fall = False
        self.sound_played = False

    '''Returns an animation consisting of self and other played one after another'''
    def __add__(self, other):
        result = Animation(self.duration + other.duration)
        for self_function in self.parametric_functions:
            def first_function(time, function=self_function):
                if time > self.duration:
                    return
                function(time)
            result.parametric_functions.append(first_function)

        for other_function in other.parametric_functions:
            def delayed_function(time, function=other_function):
                if time <= self.duration:
                    return
                function(time - self.duration)
            result.parametric_functions.append(delayed_function)

        result.with_fall = self.with_fall or other.with_fall
        return result

    def tick(self, dt):
        self.time_passed += dt
        if self.time_passed > self.duration:
            self.finished = True
            ''' Need it to solve the 'ne doehal' problem, arising due to float arithmetic '''
            self.set_all_functions_to_final_state()
            return
        self.tick_all_functions()

    def tick_all_functions(self):
        for function in self.parametric_functions:
            function(self.time_passed)

    def set_all_functions_to_final_state(self):
        for function in self.parametric_functions:
            function(self.duration)


class Parametric_along_curve_animation(Animation):

    def movement_function(self, obj, time_passed, total_duration):
        if time_passed > total_duration:
            print('ANIMATION WARNING. time_passed is greater than total_duration')
        cur_point = self.curve_function(float(clip(time_passed / total_duration, 0, 1)))
        obj.x, obj.y = cur_point.x, cur_point.y

    '''curve function takes argument from [0,1]'''
    def __init__(self, obj, curve_function, duration=1):
        assert hasattr(obj, 'x') and hasattr(obj, 'y')
        super().__init__(duration)
        self.curve_function = curve_function

        def parametric_function(time):
            self.movement_function(obj, time, duration)

        self.parametric_functions.append(parametric_function)


class Linear_movement_animation(Parametric_along_curve_animation):
    def __init__(self, obj, end_point, distribution_function, duration=1, start_point=None):
        if start_point is None:
            start_point = Point(obj.x, obj.y)
        segment = Segment(start_point, end_point)
        super().__init__(obj, lambda t_ratio: segment.divide_in_ratio(distribution_function(t_ratio)), duration)


class Steady_linear_movement_animation(Linear_movement_animation):
    def __init__(self, obj, end_point, duration=1, start_point=None):
        super().__init__(obj, end_point, linear, duration, start_point)


class Smooth_linear_movement_animation(Linear_movement_animation):
    def __init__(self, obj, end_point, duration=1, start_point=None):
        super().__init__(obj, end_point, smooth, duration, start_point)


class Falling_linear_movement_animation(Linear_movement_animation):
    def __init__(self, obj, end_point, duration=0.4, start_point=None):
        super().__init__(obj, end_point, falling, duration, start_point)
        if end_point is not None and start_point is not None:
            if end_point.y != start_point.y:
                self.with_fall = True


class Rush_into_linear_movement_animation(Linear_movement_animation):
    def __init__(self, obj, end_point, duration=1, start_point=None):
        super().__init__(obj, end_point, rush_into, duration, start_point)


def linear(t):
    return t


def falling(t):
    return t ** 2


def sigmoid(x):
    return 1.0 / (1 + exp(-x))


def smooth(t, inflection=10.0):
    error = sigmoid(-inflection / 2)
    return float(clip(
        (sigmoid(inflection * (t - 0.5)) - error) / (1 - 2 * error),
        0, 1,
    ))


def rush_into(t, inflection=10.0):
    return 2 * smooth(t / 2.0, inflection)


def clip(n, a, b):
    if n < a:
        return a
    if n > b:
        return b
    return n
