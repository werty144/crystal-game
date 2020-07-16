from src.backend.Geometry import *


class Animation:
    def __init__(self, duration=1):
        self.duration = duration
        self.time_passed = 0
        self.parametric_functions = []
        self.finished = False

    def tick(self, dt):
        self.time_passed += dt
        if self.time_passed > self.duration:
            self.finished = True
            return
        self.tick_all_functions()

    def tick_all_functions(self):
        for function in self.parametric_functions:
            function(self.time_passed)


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
        obj.x, obj.y = start_point.x, start_point.y

        def parametric_function(time):
            return self.steady_linear_movement_function(obj, start_point, end_point, time, duration)

        self.parametric_functions.append(parametric_function)

