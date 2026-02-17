import markdown

def convert_to_html(markdown_text):
    # Convert markdown text to HTML
    html = markdown.markdown(markdown_text)
    return html

# Example usage
llm_response = """
Here is a sample JavaScript program that prints \"Hello, World!\" to the console:\n\n```javascript\n// Sample JavaScript Program\nconsole.log(\"Hello, World!\");\n```\n\nFeel free to ask if you need any further assistance or have more specific requirements!
"""

html_output = convert_to_html(llm_response)
print(html_output)
