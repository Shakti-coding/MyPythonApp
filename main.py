

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.logger import Logger
import threading
import time
import os
import sys

# Try to import WebView, fallback if not available
try:
    from kivy.garden.webview import WebView
    WEBVIEW_AVAILABLE = True
    Logger.info("WebView: Garden WebView available")
except ImportError:
    WEBVIEW_AVAILABLE = False
    Logger.warning("WebView: Garden WebView not available, using fallback")

# Try alternative WebView implementations
if not WEBVIEW_AVAILABLE:
    try:
        from kivymd.uix.webview import MDWebView as WebView
        WEBVIEW_AVAILABLE = True
        Logger.info("WebView: KivyMD WebView available")
    except ImportError:
        Logger.warning("WebView: KivyMD WebView not available")

class WebViewApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.flask_server_started = False
        self.server_port = 8000
        
    def build(self):
        Logger.info("App: Starting WebView app build")
        
        # Create main layout
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Add status label
        self.status_label = Label(
            text='Starting NCERT Audio Extractor...\nPlease wait while the server initializes.',
            text_size=(None, None),
            halign='center',
            valign='middle',
            size_hint=(1, 0.3)
        )
        self.main_layout.add_widget(self.status_label)
        
        # Add refresh button
        refresh_btn = Button(
            text='🔄 Refresh App',
            size_hint=(1, 0.1),
            on_press=self.refresh_webview
        )
        self.main_layout.add_widget(refresh_btn)
        
        # Add open browser button for fallback
        browser_btn = Button(
            text='🌐 Open in Browser',
            size_hint=(1, 0.1),
            on_press=self.open_in_browser
        )
        self.main_layout.add_widget(browser_btn)
        
        # Start Flask server
        self.start_flask_server()
        
        # Schedule WebView creation
        Clock.schedule_once(self.create_webview, 5)
        
        return self.main_layout

    def start_flask_server(self):
        """Start Flask server in background thread"""
        def run_flask():
            try:
                Logger.info("Flask: Starting Flask server...")
                
                # Import and configure Flask app
                import app
                
                # Configure Flask for mobile
                app.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
                app.app.config['TEMPLATES_AUTO_RELOAD'] = True
                
                # Run Flask server
                app.app.run(
                    host='0.0.0.0',
                    port=self.server_port,
                    debug=False,
                    use_reloader=False,
                    threaded=True
                )
                
            except Exception as e:
                Logger.error(f"Flask: Failed to start server: {e}")
                Clock.schedule_once(lambda dt: self.show_error(f"Server error: {e}"), 0)
        
        # Start Flask in daemon thread
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        Logger.info("Flask: Server thread started")

    def create_webview(self, dt):
        """Create WebView after Flask server starts"""
        Logger.info("WebView: Attempting to create WebView")
        
        if self.flask_server_started:
            Logger.info("WebView: Flask server confirmed started")
        else:
            # Check if server is responding
            if self.check_server():
                self.flask_server_started = True
                Logger.info("WebView: Server is responding")
            else:
                Logger.warning("WebView: Server not responding yet, retrying...")
                Clock.schedule_once(self.create_webview, 2)
                return
        
        if WEBVIEW_AVAILABLE:
            try:
                # Create WebView
                webview_url = f'http://127.0.0.1:{self.server_port}'
                Logger.info(f"WebView: Creating WebView with URL: {webview_url}")
                
                webview = WebView(url=webview_url)
                
                # Replace content with WebView
                self.main_layout.clear_widgets()
                self.main_layout.add_widget(webview)
                
                Logger.info("WebView: Successfully created WebView")
                return
                
            except Exception as e:
                Logger.error(f"WebView: Failed to create WebView: {e}")
        
        # Fallback: show instructions
        self.show_fallback_interface()

    def check_server(self):
        """Check if Flask server is responding"""
        try:
            import urllib.request
            urllib.request.urlopen(f'http://127.0.0.1:{self.server_port}', timeout=3)
            return True
        except:
            return False

    def show_fallback_interface(self):
        """Show fallback interface when WebView is not available"""
        Logger.info("WebView: Showing fallback interface")
        
        self.main_layout.clear_widgets()
        
        # Status message
        status_text = f'''📱 NCERT Audio Extractor is running!

🌐 Server URL: http://127.0.0.1:{self.server_port}

📋 Features Available:
• YouTube audio extraction
• Telegram bot integration
• Audio file management
• Batch downloads

💡 Use the "Open in Browser" button below
   to access the full web interface.

🔄 Use "Refresh" if the app becomes unresponsive.'''

        fallback_label = Label(
            text=status_text,
            text_size=(None, None),
            halign='center',
            valign='middle',
            size_hint=(1, 0.7)
        )
        self.main_layout.add_widget(fallback_label)
        
        # Control buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3), spacing=10)
        
        refresh_btn = Button(text='🔄 Refresh App', on_press=self.refresh_webview)
        browser_btn = Button(text='🌐 Open in Browser', on_press=self.open_in_browser)
        
        button_layout.add_widget(refresh_btn)
        button_layout.add_widget(browser_btn)
        
        self.main_layout.add_widget(button_layout)

    def show_error(self, error_msg):
        """Show error message"""
        self.status_label.text = f'❌ Error: {error_msg}\n\nTry refreshing or check logs.'

    def refresh_webview(self, instance):
        """Refresh the WebView or restart the interface"""
        Logger.info("App: Refreshing interface")
        self.status_label.text = 'Refreshing...'
        Clock.schedule_once(self.create_webview, 1)

    def open_in_browser(self, instance):
        """Open app in system browser"""
        try:
            from plyer import browser
            browser_url = f'http://127.0.0.1:{self.server_port}'
            browser.open(browser_url)
            Logger.info(f"Browser: Opened {browser_url} in system browser")
        except Exception as e:
            Logger.error(f"Browser: Failed to open browser: {e}")
            try:
                import webbrowser
                webbrowser.open(f'http://127.0.0.1:{self.server_port}')
                Logger.info("Browser: Opened using webbrowser module")
            except Exception as e2:
                Logger.error(f"Browser: All browser methods failed: {e2}")

    def on_pause(self):
        """Handle app pause (Android lifecycle)"""
        Logger.info("App: Application paused")
        return True

    def on_resume(self):
        """Handle app resume (Android lifecycle)"""
        Logger.info("App: Application resumed")

if __name__ == '__main__':
    Logger.info("Main: Starting NCERT Audio Extractor app")
    WebViewApp().run()
