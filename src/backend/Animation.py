from src.backend.Geometry import *


class Animation:
    def __init__(self, duration=1):
        self.duration = duration
        self.time_passed = 0
        self.parametric_functions = []
        self.finished = False

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


class Steady_linear_movement_animation(Animation):
    @staticmethod
    def steady_linear_movement_function(obj, start_point, end_point, time_passed, total_duration):
        segment = Segment(start_point, end_point)
        cur_point = segment.divide_in_ratio(ratio=time_passed / total_duration)
        obj.x, obj.y = cur_point.x, cur_point.y

    def __init__(self, obj, end_point, duration=1, start_point=None):
        assert hasattr(obj, 'x') and hasattr(obj, 'y')
        super().__init__(duration)

        if start_point is None:
            start_point = Point(obj.x, obj.y)
        self.start_point = start_point

        def parametric_function(time):
            self.steady_linear_movement_function(obj, start_point, end_point, time, duration)

        self.parametric_functions.append(parametric_function)

