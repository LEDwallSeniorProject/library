import cProfile
import pstats
from matrix_library import shapes as s, canvas as c

# Profile the function
profiler = cProfile.Profile()
profiler.enable()


def scrolling():
    canvas = c.Canvas()
    text = s.Phrase("WOW!", [64, 64], size=8)
    for i in range(1000):
        canvas.clear()
        text.translate(-2, 0)
        if text.get_width() + text.position[0] < 0:
            text.set_position([128, (text.position[1] + 64) % 128])
        canvas.add(text)
        canvas.draw()


# Call your method here
result = scrolling()

profiler.disable()
stats = pstats.Stats(profiler).sort_stats("cumtime")
stats.print_stats(10)  # Show top 10 time-consuming calls
