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
class FirstCase(Scene):
    frequencies=list(range(my_dict['number_min'],my_dict['number_max']))
    radios=[2/(2**i) for i in range(my_dict['number_min'],my_dict['number_max'])]
    def construct(self):
        my_circles=self.get_circle(self.radios)
        my_numbers=[]
        for i in range(len(self.radios)):
            if i==len(my_circles)-1:
                break
            my_number=ValueTracker(self.frequencies[i])
            my_circles[1].add_updater(lambda t: self.my_update(my_circles[1],my_circles[0],my_number))
            my_circles[2].add_updater(lambda t: self.my_update(my_circles[2],my_circles[0],my_number))
            my_numbers.append(my_number)
        self.play(ShowCreation(my_circles))
        self.play(*it.chain(*[(my_number.set_value,1) \
            for my_number in my_numbers]))
        self.wait()
    def get_circle(self,radios):
        circles=VGroup()
        for radio in radios:
            circle=Circle(**my_dict['circle_kwargs'],radius=radio)
            circles.add(circle)
        for i in it.count():
            circles[0].move_to(2*LEFT)
            if i ==len(circles)-1:
                break
            circles[i+1].shift(circles[i].points[0])
            circles[i].start=circles[i].copy()
        return circles
    def my_update(self,circle,CIRCLE,alpha):
        circle.become(circle.start)
        circle.rotate(alpha.get_value()*TAU,about_point=circle.get_center())
        circle.rotate(alpha.get_value()*TAU,about_point=CIRCLE.get_center())
        circle.shift(CIRCLE.get_center())
        return circle

class SecondIntent(Scene):
    my_config={
        'radios':[2,1,.5],
        'circle_kwargs':{
            'stroke_width':2,
            'stroke_color':YELLOW
        }
    }
    def construct(self):
        circle_init=self.get_my_circles(self.my_config['radios'][0])
        circle_init.shift(3*LEFT)
        self.play(ShowCreation(circle_init))
        circles_soon=VGroup(*[self.get_my_circles(r) \
            for r in self.my_config['radios'][1:]])
        self.play(ShowCreation(circles_soon))
        self.wait()
    def get_my_circles(self,radio):
        circle=Circle(stroke_width=2,radius=radio)
        return circle

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
        self.play(ShowCreation(my_circles))
        self.play(alpha.set_value,1,rate_func=smooth,run_time=30)
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

class ThridIntent2(Scene):
    my_config={
        'radios':[2/2**(i) for i in range(6)],
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
        my_dot=self.get_dot(my_circles[-1])
        my_path=self.my_path(my_dot)
        my_circles.add_updater(get_my_update)
        self.play(ShowCreation(my_circles))
        self.play(ShowCreation(my_dot))
        self.add(my_path)
        self.play(alpha.set_value,1,rate_func=smooth,run_time=30)
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
    def get_dot(self,circle):
        dot=Dot(radius=0.02,color=RED)
        dot.move_to(circle.points[0])
        dot.add_updater(lambda t: t.move_to(circle.points[0]))
        return dot
    def my_path(self,dot):
        path=VMobject(stroke_width=self.my_config['circle_kwargs']['stroke_width'])
        path.set_points_as_corners([dot.get_center(),dot.get_center()+LEFT*0.001])
        def my_path_update(my_path):
            my_path.append_vectorized_mobject(
                Line(my_path.points[-1],dot.get_center())
            )
            my_path.make_smooth()
        path.add_updater(my_path_update)
        return path

class ThridIntent3(Scene):
    my_config={
        'radios':[1/2**(i) for i in range(6)],
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
        my_dot=self.get_dot(my_circles[-1])
        my_path=self.my_path(my_dot)
        my_vertical_dot=self.my_second_dot(my_dot)
        my_path_2=self.get_my_second_path(my_vertical_dot,alpha)
        my_circles.add_updater(get_my_update)
        line=Line(stroke_width=1)
        line.add_updater(lambda t: t.put_start_and_end_on(my_dot.get_center(),my_vertical_dot.get_center()))
        self.play(ShowCreation(my_circles))
        self.play(ShowCreation(my_dot),ShowCreation(my_vertical_dot),ShowCreation(line))
        self.add(my_path,my_path_2)
        self.play(alpha.set_value,1,rate_func=smooth,run_time=30)
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
    def get_dot(self,circle):
        dot=Dot(radius=0.02,color=RED)
        dot.move_to(circle.points[0])
        dot.add_updater(lambda t: t.move_to(circle.points[0]))
        return dot
    def my_path(self,dot):
        path=VMobject(stroke_width=self.my_config['circle_kwargs']['stroke_width'])
        path.set_points_as_corners([dot.get_center(),dot.get_center()+LEFT*0.001])
        def my_path_update(my_path):
            my_path.append_vectorized_mobject(
                Line(my_path.points[-1],dot.get_center())
            )
            my_path.make_smooth()
        path.add_updater(my_path_update)
        return path
    def my_second_dot(self,first_dot):
        dot_vertical=Dot(radius=0.02,color=RED)
        dot_vertical.move_to(first_dot.get_center()*UP)
        dot_vertical.add_updater(
            lambda m: m.move_to(first_dot.get_center()*UP)
        )
        return dot_vertical
    def get_my_second_path(self,vertical_dot,alpha):
        my_path=VMobject(stroke_width=self.my_config['circle_kwargs']['stroke_width'])
        my_path.set_points_as_corners([vertical_dot.get_center(),vertical_dot.get_center()+0.0001*UP])
        my_path.move_to(vertical_dot.get_center())
        def update_path(path):
            path.append_vectorized_mobject(Line(
                path.points[-1],vertical_dot.get_center()
            ))
            path.make_smooth()
            path.move_to(alpha.get_value()*2*RIGHT)
            my_path.become(path)
        my_path.add_updater(update_path)
        return my_path