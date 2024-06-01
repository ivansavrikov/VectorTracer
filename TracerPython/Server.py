from core.Tracer import Tracer
from fastapi import FastAPI, UploadFile, Form, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse
from core.UTracer import UTracer
from core.ColorClusterizer import quantize_colors
import time
from core.ImageAnalyzer import ImagePreparer
from core.BuilderSVG import BuilderSVG as SVG
from core.Console import Console as C
from core.UAnalyzer import UAnalyzer
from core.UFragment import UFragment
from core.FragmentAnalyzer import FragmentAnalyzer
from core.Point import Point
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

# @app.post("/tracer/")
async def temp(file: UploadFile = File(...), num_colors: int = Form(...), smooth_range: int = Form(...)):
	contents = await file.read()
	image = Image.open(BytesIO(contents))
	image = ImagePreparer.process_image(image)
	image = quantize_colors(image, num_colors)

	analyzer = FragmentAnalyzer(image)

	svg_body = []

	fragments = UAnalyzer.analyze(image)
	images = []
	for f in fragments.values():
		images.append(UTracer.put_image(analyzer.Analyze(f), f.position))
		for p in f.start_points.keys():
			x, y = p.split(',')
			color = f.start_points[p]
			hex = '#{:02x}{:02x}{:02x}'.format(*color)
			if True:
				svg_body.append(SVG.add_fragment(Point(float(x), float(y)), 1, 1, fill=hex, stroke='purple'))
				svg_body.append(SVG.add_text(Point(float(x), float(y)), 'p', 'red'))


	svg_code = SVG.svg_open(image.width, image.height) + ''.join(images) + ''.join(svg_body) + SVG.svg_close()

	svg_data = BytesIO()
	svg_data.write(svg_code.encode("utf-8"))
	svg_data.seek(0)
	return StreamingResponse(svg_data, media_type="image/svg+xml", headers={"Content-Disposition": f"attachment; filename={file.filename}.svg"})



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
	svg_body = ''
	svg_fragments = ''
	# svg_image = UTracer.put_image(image)
	# svg_fragments = UTracer.draw_fragments(UAnalyzer.analyze(image).values())
	# svg_body = UTracer.trace(image, smooth_range)
	# svg_body = UTracer.u_trace(image, smooth_range)
	svg_body = UTracer.vectorize(image)
	svg_code = SVG.svg_open(image.width, image.height) + SVG.metadata() + svg_image + svg_body + svg_fragments + SVG.svg_close()
	end_time = time.time()
	tracing_time = end_time - start_time

	svg_data = BytesIO()
	svg_data.write(svg_code.encode("utf-8"))
	result_size = svg_data.tell()
	svg_data.seek(0)

	#Вывод информации о работе алгоритма
	print(f"\n{C.BOLD}Clustering{C.END}:\t\t{clustering_time:.3f} sec ({clustering_time/60:.1f} min) ({num_colors} colors)")
	# print(f"{C.BOLD}Analyzing{C.END}:\t\t{analyzing_time:.2f} sec ({analyzing_time/60:.1f} min)")
	print(f"{C.BOLD}Analyzing{C.END} + {C.BOLD}Tracing{C.END}:\t{tracing_time:.3f} sec ({tracing_time/60:.1f} min)")
	print(f"{C.BOLD}Total{C.END}:\t\t\t{C.GREEN}{(clustering_time+analyzing_time+tracing_time):.3f} sec ({(clustering_time+tracing_time)/60:.1f} min){C.END}\n")
	
	print(f"Image ({(image_bytes.tell()/(1024*1024)):.2f} MB or {image_bytes.tell()} bytes): {image.width:,}x{image.height:,} ({image.width*image.height:,} pixels)")
	print(f"SVG ({(result_size/(1024*1024)):.2f} MB or {result_size} bytes)")
	# Возвращение SVG-файла в ответе
	return StreamingResponse(svg_data, media_type="image/svg+xml", headers={"Content-Disposition": f"attachment; filename={file.filename}.svg"})