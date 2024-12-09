import cProfile
import pstats
import matrix_library as matrix

# Profile the function
profiler = cProfile.Profile()
profiler.enable()

def scrolling():
    canvas = matrix.Canvas()
    text = matrix.Phrase("WOW!", [64, 64], size=8)
    for i in range(1000):
        canvas.clear()
        text.translate(-2, 0)
        if text.get_width() + text.position[0] < 0:
            text.set_position([128, (text.position[1] + 64) % 128])
        canvas.add(text)
        canvas.draw()

def benchmark():
    import benchmark

# Call your method here
result = benchmark()

profiler.disable()
stats = pstats.Stats(profiler).sort_stats("tottime")
stats.print_stats(20)  # Show top 10 time-consuming calls
