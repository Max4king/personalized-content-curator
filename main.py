import gradio as gr

def generate_content(interest, content_type, complexity):
    # This is where you'd integrate your content generation logic
    # For demonstration, we'll just return a simple string based on the inputs
    return f"Generated content about {interest} as a {content_type} with {complexity} complexity."

# Define your Gradio interface
iface = gr.Interface(fn=generate_content,
                     inputs=["text", "dropdown", "slider"],
                     outputs="text",
                     description="Generate personalized content based on your preferences",
                     examples=[["Technology", "Article", 3], ["Cooking", "Tutorial", 2]])

# Input options
iface.input_components[1].choices = ["Article", "Tutorial", "Summary"]  # Dropdown choices
iface.input_components[2].minimum = 1  # Slider min value
iface.input_components[2].maximum = 5  # Slider max value
iface.input_components[2].step = 1  # Slider step

# Launch the interface
iface.launch()
