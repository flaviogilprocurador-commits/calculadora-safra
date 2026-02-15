import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise de Quebra de Safra", page_icon="🌾")

# Título Principal - Agora mais focado no produtor
st.title("🌾 Análise de Quebra de Safra")
st.write("Calcule o impacto financeiro na sua safra e veja se você tem direito à prorrogação de dívidas.")
st.markdown("---")

# 1. ENTRADA DE DADOS
st.subheader("1. Localização e Dados da Produção")

cidades = [
    "Juína", "Juara", "Brasnorte", "Campo Novo do Parecis", 
    "Porto dos Gaúchos", "Tapurah", "Itanhangá", "Sorriso", 
    "Nova Mutum", "Lucas do Rio Verde", "Sinop", "Matupá", 
    "Alta Floresta", "Tabaporã"
]

cidade_ref = st.selectbox("Selecione sua Cidade/Região:", ["Selecione..."] + cidades)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**O que foi planejado (Custeio)**")
    prod_esperada = st.number_input("Produtividade Esperada (sc/ha):", value=0.0, step=0.1)
    preco_esperado = st.number_input("Preço de Venda Esperado (R$):", value=0.0, step=0.1)

with col2:
    st.markdown("**O que ocorreu (Realidade)**")
    prod_atual = st.number_input("Produtividade Real Colhida (sc/ha):", value=0.0, step=0.1)
    preco_atual = st.number_input("Preço de Mercado Atual (R$):", value=0.0, step=0.1)

# 2. CÁLCULO FINANCEIRO
receita_planejada = prod_esperada * preco_esperado
receita_atual = prod_atual * preco_atual

if receita_planejada > 0:
    quebra_financeira = (1 - (receita_atual / receita_planejada)) * 100
else:
    quebra_financeira = 0

st.markdown("---")

# 3. DIAGNÓSTICO FINAL
if receita_planejada > 0 and receita_atual > 0:
    st.subheader("📊 Resultado da Análise")
    
    if quebra_financeira >= 20:
        st.error(f"🚨 ALTA QUEBRA DETECTADA: {quebra_financeira:.1f}%")
        st.write(f"A redução na sua capacidade de pagamento em {cidade_ref} atingiu um nível crítico.")
        st.write("De acordo com o Manual de Crédito Rural (MCR 2-6-4), você pode ter direito legal à renegociação de seus débitos.")
        
        # WhatsApp do Dr. Flavio Lemos Gil
        numero_whats = "5566996626402"
        mensagem = (f"Olá Dr. Flavio, fiz a análise de quebra de safra para {cidade_ref}. "
                    f"Minha perda financeira calculada foi de {quebra_financeira:.1f}%. "
                    f"Preciso de orientação sobre prorrogação.")
        
        link_final = f"https://wa.me/{numero_whats}?text={mensagem.replace(' ', '%20')}"
        
        st.markdown(f'''
            <a href="{link_final}" target="_blank">
                <button style="width:100%; height:60px; background-color:#25D366; color:white; border:none; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer;">
                    🟢 ENVIAR ANÁLISE PARA O DR. FLAVIO
                </button>
            </a>
        ''', unsafe_allow_html=True)
    else:
        st.success(f"✅ QUEBRA DENTRO DA MARGEM: {quebra_financeira:.1f}%")
        st.write("Embora haja perda, o índice atual não preenche automaticamente os requisitos do MCR 2-6-4.")
else:
    st.info("Preencha os valores de produtividade e preço para gerar o diagnóstico.")

st.markdown("---")
st.caption("Desenvolvido por Flavio Lemos Gil - Especialista em Direito do Agronegócio.")
