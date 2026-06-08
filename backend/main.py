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
from semantic import SemanticAnalyzer

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
        lexer.lineno = 1
        
        ast = parser.parse(matlab_code, lexer=lexer)

        if not ast:
            return {
                "success": False,
                "error": "Nie udało się wygenerować drzewa (błąd krytyczny)."
            }
        
        analyzer = SemanticAnalyzer()
        semantic_errors = analyzer.analyze(ast)

        if semantic_errors:
            error_msg = "\n".join(semantic_errors)
            return {
                "success": False,
                "error": error_msg,
                "ast": str(ast)
            }

        python_code = generator.generate(ast)

        return {
            "success": True,
            "python": python_code,
            "ast": str(ast)
        }

    except ValueError as parse_error:
        return {
            "success": False,
            "error": str(parse_error)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Wewnętrzny błąd translacji: {str(e)}"
        }

@app.post("/run")
def run_code(data: CodeInput):
    output = run_python_code(data.code)
    return output