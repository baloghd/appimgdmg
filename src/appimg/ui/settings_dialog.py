"""Settings dialog for appimg"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from appimg.settings import SettingsManager


class SettingsDialog(Gtk.Dialog):
    """Settings dialog for configuring appimg"""
    
    def __init__(self, parent=None):
        super().__init__(
            title="Settings",
            transient_for=parent,
            modal=True,
            destroy_with_parent=True,
            default_width=400,
            default_height=300
        )
        
        self.settings = SettingsManager()
        
        # Add action buttons
        self.add_button("Close", Gtk.ResponseType.CLOSE)
        
        # Get content area
        content_area = self.get_content_area()
        content_area.set_margin_start(24)
        content_area.set_margin_end(24)
        content_area.set_margin_top(24)
        content_area.set_margin_bottom(24)
        content_area.set_spacing(16)
        
        # Create settings box
        settings_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content_area.append(settings_box)
        
        # Section: Notifications
        section_label = Gtk.Label(label="Notifications")
        section_label.add_css_class("title-2")
        section_label.set_halign(Gtk.Align.START)
        settings_box.append(section_label)
        sound_section = Gtk.Label(label="Notifications")
        sound_section.add_css_class("title-2")
        sound_section.set_halign(Gtk.Align.START)
        settings_box.append(sound_section)
        
        # Play sound toggle
        self._create_switch_row(
            settings_box,
            "Play Sound on Install",
            "Play a sound effect after successful installation",
            self.settings.play_sound,
            self._on_sound_toggled
        )
        
        # System notifications toggle
        self._create_switch_row(
            settings_box,
            "System Notifications",
            "Show desktop notifications for install status",
            self.settings.show_notifications,
            self._on_notifications_toggled
        )
        
        # Show current status
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        status_box.set_margin_top(8)
        settings_box.append(status_box)
        
        status_icon = Gtk.Image.new_from_icon_name("emblem-system-symbolic")
        status_icon.set_pixel_size(16)
        status_box.append(status_icon)
        
        status_label = Gtk.Label(label="Settings are saved automatically")
        status_label.add_css_class("caption")
        status_box.append(status_label)
        
        self.connect("response", self._on_response)
    
    def _create_switch_row(self, parent, title, subtitle, active, callback):
        """Create a row with a switch"""
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row.set_margin_top(8)
        row.set_margin_bottom(8)
        
        # Text container
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        text_box.set_hexpand(True)
        row.append(text_box)
        
        # Title
        title_label = Gtk.Label(label=title)
        title_label.set_halign(Gtk.Align.START)
        title_label.add_css_class("heading")
        text_box.append(title_label)
        
        # Subtitle
        subtitle_label = Gtk.Label(label=subtitle)
        subtitle_label.set_halign(Gtk.Align.START)
        subtitle_label.add_css_class("caption")
        subtitle_label.add_css_class("dim-label")
        text_box.append(subtitle_label)
        
        # Switch
        switch = Gtk.Switch()
        switch.set_active(active)
        switch.set_valign(Gtk.Align.CENTER)
        switch.connect("state-set", callback)
        row.append(switch)
        
        parent.append(row)
    
    def _on_sound_toggled(self, switch, state):
        """Handle sound toggle"""
        self.settings.play_sound = state
        return False
    
    def _on_notifications_toggled(self, switch, state):
        """Handle notifications toggle"""
        self.settings.show_notifications = state
        return False
    
    def _on_response(self, dialog, response_id):
        """Handle dialog response"""
        self.destroy()
