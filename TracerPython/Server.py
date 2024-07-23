from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse
from core.UTracer import UTracer
from core.ColorConverter import hex_to_rgb
import time
from core.BuilderSVG import BuilderSVG as SVG
from core.Console import Console as C
from core.ImagePreparer import ImagePreparer
from core.PixelRecolorer import recolor_image
import json
#uvicorn Server:app --reload
app = FastAPI()

origins = [
    "https://ivansavrikov.github.io/VectorizerWebApp/",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/tracer/")
async def vectorize(file: UploadFile = File(...), colors: str = Form(...), detailing: int = Form(...), mode: int = Form(...)):
	contents = await file.read()
	image_bytes = BytesIO(contents)
	image = Image.open(image_bytes)
	image = ImagePreparer.process_image(image)
	
	start_time = time.time()
	recolor_colors = json.loads(colors)
	hex_colors = []
	for color in recolor_colors:
		hex_colors.append(hex_to_rgb(color))
	image = recolor_image(image, hex_colors)
	num_colors = len(hex_colors)
	end_time = time.time()
	clustering_time = end_time - start_time

	analyzing_time = 0

	start_time = time.time()
	svg_paths = UTracer.trace(image, detailing, mode)
	svg_code = SVG.svg_open(image.width, image.height) + SVG.metadata() + svg_paths + SVG.svg_close()
	end_time = time.time()
	tracing_time = end_time - start_time

	svg_data = BytesIO()
	svg_data.write(svg_code.encode("utf-8"))
	result_size = svg_data.tell()
	svg_data.seek(0)

	print(f"\n{C.BOLD}Clustering{C.END}:\t\t{clustering_time:.3f} sec ({clustering_time/60:.1f} min) ({num_colors} colors)")
	print(f"{C.BOLD}Analyzing{C.END} + {C.BOLD}Tracing{C.END}:\t{tracing_time:.3f} sec ({tracing_time/60:.1f} min)")
	print(f"{C.BOLD}Total{C.END}:\t\t\t{C.GREEN}{(clustering_time+analyzing_time+tracing_time):.3f} sec ({(clustering_time+tracing_time)/60:.1f} min){C.END}\n")
	
	print(f"Image ({(image_bytes.tell()/(1024*1024)):.2f} MB or {image_bytes.tell()} bytes): {image.width:,}x{image.height:,} ({image.width*image.height:,} pixels)")
	print(f"SVG ({(result_size/(1024*1024)):.2f} MB or {result_size} bytes)")
	print(f"SVG < BITMAP = {(image_bytes.tell()/result_size):.2f}")

	return StreamingResponse(svg_data, media_type="image/svg+xml", headers={"Content-Disposition": f"attachment; filename={file.filename}.svg"})