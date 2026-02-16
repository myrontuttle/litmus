from vibetuner import VibetunerApp

from litmus.frontend.routes import router


app = VibetunerApp(
    routes=[router],
)
