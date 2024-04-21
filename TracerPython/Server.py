from core.Tracer import Tracer
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse
from core.UTracer import UTracer
from core.ColorClusterizer import quantize_colors
import time
from core.Console import Console
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

        num_colors = 5
        start_time = time.time()
        image = quantize_colors(image, num_colors)
        end_time = time.time()
        clustering_time = end_time - start_time

        analyzing_time = 0

        start_time = time.time()
        svg_code = UTracer.trace(image, draw_fragments=False)
        end_time = time.time()
        tracing_time = end_time - start_time

        svg_data = BytesIO()
        svg_data.write(svg_code.encode("utf-8"))
        svg_data.seek(0)

        #Вывод информации о работе алгоритма
        print(f"image: {image.width:,}px*{image.height:,}px")
        print(f"\n{Console.BOLD}Clustering{Console.END}:\t\t{clustering_time:.2f} sec ({clustering_time/60:.1f} min) ({num_colors} colors)")
        print(f"{Console.BOLD}Analyzing{Console.END}:\t\t{analyzing_time:.2f} sec ({analyzing_time/60:.1f} min)")
        print(f"{Console.BOLD}Tracing{Console.END}:\t\t{tracing_time:.2f} sec ({tracing_time/60:.1f} min)")
        print(f"{Console.BOLD}Total{Console.END}:\t\t\t{Console.GREEN}{(clustering_time+analyzing_time+tracing_time):.2f} sec ({(clustering_time+tracing_time)/60:.1f} min){Console.END}\n")
        
        # Возвращение SVG-файла в ответе
        return StreamingResponse(svg_data, media_type="image/svg+xml", headers={"Content-Disposition": f"attachment; filename={file.filename}.svg"})
    except Exception:
        print("Exeption in server module")