from collections.abc import Callable
from enum import StrEnum

from .abc_rendering import Renderer
from .impl_rendering import RichTreeRenderer


class RendererToken(StrEnum):
    RICH = "rich"


di: dict[RendererToken, Callable[..., Renderer]] = {
    RendererToken.RICH: lambda clear_console: RichTreeRenderer(clear_console),
}


def get_renderer(token: RendererToken, *args, **kwargs) -> Renderer:
    return di[token](*args, **kwargs)
