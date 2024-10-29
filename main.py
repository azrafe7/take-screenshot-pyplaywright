from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from playwright.sync_api import sync_playwright
import base64
from typing import Optional
import uvicorn

app = FastAPI()

def get_html(screenshot=None, error=None):
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Website Screenshot Tool</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ padding: 20px; }}
            .screenshot-container {{ margin-top: 20px; }}
            img {{ max-width: 100%; border: 1px solid #ddd; border-radius: 4px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="mb-4">Website Screenshot Tool</h1>
            <form action="/screenshot" method="POST" class="mb-4">
                <div class="mb-3">
                    <label for="url" class="form-label">Enter Website URL:</label>
                    <input type="url" class="form-control" id="url" name="url" required 
                           placeholder="https://example.com">
                </div>
                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="fullpage" name="fullpage">
                    <label class="form-check-label" for="fullpage">Capture Full Page</label>
                </div>
                <button type="submit" class="btn btn-primary">Take Screenshot</button>
            </form>
            
            {f'''
            <div class="alert alert-danger" role="alert">
                {error}
            </div>
            ''' if error else ''}
            
            {f'''
            <div class="screenshot-container">
                <h3>Screenshot:</h3>
                <img src="data:image/png;base64,{screenshot}" alt="Website Screenshot">
            </div>
            ''' if screenshot else ''}
        </div>
    </body>
    </html>
    """

@app.get("/", response_class=HTMLResponse)
async def index():
    return get_html()

@app.post("/screenshot", response_class=HTMLResponse)
async def take_screenshot(
    url: str = Form(...),
    fullpage: Optional[bool] = Form(False)
):
    screenshot = None
    error = None
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            
            # Navigate to the URL
            page.goto(url)
            
            # Wait for network requests to finish
            page.wait_for_load_state('networkidle')
            
            # Take screenshot
            screenshot_bytes = page.screenshot(full_page=fullpage)
            browser.close()
            
            # Convert bytes to base64 for embedding in HTML
            screenshot = base64.b64encode(screenshot_bytes).decode()
            
    except Exception as e:
        error = f"Error capturing screenshot: {str(e)}"
    
    return get_html(screenshot=screenshot, error=error)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)