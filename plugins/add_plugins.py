from semantic_kernel.kernel import Kernel

from plugins.weather import WeatherPlugin


def add_plugins(kernel: Kernel):
    kernel.add_plugin(WeatherPlugin(), plugin_name="weather")
    # Add more plugins here as needed
