import asyncio
import json
import uuid
import re
from fastapi import APIRouter, Form, Body, HTTPException, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from pathlib import Path
from app.aina import generate_html_stream, active_generations, save_html, title_to_filename
from app.crud import get_page_by_slug
import traceback
from app.bundler import StaticBundler
from app.models import Page
router = APIRouter()

@router.post("/save-html")
async def deploy_site(
    content: str = Body(..., example="<html>...</html>"),
    title: str = Body(..., example="my-page")
):
    try:
        title = title_to_filename(title)
        # title = title+".html"
        output_path = save_html(content, title)
        return {"status": "success", "path": output_path}  # Return proper JSON!
    except Exception as e:
        # Print full traceback
        traceback.print_exc()
        # Or capture the traceback as a string
        error_traceback = traceback.format_exc()
        print(error_traceback)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/site-builder", response_class=HTMLResponse)
async def get_html(request: Request):
    bundler = StaticBundler(
        template_path="static/site-builder/index.html",
        scripts_dir="static/site-builder/scripts",
        styles_dir="static/site-builder/styles",
        js_file_order=[
            "utils/*.js",
            "*.js",
            "services/*.js"
        ])
    html = bundler.generate_html()
    slug = request.query_params.get("slug", "")

    # Inject the slug value into the HTML
    if slug != "":
        page: Page = get_page_by_slug(slug)
        html_content = page.html
        
        # Sanitize and escape the slug for HTML attribute
        from html import escape
        escaped_slug = escape(slug)

        safe_html_content = json.dumps(html_content)

        # Escape any closing script tags so it won't terminate the <script> block
        safe_html_content = safe_html_content.replace("</script>", "<\\/script>")

        html = html.replace(
            'const editingHTML = ""',
            f'const editingHTML = {safe_html_content}'
        )
        
        # Update the input field with escaped slug
        html = html.replace(
            '<input type="text" id="site-title" class="form-control" placeholder="Enter site title (e.g. my-kawaii-page)" style="max-width: 400px; margin: 0 auto;">',
            f'<input type="text" id="site-title" class="form-control" placeholder="Enter site title (e.g. my-kawaii-page)" style="max-width: 400px; margin: 0 auto;" value="{escaped_slug}">'
        )

    
    return html

@router.post("/generate-website")
async def generate_website(content: str = Form(...)):
    # Create a unique ID for this generation
    generation_id = str(uuid.uuid4())
    
    # Start generation in background
    task = asyncio.create_task(generate_html_stream(content, generation_id))
    active_generations[generation_id] = {"task": task, "chunks": []}
    
    # Return the ID immediately
    return {"id": generation_id}

@router.get("/stream/{generation_id}")
async def stream_response(generation_id: str):
    if generation_id not in active_generations:
        return {"error": "Generation not found"}
    
    # Create a streaming response
    async def event_generator():
        current_index = 0
        chunks = active_generations[generation_id]["chunks"]
        
        while True:
            # Check if there are new chunks
            if current_index < len(chunks):
                # Send all new chunks
                for i in range(current_index, len(chunks)):
                    yield f"data: {json.dumps({'html': chunks[i]})}\n\n"
                current_index = len(chunks)
            
            # Check if task is done
            if active_generations[generation_id]["task"].done():
                if current_index == len(chunks):  # Make sure we've sent everything
                    yield f"data: {json.dumps({'done': True})}\n\n"
                    break
            
            # Wait before checking again
            await asyncio.sleep(0.1)
        
        # Clean up after streaming is complete
        if generation_id in active_generations:
            del active_generations[generation_id]
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


def regex_html(text):
    # Try to find complete HTML document with doctype
    doctype_pattern = re.compile(r'<!DOCTYPE\s+html[^>]*>.*?</html>', re.DOTALL | re.IGNORECASE)
    match = doctype_pattern.search(text)
    if match:
        return match.group(0)
    
    # Try to find HTML without doctype but with html tags
    html_pattern = re.compile(r'<html[^>]*>.*?</html>', re.DOTALL | re.IGNORECASE)
    match = html_pattern.search(text)
    if match:
        return match.group(0)
    
    return None