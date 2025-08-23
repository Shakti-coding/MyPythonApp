from kivy.app import App
from kivy.uix.widget import Widget
from kivy.garden.webview import WebView
from kivy.clock import Clock
import threading
import time
import subprocess
import sys
import os

class WebViewApp(App):
    def build(self):
        # Start Flask app in background thread
        flask_thread = threading.Thread(target=self.start_flask_app, daemon=True)
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
            app.app.run(host='127.0.0.1', port=8000, debug=False)
        except Exception as e:
            print(f"Error starting Flask app: {e}")
    
    def create_webview(self, dt):
        """Create WebView after Flask has started"""
        try:
            webview = WebView(url='http://127.0.0.1:8000')
            self.root.clear_widgets()
            self.root.add_widget(webview)
        except Exception as e:
            print(f"Error creating WebView: {e}")
            # Fallback: try to start browser intent
            self.open_browser_fallback()
    
    def open_browser_fallback(self):
        """Fallback: open in system browser if WebView fails"""
        try:
            from plyer import browser
            browser.open('http://127.0.0.1:8000')
        except Exception as e:
            print(f"Browser fallback failed: {e}")

if __name__ == '__main__':
    WebViewApp().run()