import json
import os

from modelos import Riscos

# Em ordem de preferência; se um falhar (ex.: 503 por excesso de demanda), tenta o próximo
MODELOS = ("gemini-3.6-flash", "gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.7-flash")

PROMPT_SISTEMA = """Você é um assistente de triagem médica (Protocolo de Manchester simplificado).
Receba os sintomas de um paciente e classifique o risco:
- VERMELHO: emergência, risco de morte (dor no peito, falta de ar grave, desmaio, convulsão, sangramento intenso, AVC).
- AMARELO: urgência, precisa de atendimento em breve (febre alta, fratura, dor forte, vômitos persistentes).
- VERDE: sem risco imediato (resfriado, dor leve, consulta de rotina).
Responda SOMENTE com JSON no formato:
{"risco": "VERMELHO" | "AMARELO" | "VERDE", "motivo": "justificativa curta em português"}"""

# Usado só quando a API não está disponível (sem chave, sem internet, erro)
PALAVRAS_VERMELHO = ("dor no peito", "falta de ar", "desmaio", "convulsão", "convulsao",
                     "sangramento", "inconsciente", "avc", "infarto", "parada")
PALAVRAS_AMARELO = ("febre", "fratura", "vômito", "vomito", "dor forte", "tontura", "corte")


def _para_risco(texto):
    # Converte "VERMELHO" em Riscos.Vermelho (os nomes do enum não são todos maiúsculos)
    return Riscos[texto.strip().capitalize()]


def classificar_local(sintomas):
    texto = sintomas.lower()
    if any(p in texto for p in PALAVRAS_VERMELHO):
        return Riscos.Vermelho, "Classificação local: sintoma de emergência detectado"
    if any(p in texto for p in PALAVRAS_AMARELO):
        return Riscos.Amarelo, "Classificação local: sintoma de urgência detectado"
    return Riscos.Verde, "Classificação local: nenhum sinal de gravidade detectado"


def classificar_com_api(sintomas, idade=None):
    # importado aqui para o fallback funcionar sem a biblioteca
    from google import genai
    from google.genai import types

    # timeout de 15s por tentativa e sem retentativas internas: se um modelo estiver
    # sobrecarregado (erro 503), passamos logo para o próximo da lista
    cliente = genai.Client(  # lê GEMINI_API_KEY do ambiente
        http_options=types.HttpOptions(timeout=15000, retry_options=types.HttpRetryOptions(attempts=1))
    )
    mensagem = f"Sintomas: {sintomas}"
    if idade is not None:
        mensagem = f"Idade: {idade} anos\n{mensagem}"

    ultimo_erro = None
    for modelo in MODELOS:
        try:
            resposta = cliente.models.generate_content(
                model=modelo,
                contents=mensagem,
                config=types.GenerateContentConfig(
                    system_instruction=PROMPT_SISTEMA,
                    response_mime_type="application/json",
                    temperature=0,
                ),
            )
            dados = json.loads(resposta.text)
            return _para_risco(dados["risco"]), dados["motivo"]
        except Exception as erro:
            ultimo_erro = erro
    raise ultimo_erro


def classificar(sintomas, idade=None):
    """Devolve (Riscos, motivo). Nunca lança erro: se a IA falhar, usa a classificação local."""
    if not sintomas or not sintomas.strip():
        raise ValueError("Informe os sintomas do paciente")

    if os.environ.get("GEMINI_API_KEY"):
        try:
            return classificar_com_api(sintomas, idade)
        except Exception as erro:
            print(f"[ia] API indisponível ({erro}); usando classificação local")
    return classificar_local(sintomas)


if __name__ == "__main__":
    for exemplo in ("dor forte no peito e falta de ar", "febre alta há 2 dias", "coriza leve"):
        risco, motivo = classificar(exemplo)
        print(f"{exemplo!r} -> {risco.name}: {motivo}")
