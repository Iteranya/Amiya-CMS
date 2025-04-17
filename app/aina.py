import ai_config as config
from app import llm
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import asyncio
from openai import OpenAI

# Create a thread pool for CPU-bound tasks
executor = ThreadPoolExecutor()

def save_html(html_content, file_name):
    """Save HTML content to file - this can run in a separate thread"""
    output_path = f"app/data/drafts/{file_name}"
    # Open file in text write mode (not binary)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"HTML successfully saved to {output_path}")
    return output_path

def process_website_request(title, content):
    """Process a website generation request - runs in a separate thread"""
    # This is a blocking function that will be run in a thread pool
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Generate the website synchronously since we're already in a separate thread
        website_html = loop.run_until_complete(llm.generate_website({"title": title, "content": content}))
        # Convert title to filename
        filename = title_to_filename(title)
        
        # Save the HTML file
        filename = title_to_filename(filename)
        save_html(website_html, f"{filename}.html")
        
        print(f"Successfully processed website request: {title}")


    finally:
        loop.close()

def title_to_filename(title):
    # Convert to lowercase
    filename = title.lower()
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '-')
    
    # Remove special characters
    import re
    filename = re.sub(r'[^\w\s_-]', '', filename)
    
    return filename




# Store active generation tasks
active_generations = {}

async def generate_html_stream(content, generation_id):
    ai_config:config.Config = config.load_or_create_config()

    client = OpenAI(
        base_url=ai_config.ai_endpoint,
        api_key=config.get_key(),
    )
    try:
        # Create the prompt
        messages = [
            {
            "role": "system",
            "content": ai_config.system_note
            },
            {
            "role": "user",
            "content": f"{content}"
            },
            {
            "role": "assistant",
            "content": "Understood, here's the requested site: ```html\n"
            }
        ]
        
        # Use synchronous client with stream=True for streaming
        stream = client.chat.completions.create(
            model=ai_config.base_llm,
            messages=messages,
            stream=True
        )
        
        html_so_far = ""
        # Iterate through the stream (this works synchronously)
        for chunk in stream:
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                html_so_far += delta_content
                # Store this chunk
                if generation_id in active_generations:
                    active_generations[generation_id]["chunks"].append(delta_content)
                await asyncio.sleep(0.01)  # Small delay to prevent CPU overload
        
        return html_so_far
    except Exception as e:
        print(f"Error in generation: {str(e)}")
        return f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"