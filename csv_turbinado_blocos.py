import os
import spacy
from collections import Counter
import pandas as pd
from tqdm import tqdm

# === CONFIGURAÇÕES ===
limiar_similaridade = 0.75
frequencia_minima = 10
caminho_textos = r"A:\05_USUARIOS\Nadelly Gama\Nuvem de Palavras\textos"
caminho_saida = r"A:\05_USUARIOS\Nadelly Gama\Nuvem de Palavras\nuvem_formatado.csv"

# === Inicializa spaCy ===
print("🚀 Carregando spaCy...")
nlp = spacy.load("pt_core_news_md")

# Palavras-chave de referência
palavras_chave = [
    "educação", "ambiental", "meio", "ambiente", "natureza", "sustentabilidade",
    "conscientização", "escola", "aprendizagem", "aluno", "professor", "sociedade",
    "conservação", "recursos", "desenvolvimento", "preservação", "cidadania", "ecologia"
]
tokens_referencia = [nlp(p)[0] for p in palavras_chave]

# Função de similaridade com cache
cache_similaridade = {}

def semelhante_ao_tema(palavra):
    if palavra in cache_similaridade:
        return cache_similaridade[palavra]
    token = nlp(palavra)[0]
    resultado = any(token.similarity(ref) >= limiar_similaridade for ref in tokens_referencia)
    cache_similaridade[palavra] = resultado
    return resultado

# Contagem geral
contagem_geral = Counter()

# === Processa cada arquivo individualmente ===
print("📚 Processando textos individualmente...")

for nome_arquivo in tqdm(os.listdir(caminho_textos), desc="🧾 Lendo arquivos"):
    if nome_arquivo.endswith(".txt"):
        caminho_arquivo = os.path.join(caminho_textos, nome_arquivo)
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            texto = f.read().lower()

        nlp.max_length = len(texto) + 1000  # evita erro com textos muito longos
        doc = nlp(texto)

        palavras = [
            token.lemma_ for token in doc
            if token.is_alpha and not token.is_stop and token.lang_ == "pt"
        ]
        contagem_local = Counter(palavras)
        contagem_geral.update(contagem_local)

# === Filtra por similaridade e frequência ===
print("🔍 Filtrando palavras relevantes...")

contagem_frequente = {p: f for p, f in contagem_geral.items() if f >= frequencia_minima}
palavras_relevantes = {
    p: f for p, f in tqdm(contagem_frequente.items(), desc="🔎 Aplicando similaridade")
    if semelhante_ao_tema(p)
}

# === Gera CSV ===
print("💾 Salvando CSV formatado...")
df = pd.DataFrame([
    {"weight": freq, "word": palavra, "color": "", "url": ""}
    for palavra, freq in sorted(palavras_relevantes.items(), key=lambda x: x[1], reverse=True)
])
df.to_csv(caminho_saida, index=False, encoding="utf-8")

print(f"\n✅ CSV gerado com {len(df)} palavras: {caminho_saida}")
