from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from runner import run_python_code
from parser import parser
from lexer import lexer
from generator import MatlabToPythonGenerator
from pathlib import Path

app = FastAPI()
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

generator = MatlabToPythonGenerator()

class CodeInput(BaseModel):
    code: str

BASE_DIR = Path(__file__).resolve().parent
@app.get("/")
def root():
    index_path = BASE_DIR.parent / "frontend" / "index.html"
    return FileResponse(str(index_path))

@app.post("/translate")
def translate(data: CodeInput):

    matlab_code = data.code

    try:
        ast = parser.parse(matlab_code, lexer=lexer)

        python_code = generator.generate(ast)

        return {
            "success": True,
            "python": python_code,
            "ast": str(ast)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/run")
def run_code(data: CodeInput):
    output = run_python_code(data.code)
    return output