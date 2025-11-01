"""
Custom Gradio themes
"""
import gradio as gr

def get_voicemeet_theme():
    """
    Custom theme for Voicemeet_sum
    
    Returns:
        Gradio theme
    """
    return gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="gray",
        font=("Arial", "sans-serif"),
        font_mono=("Courier", "monospace")
    )

def get_dark_theme():
    """
    Dark theme variant
    
    Returns:
        Dark theme
    """
    return gr.themes.Monochrome()

