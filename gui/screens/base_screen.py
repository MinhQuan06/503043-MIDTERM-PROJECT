
class BaseScreen:
    """Base class for all game screens."""

    def __init__(self, app):
        self.app = app

    def handle_event(self, event):
        """Handle keyboard and mouse events."""
        pass

    def update(self, dt):
        """Update screen state."""
        pass

    def draw(self, surface):
        """Draw the screen."""
        raise NotImplementedError
