# ⚙️ Backend Mock Mode for Vercel Deployment

Este documento descreve as alterações realizadas no backend do projeto para permitir sua implantação gratuita na plataforma **Vercel**, utilizando um modo de inferência **mockado** (simulado) de IA.

---

## 🚀 Visão Geral

Para contornar a limitação de **50MB para funções serverless** no plano gratuito da Vercel, foram implementadas adaptações que simulam a inferência de modelos de Machine Learning (como CLIP e ViT). Essas mudanças permitem a execução da aplicação no ambiente da Vercel sem comprometer a estrutura original do backend para ambientes com mais recursos.

---

## 🔧 Alterações Realizadas

### 📁 `backend/requirements.txt`
- ❌ Remoção de bibliotecas pesadas: `transformers`, `torch`.
- ✅ Mantidas apenas as dependências essenciais para o funcionamento da API em modo simulado.

---

### 📁 `backend/src/core/dependencies.py`
- 🧠 Lógica de carregamento dos modelos reais foi **removida**.
- 🛠️ A função `get_all_image_models_and_processors()` agora retorna objetos simulados (`None`) e exibe um **log informativo** indicando a ausência do modelo real.

---

### 📁 `backend/src/services/image_analysis.py`
- 🧪 Toda a inferência baseada em IA foi substituída por um sistema de **tags mockadas**:
  - Seleção aleatória de tags a partir de um `mock_tags_pool`.
  - Geração de confiabilidade aleatória para cada tag.
  - Origem definida como `"Mock AI"`.
- ✅ Mensagem de resposta ajustada:  
  `"Image analysis completed (Mock AI for Vercel Free Tier)"`
- 📌 Garantia de retorno consistente: sempre 5 tags por imagem, mesmo em modo mock.

---

### ⚙️ `vercel.json`
- 📦 `installCommand`: modificado para instalar apenas as dependências leves necessárias.
- 🚫 `maxLambdaSize`: mantido em `50mb`, limite máximo da Vercel Free Tier.

---

## ⚠️ Implicações Importantes

| Contexto | Comportamento |
|----------|----------------|
| **Vercel (Free Tier)** | Executa com IA **simulada**, sem relevância contextual real nas tags retornadas. |
| **Localmente (com dependências reais)** | Executa com os modelos de IA reais, oferecendo análise de imagem precisa e baseada em Machine Learning. |

---

## 💡 Conclusão

Essa abordagem garante:
- ✅ Compatibilidade com **ambientes gratuitos** (como a Vercel Free Tier).
- 🧱 Estrutura pronta para **migração futura** para ambientes com maior capacidade.
- 🔁 Flexibilidade para desenvolver e testar com IA real localmente, sem mudanças estruturais no código.

---

Caso deseje reverter para o modo real de inferência, basta restaurar:
- As dependências completas no `requirements.txt`;
- A lógica original de `dependencies.py` e `image_analysis.py`.