from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from playwright.async_api import async_playwright
from typing import Optional
import uvicorn
from io import BytesIO
from pathlib import Path
import asyncio
import platform

app = FastAPI()

# Mount static files directory
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.post("/screenshot")
async def take_screenshot(
    url: str = Form(...),
    fullpage: Optional[bool] = Form(False),
    device: str = Form("Desktop"),
    custom_width: Optional[int] = Form(None),
    custom_height: Optional[int] = Form(None)
):
    try:
        p = await async_playwright().start()
        browser = await p.chromium.launch(args=['--no-sandbox'])
        
        # Handle device selection and viewport settings
        context_options = {}
        if device == "custom" and custom_width and custom_height:
            context_options["viewport"] = {"width": custom_width, "height": custom_height}
        elif device == "Desktop":
            context_options["viewport"] = {"width": 1920, "height": 1080}
        elif device != "custom":
            device_descriptor = p.devices.get(device)
            if device_descriptor:
                context_options = device_descriptor
        
        context = await browser.new_context(**context_options)
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=30000)
            # Apply screenshot options if device-specific dimensions are set
            if device != "custom":
                screenshot_bytes = await page.screenshot(full_page=fullpage, type='png', scale="device")
            else:
                screenshot_bytes = await page.screenshot(full_page=fullpage, type='png')
            
            return StreamingResponse(
                BytesIO(screenshot_bytes),
                media_type="image/png"
            )
        finally:
            await context.close()
            await browser.close()
            await p.stop()
            
    except Exception as e:
        return StreamingResponse(
            BytesIO(str(e).encode()),
            media_type="text/plain",
            status_code=500
        )

if __name__ == "__main__":
    platform_system = platform.system()
    print(f"Platform: {platform_system}")
    # breakpoint()
    if platform_system.lower() == "windows":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")