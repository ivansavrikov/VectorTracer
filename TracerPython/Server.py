from core.Tracer import Tracer
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse
from core.UTracer import UTracer
from core.ColorClusterizer import quantize_colors

#uvicorn Server:app --reload
app = FastAPI()

TEST_FOLDER = './ResourcesForTesting/TestFastAPI/'
new_image_path = f"{TEST_FOLDER}default.svg"

# CORS (Cross-Origin Resource Sharing) для работы с внешним frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все origin (необходимо настроить для безопасности в реальном приложении)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tracer/")
async def trace(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        image = quantize_colors(image, 2)
        svg_code = UTracer.trace(image, draw_fragments=False)
        svg_data = BytesIO()
        svg_data.write(svg_code.encode("utf-8"))
        svg_data.seek(0)

        # Возвращение SVG-файла в ответе
        return StreamingResponse(svg_data, media_type="image/svg+xml", headers={"Content-Disposition": f"attachment; filename={file.filename}.svg"})
    except TimeoutError:
        pass