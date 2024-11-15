from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import PyPDF2
import os
from fastapi import Request

app = FastAPI()

# Definindo onde os templates HTML estarão localizados
templates = Jinja2Templates(directory="templates")

# Adicionando a funcionalidade de servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para exibir o formulário de upload
@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/mesclar_pdfs/")
async def mesclar_pdfs(files: List[UploadFile] = File(...)):
    merger = PyPDF2.PdfMerger() #criando objeto de mesclagem
    os.makedirs("arquivos", exist_ok=True) #criando diretorio de arquivo temporários

    # salva os arquivos temporariamente no diretório
    for file in files:
        file_location = f"arquivos/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

    # ordena os arquivos
    arquivos_pdf = os.listdir("arquivos")
    arquivos_pdf.sort()
    
    # mesclando os pdfs
    for arquivo in arquivos_pdf:
        if".pdf" in arquivo:
            merger.append(f"arquivos/{arquivo}")
    
    # salva o pdf mesclado
    output_pdf = "PDF_Mesclado.pdf"
    merger.write(output_pdf)
    
    # retorna o pdf mesclado para o usuario
    return FileResponse(output_pdf, media_type="application/pdf", filename=output_pdf)