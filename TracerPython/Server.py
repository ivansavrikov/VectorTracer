from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse
from core.UTracer import UTracer
from core.ColorClusterizer import quantize_colors
import time
from core.BuilderSVG import BuilderSVG as SVG
from core.Console import Console as C
from core.Point import Point
from core.ImagePreparer import ImagePreparer
import io
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
async def trace(file: UploadFile = File(...), num_colors: int = Form(...), smooth_range: int = Form(...)):
	contents = await file.read()
	image_bytes = BytesIO(contents)
	image = Image.open(image_bytes)
	image = ImagePreparer.process_image(image)
	
	start_time = time.time()
	image = quantize_colors(image, num_colors)
	end_time = time.time()
	clustering_time = end_time - start_time

	analyzing_time = 0

	start_time = time.time()
	svg_image = ''
	svg_paths = ''
	# svg_image = UTracer.put_image(image)
	# svg_body = UTracer.trace(image, smooth_range)
	svg_paths = UTracer.vectorize(image)
	svg_code = SVG.svg_open(image.width, image.height) + SVG.metadata() + svg_image + svg_paths + SVG.svg_close()
	end_time = time.time()
	tracing_time = end_time - start_time

	svg_data = BytesIO()
	svg_data.write(svg_code.encode("utf-8"))
	result_size = svg_data.tell()
	svg_data.seek(0)

	#Вывод информации о работе алгоритма
	print(f"\n{C.BOLD}Clustering{C.END}:\t\t{clustering_time:.3f} sec ({clustering_time/60:.1f} min) ({num_colors} colors)")
	print(f"{C.BOLD}Analyzing{C.END} + {C.BOLD}Tracing{C.END}:\t{tracing_time:.3f} sec ({tracing_time/60:.1f} min)")
	print(f"{C.BOLD}Total{C.END}:\t\t\t{C.GREEN}{(clustering_time+analyzing_time+tracing_time):.3f} sec ({(clustering_time+tracing_time)/60:.1f} min){C.END}\n")
	
	print(f"Image ({(image_bytes.tell()/(1024*1024)):.2f} MB or {image_bytes.tell()} bytes): {image.width:,}x{image.height:,} ({image.width*image.height:,} pixels)")
	print(f"SVG ({(result_size/(1024*1024)):.2f} MB or {result_size} bytes)")

	return StreamingResponse(svg_data, media_type="image/svg+xml", headers={"Content-Disposition": f"attachment; filename={file.filename}.svg"})