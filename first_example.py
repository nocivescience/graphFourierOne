from manim import *
import itertools as it
FRAME_HEIGHT=config['frame_height']
FRAME_WIDTH=FRAME_HEIGHT*19/6
FRAME_X_RADIUS=FRAME_WIDTH/2
FRAME_Y_RADIUS=FRAME_HEIGHT/2
my_dict={
    'number_min':1,
    'number_max':7,
    'circle_kwargs':{
        'stroke_width':2,
        'stroke_color':RED
    }
}
class ThridIntent(Scene):
    my_config={
        'radios':[2/2**(i) for i in range(9)],
        'circle_kwargs':{
            'stroke_width':2,
            'stroke_color':YELLOW
        }
    }
    def construct(self):
        my_circles=VGroup(*[Circle(radius=radio,**self.my_config['circle_kwargs'])\
            for radio in self.my_config['radios']])
        self.get_sortment(my_circles)
        for my_circle in my_circles:
            my_circle.copy=my_circle.copy()
        alpha=ValueTracker(0)
        my_freqs=list(map(lambda t: 2/t,self.my_config['radios']))
        def get_my_update(sub_circles):
            for daughter_circle,mother_circle,my_freq in zip(sub_circles[1:],sub_circles[:-1],my_freqs[1:]):
                daughter_circle.become(daughter_circle.copy)
                daughter_circle.move_to(mother_circle.points[0])           
                daughter_circle.rotate(
                    my_freq*alpha.get_value()*TAU,about_point=mother_circle.get_center()
                )
        my_circles.add_updater(get_my_update)
        path=self.get_path(my_circles[0],my_circles[-1]).add_updater(
            lambda path:path.become(self.get_path(my_circles[0],my_circles[-1]))
        )
        self.play(Create(my_circles), Create(path))
        self.play(alpha.animate.set_value(1),rate_func=smooth,run_time=30)
        self.wait()
    def get_circle(self,radio):
        circle=Circle(radius=radio)
        return circle
    def get_sortment(self,circles):
        circles[0].move_to(3*LEFT)
        for i in range(len(circles)):
            if i == len(circles)-1: #porque aca toma el limite superior inclusive
                break
            circles[i+1].move_to(circles[i].points[0])
    def get_path(self, mob, dot):
        path = VMobject(stroke_width=1, color=RED)
        path.set_points_as_corners([dot.get_center(), mob.get_center()])
        return path