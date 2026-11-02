# Como rodar o Smart Triage com a IA (Gemini)

O sistema funciona de duas formas:

- **Sem chave:** roda normalmente, mas a classificação de risco é feita por
  palavras-chave (modo local), sem IA.
- **Com chave (recomendado):** a classificação (Vermelho, Amarelo ou Verde) e a
  justificativa são geradas pelo Gemini, a IA do Google.

A chave é gratuita, não pede cartão e leva cerca de 2 minutos para criar.

## 1. Criar a chave gratuita

1. Acesse https://aistudio.google.com/api-keys e entre com uma conta Google.
2. Clique em **Criar chave de API** (*Create API key*).
3. Copie a chave gerada (começa com `AIza` ou `AQ.`).

## 2. Preparar o projeto

No terminal, dentro da pasta do projeto:

```bash
python3 -m venv venv
source venv/bin/activate        # no Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Informar a chave

Cole a chave entre as aspas (vale só para este terminal):

```bash
export GEMINI_API_KEY="COLE_SUA_CHAVE_AQUI"     # Mac/Linux
set GEMINI_API_KEY=COLE_SUA_CHAVE_AQUI          # Windows (cmd)
$env:GEMINI_API_KEY="COLE_SUA_CHAVE_AQUI"       # Windows (PowerShell)
```

## 4. Rodar

Teste rápido só da IA:

```bash
python ia.py
```

Deve mostrar três pacientes classificados, com justificativas escritas pela IA.

Sistema completo:

```bash
python main.py
```

## Problemas comuns

- **`[ia] API indisponível ... usando classificação local`:** o Google pode
  estar sobrecarregado (erro 503) ou a chave foi digitada errada. O sistema
  continua funcionando em modo local; basta rodar de novo.
- **`externally-managed-environment`:** faltou criar e ativar o `venv` (passo 2).
- **Privacidade:** a chave não está no repositório de propósito. Ela é pessoal e
  não deve ser compartilhada.
