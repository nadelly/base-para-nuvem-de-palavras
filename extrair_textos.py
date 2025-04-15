import fitz  # PyMuPDF
import os

pasta_pdfs = r"A:/05_USUARIOS/Nadelly Gama/Nuvem de Palavras/pdfs"
pasta_textos = r"A:/05_USUARIOS/Nadelly Gama/Nuvem de Palavras/textos"
os.makedirs(pasta_textos, exist_ok=True)

for nome_arquivo in os.listdir(pasta_pdfs):
    if nome_arquivo.endswith('.pdf'):
        caminho_pdf = os.path.join(pasta_pdfs, nome_arquivo)
        caminho_txt = os.path.join(pasta_textos, nome_arquivo.replace('.pdf', '.txt'))

        try:
            doc = fitz.open(caminho_pdf)
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            doc.close()

            with open(caminho_txt, "w", encoding="utf-8") as f:
                f.write(texto)

            print(f"✅ Texto salvo: {nome_arquivo}")
        except Exception as e:
            print(f"❌ Erro ao processar {nome_arquivo}: {e}")
