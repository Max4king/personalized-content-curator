import gradio as gr
from model import news_summary

with gr.Blocks() as app:
    gr.Markdown("# News Summary Generator")
    with gr.Tabs():
        with gr.TabItem("Summary"):
            interests_input = gr.Textbox(label="Enter your interests")
            title_output = gr.Textbox(label="Title", lines=1, placeholder="Summary Title")
            summary_output = gr.Textbox(label="Summary", lines=10, placeholder="Text Summary")
            # rating_output = gr.Slider(minimum=0, maximum=5, step=1, label="Rating from 0 to 5")
            submit_button = gr.Button("Generate Summary")
        
    # When the button is clicked, process the input and set the output
    submit_button.click(    
        fn=news_summary,
        inputs=interests_input,
        outputs=[title_output, summary_output]
    )

app.launch()