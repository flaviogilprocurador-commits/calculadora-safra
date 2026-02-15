import streamlit as st

# Configuração da página
st.set_page_config(page_title="Análise de Quebra de Safra", page_icon="🌱", layout="centered")

# Título Principal
st.title("🌾 Análise de Quebra de Safra")
st.write("Calcule o impacto financeiro na sua produção e verifique o enquadramento no MCR 2-6-4.")
st.markdown("---")

# 1. ENTRADA DE DADOS
st.subheader("1. Localização e Dados da Produção")

# Lista completa das cidades do Mato Grosso em ordem alfabética
cidades_mt = [
    "Abadia dos Dourados", "Acorizal", "Água Boa", "Albuquerque", "Alta Floresta", "Alto Araguaia", 
    "Alto Boa Vista", "Alto Garças", "Alto Paraguai", "Alto Taquari", "Apiacás", "Araguaiana", 
    "Araguainha", "Araputanga", "Arenápolis", "Aripuanã", "Barão de Melgaço", "Barra do Bugres", 
    "Barra do Garças", "Bom Jesus do Araguaia", "Brasnorte", "Cáceres", "Campinápolis", 
    "Campo Novo do Parecis", "Campo Verde", "Campos de Júlio", "Canabrava do Norte", 
    "Canarana", "Carlinda", "Castanheira", "Chapada dos Guimarães", "Cláudia", "Cocalinho", 
    "Colíder", "Colniza", "Comodoro", "Confresa", "Conquista D'Oeste", "Cotriguaçu", 
    "Cuiabá", "Curvelândia", "Denise", "Diamantino", "Dom Aquino", "Feliz Natal", 
    "Figueirópolis D'Oeste", "Gaúcha do Norte", "General Carneiro", "Glória D'Oeste", 
    "Guarantã do Norte", "Guiratinga", "Indiavaí", "Ipiranga do Norte", "Itanhangá", 
    "Itaúba", "Itiquira", "Jaciara", "Jangada", "Jauru", "Juara", "Juína", "Juruena", 
    "Juscimeira", "Lambari D'Oeste", "Lucas do Rio Verde", "Luciara", "Marcelândia", 
    "Matupá", "Mirassol d'Oeste", "Nobres", "Nortelândia", "Nossa Senhora do Livramento", 
    "Nova Bandeirantes", "Nova Brasilândia", "Nova Canaã do Norte", "Nova Guarita", 
    "Nova Lacerda", "Nova Marilândia", "Nova Maringá", "Nova Monte Verde", "Nova Mutum", 
    "Nova Nazaré", "Nova Olímpia", "Nova Santa Helena", "Nova Ubiratã", "Nova Xavantiva", 
    "Novo Horizonte do Norte", "Novo Mundo", "Novo Santo Antônio", "Novo São Joaquim", 
    "Paranaíta", "Paranatinga", "Pedra Preta", "Peixoto de Azevedo", "Planalto da Serra", 
    "Poconé", "Pontal do Araguaia", "Ponte Branca", "Pontes e Lacerda", "Porto Alegre do Norte", 
    "Porto dos Gaúchos", "Porto Esperidião", "Porto Estrela", "Poxoréu", "Primavera do Leste", 
    "Querência", "Reserva do Cabaçal", "Ribeirão Cascalheira", "Ribeirãozinho", "Rio Branco", 
    "Rondonópolis", "Rosário Oeste", "Salto do Céu", "Santa Carmem", "Santa Cruz do Xingu", 
    "Santa Rita do Trivelato", "Santa Terezinha", "Santo Antônio do Leste", 
    "Santo Antônio do Leverger", "Santo Afonso", "São Félix do Araguaia", "São José do Povo", 
    "São José do Rio Claro", "São José do Xingu", "São José dos Quatro Marcos", 
    "São Pedro da Cipa", "Sapezal", "Serra Nova Dourada", "Sinop", "Sorriso", 
    "Tabaporã", "Tangará da Serra", "Tapurah", "Terra Nova do Norte", "Tesouro", 
    "Torixoréu", "União do Sul", "Vale de São Domingos", "Várzea Grande", "Vera", 
    "Vila Bela da Santíssima Trindade", "Vila Rica"
]

cidade_ref = st.selectbox("Selecione sua Cidade (Mato Grosso):", ["Selecione..."] + cidades_mt)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Planejado (Custeio)**")
    prod_esperada = st.number_input("Produtividade Esperada (sc/ha):", value=0.0, step=0.1, key="p_esp")
    preco_esperado = st.number_input("Preço de Venda Esperado (R$):", value=0.0, step=0.1, key="pr_esp")

with col2:
    st.markdown("**Realidade (Colheita)**")
    prod_atual = st.number_input("Produtividade Real (sc/ha):", value=0.0, step=0.1, key="p_real")
    preco_atual = st.number_input("Preço de Mercado Atual (R$):", value=0.0, step=0.1, key="pr_real")

# 2. CÁLCULO FINANCEIRO
receita_planejada = prod_esperada * preco_esperado
receita_atual = prod_atual * preco_atual

if receita_planejada > 0:
    quebra_financeira = (1 - (receita_atual / receita_planejada)) * 100
else:
    quebra_financeira = 0

st.markdown("---")

# 3. DIAGNÓSTICO
if receita_planejada > 0 and receita_atual > 0:
    st.subheader("📊 Resultado da Análise")
    
    if quebra_financeira >= 20:
        st.error(f"🚨 ALTA QUEBRA DETECTADA: {quebra_financeira:.1f}%")
        st.write(f"Sua redução de receita em {cidade_ref} atingiu um patamar crítico para o enquadramento no MCR 2-6-4.")
        
        # Link Direto para o WhatsApp do Dr. Flavio
        numero_whats = "5566996626402"
        mensagem = (f"Olá Dr. Flavio, fiz a análise de quebra de safra para {cidade_ref}. "
                    f"Minha perda financeira foi de {quebra_financeira:.1f}%. "
                    f"Gostaria de orientações sobre a prorrogação.")
        
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
        st.write("O índice atual não preenche, por si só, os requisitos automáticos de prorrogação.")
else:
    st.info("Aguardando preenchimento dos dados para gerar o diagnóstico.")

st.markdown("---")
st.caption("Desenvolvido por Flavio Lemos Gil - Advogado Especialista em Agronegócio.")
