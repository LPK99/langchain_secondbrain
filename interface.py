from pdfreader import query
import gradio as gr

with gr.Blocks() as interface:
    api_key_input = gr.Textbox(label="Enter your API key here")
    with gr.Row():
        pdf_file_path_input = gr.Textbox(label="Pdf_directory")
        query_question_input = gr.Textbox(label="Type your question here")
    query_button = gr.Button("Query")
    output = gr.Textbox(label="Answer")

    query_button.click(query, inputs=[query_question_input, pdf_file_path_input, api_key_input],outputs=output)

interface.launch()