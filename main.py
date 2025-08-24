from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import time
import subprocess
import sys
import os

try:
    from kivy.garden.webview import WebView
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False


class WebViewApp(App):

    def build(self):
        # Start Flask app in background thread
        flask_thread = threading.Thread(target=self.start_flask_app,
                                        daemon=True)
        flask_thread.start()

        # Wait a moment for Flask to start
        Clock.schedule_once(self.create_webview, 3)

        # Return empty widget initially
        return Widget()

    def start_flask_app(self):
        """Start the Flask app from app.py in background"""
        try:
            # Import and run the Flask app
            import app
            app.app.run(host='0.0.0.0',
                        port=8000,
                        debug=False,
                        use_reloader=False)
        except Exception as e:
            print(f"Error starting Flask app: {e}")

    def create_webview(self, dt):
        """Create WebView after Flask has started"""
        if WEBVIEW_AVAILABLE:
            try:
                webview = WebView(url='http://127.0.0.1:8000')
                self.root.clear_widgets()
                self.root.add_widget(webview)
                return
            except Exception as e:
                print(f"Error creating WebView: {e}")

        # Fallback: show message and try to open browser
        self.show_fallback_message()
        self.open_browser_fallback()

    def show_fallback_message(self):
        """Show fallback message when WebView is not available"""
        label = Label(
            text=
            'WebView not available.\nOpening in system browser...\nServer running on http://127.0.0.1:8000',
            text_size=(None, None),
            halign='center')
        self.root.clear_widgets()
        self.root.add_widget(label)

    def open_browser_fallback(self):
        """Fallback: open in system browser if WebView fails"""
        try:
            from plyer import browser
            browser.open('http://127.0.0.1:8000')
        except Exception as e:
            print(f"Browser fallback failed: {e}")
            # Alternative: use webbrowser module
            try:
                import webbrowser
                webbrowser.open('http://127.0.0.1:8000')
            except Exception as e2:
                print(f"All browser methods failed: {e2}")


if __name__ == '__main__':
    WebViewApp().run()
