from core       import TemplateFactory, GoogleTranslator
from ui         import MenuAutoApp



# boots the Tkinter UI
#!/usr/bin/env python3
"""
Entry point for MenuAuto application.
Launches the Tkinter UI for selecting source, template, and mode.
"""
from ui.app import MenuAutoApp


def main():
    """Initialize and run the Tkinter application."""
    app = MenuAutoApp()
    app.mainloop()


if __name__ == "__main__":
    main()
