#!/usr/bin/env python3
"""Gera o PDF Capital Blindado — Bezerra Borges Advogados."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

W, H = A4
OUT = os.path.join(os.path.dirname(__file__), "entregaveis", "Capital-Blindado.pdf")

BG = HexColor("#070d0a")
BG2 = HexColor("#0e1a14")
WHITE = white
GRAY = HexColor("#999999")
GRAY_LIGHT = HexColor("#cccccc")
GRAY_DIM = HexColor("#555555")
LINE = HexColor("#1a2e1f")

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

# ── Styles ──

def style_body():
    return ParagraphStyle("body", fontName=FONT, fontSize=10, leading=16,
                          textColor=GRAY_LIGHT, alignment=TA_JUSTIFY, spaceAfter=8)

def style_body_sm():
    return ParagraphStyle("bodysm", fontName=FONT, fontSize=9, leading=14,
                          textColor=GRAY, alignment=TA_LEFT, spaceAfter=6)

def style_h2():
    return ParagraphStyle("h2", fontName=FONT_B, fontSize=13, leading=18,
                          textColor=WHITE, spaceAfter=10, spaceBefore=18)

def style_h3():
    return ParagraphStyle("h3", fontName=FONT_B, fontSize=11, leading=15,
                          textColor=HexColor("#d0d0d0"), spaceAfter=8, spaceBefore=14)

def style_bullet():
    return ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=15,
                          textColor=GRAY_LIGHT, leftIndent=16, bulletIndent=0,
                          spaceAfter=4, alignment=TA_LEFT)

def style_table_header():
    return ParagraphStyle("th", fontName=FONT_B, fontSize=9, leading=12,
                          textColor=WHITE, alignment=TA_LEFT)

def style_table_cell():
    return ParagraphStyle("td", fontName=FONT, fontSize=9, leading=12,
                          textColor=GRAY_LIGHT, alignment=TA_LEFT)


class PDFBuilder:
    def __init__(self, filename):
        self.c = canvas.Canvas(filename, pagesize=A4)
        self.c.setTitle("Capital Blindado - Bezerra Borges Advogados")
        self.c.setAuthor("Bezerra Borges Advogados")
        self.page_num = 0

    def bg(self):
        self.c.setFillColor(BG)
        self.c.rect(0, 0, W, H, fill=1, stroke=0)

    def footer(self, text="Bezerra Borges Advogados"):
        self.c.setFont(FONT, 7)
        self.c.setFillColor(GRAY_DIM)
        self.c.drawString(2*cm, 1.2*cm, text)
        self.c.drawRightString(W - 2*cm, 1.2*cm, str(self.page_num))

    def new_page(self, with_footer=True):
        if self.page_num > 0:
            self.c.showPage()
        self.page_num += 1
        self.bg()
        if with_footer and self.page_num > 1:
            self.footer()

    def draw_line(self, y, margin=2*cm):
        self.c.setStrokeColor(LINE)
        self.c.setLineWidth(0.5)
        self.c.line(margin, y, W - margin, y)

    def chapter_header(self, number, title):
        self.new_page()
        y = H - 4*cm
        self.c.setFont(FONT, 10)
        self.c.setFillColor(GRAY_DIM)
        self.c.drawString(2*cm, y + 20, f"CAPITULO {number}")
        self.c.setFont(FONT_B, 22)
        self.c.setFillColor(WHITE)
        self.c.drawString(2*cm, y - 10, title)
        self.draw_line(y - 30)
        return y - 50

    def render_flow(self, flowables, y_start, x=2*cm, width=None):
        if width is None:
            width = W - 4*cm
        y = y_start
        for f in flowables:
            fw, fh = f.wrap(width, 9999)
            if y - fh < 2.5*cm:
                self.new_page()
                y = H - 3*cm
            f.drawOn(self.c, x, y - fh)
            y -= fh
        return y

    def save(self):
        self.c.save()


def build():
    pdf = PDFBuilder(OUT)

    # ── CAPA ──
    pdf.new_page(with_footer=False)
    pdf.page_num = 0
    y = H / 2 + 3*cm
    pdf.c.setFont(FONT, 9)
    pdf.c.setFillColor(GRAY_DIM)
    pdf.c.drawCentredString(W/2, y + 40, "BEZERRA BORGES ADVOGADOS")

    pdf.c.setFont(FONT_B, 32)
    pdf.c.setFillColor(WHITE)
    pdf.c.drawCentredString(W/2, y - 10, "CAPITAL BLINDADO")

    pdf.c.setFont(FONT, 12)
    pdf.c.setFillColor(GRAY)
    pdf.c.drawCentredString(W/2, y - 40, "Guia pratico para estruturacao")
    pdf.c.drawCentredString(W/2, y - 56, "internacional de patrimonio")

    pdf.draw_line(y - 90)

    pdf.c.setFont(FONT, 9)
    pdf.c.setFillColor(GRAY_DIM)
    pdf.c.drawCentredString(W/2, y - 115, "bezerraborges.com.br")

    # ── SUMARIO ──
    pdf.new_page()
    y = H - 4*cm
    pdf.c.setFont(FONT_B, 18)
    pdf.c.setFillColor(WHITE)
    pdf.c.drawString(2*cm, y, "SUMARIO")
    pdf.draw_line(y - 15)
    y -= 40

    toc = [
        ("01", "Por que internacionalizar seu patrimonio"),
        ("02", "LLC nos EUA"),
        ("03", "Holding Internacional: Portugal e Malta"),
        ("04", "Trust e Fundacao Privada"),
        ("05", "Offshore no Caribe"),
        ("06", "Obrigacoes legais no Brasil"),
        ("07", "Como escolher a estrutura certa"),
        ("08", "20 perguntas para o seu advogado"),
    ]
    for num, title in toc:
        pdf.c.setFont(FONT, 10)
        pdf.c.setFillColor(GRAY_DIM)
        pdf.c.drawString(2*cm, y, num)
        pdf.c.setFillColor(GRAY_LIGHT)
        pdf.c.drawString(3.2*cm, y, title)
        y -= 22

    # ────────────────────────────────────────
    # CAP 1
    # ────────────────────────────────────────
    y = pdf.chapter_header("01", "Por que internacionalizar")

    flow = [
        Paragraph("CPF milionario descoberto", style_h2()),
        Paragraph(
            "A maioria dos empresarios brasileiros com patrimonio entre R$ 2M e R$ 30M esta numa situacao "
            "simples de descrever: CPF milionario, totalmente descoberto. Tudo que construiram esta vinculado "
            "a um unico numero, em uma unica jurisdicao, sujeito a um unico sistema juridico.", style_body()),
        Paragraph(
            "Isso significa que uma acao trabalhista, uma execucao fiscal, um inventario ou um divorcio "
            "pode atingir a totalidade do patrimonio de uma so vez. Nao importa se voce construiu ao longo "
            "de 20 anos — o sistema juridico brasileiro trata tudo como uma massa unica.", style_body()),

        Paragraph("Exposicoes reais", style_h2()),
        Paragraph("<bullet>&bull;</bullet> <b>Trabalhista:</b> desconsideracao da personalidade juridica atinge bens pessoais do socio", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Fiscal:</b> execucao fiscal pode bloquear contas, imoveis e participacoes", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Inventario:</b> sem planejamento, empresa para. ITCMD de ate 8%. Herdeiros brigam.", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Divorcio:</b> regime de comunhao parcial inclui tudo adquirido apos casamento", style_bullet()),

        Paragraph("O que muda com uma camada internacional", style_h2()),
        Paragraph(
            "Quando voce cria uma estrutura juridica em outra jurisdicao — uma LLC, uma Holding, um Trust — "
            "voce separa seu patrimonio do seu CPF. Os ativos passam a ser titularidade de uma pessoa juridica "
            "estrangeira, sujeita a outro ordenamento juridico. Isso nao e ilegal. E planejamento.", style_body()),
        Paragraph(
            "A camada internacional cria segregacao patrimonial, otimizacao tributaria licita e, em muitos "
            "casos, facilita a sucessao — eliminando inventario, ITCMD e burocracia.", style_body()),

        Paragraph("Para quem faz sentido", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Patrimonio acima de R$ 500 mil (imoveis + investimentos + empresa)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Renda mensal acima de R$ 30 mil", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Empresario com exposicao a processos trabalhistas ou fiscais", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Quem recebe ou pretende receber em moeda estrangeira", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Quem quer planejar sucessao sem inventario", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 2
    # ────────────────────────────────────────
    y = pdf.chapter_header("02", "LLC nos EUA")

    flow = [
        Paragraph("Wyoming — Preferencia para brasileiros", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Zero imposto estadual de renda (State Income Tax = 0%)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Charging Order Protection: credores nao acessam ativos da LLC", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Sem obrigacao de registrar membros publicamente (anonimato)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Sem minimo de capital. Custo total: US$ 400-800", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Prazo: 3-7 dias uteis, 100% remoto", style_bullet()),

        Paragraph("Delaware — Preferencia para startups", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Jurisprudencia mais desenvolvida para empresas nos EUA", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Court of Chancery: tribunal especializado em direito societario", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Preferido por VCs e investidores americanos (C-Corp)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Custo: US$ 500-1.200. Prazo: 3-10 dias uteis", style_bullet()),

        Paragraph("New Mexico — Anonimato maximo", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Nao exige publicacao de nome de membros", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Sem renovacao anual obrigatoria", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Uma das LLCs mais baratas: US$ 200-500", style_bullet()),

        Paragraph("Single-Member LLC como pass-through", style_h2()),
        Paragraph(
            "Para brasileiros nao-residentes nos EUA, a Single-Member LLC e tratada como entidade "
            "desconsiderada (disregarded entity) pelo IRS. Os lucros passam direto para o socio sem "
            "tributacao corporativa americana — desde que a renda nao seja efetivamente conectada aos EUA (ECI).", style_body()),

        Paragraph("Processo de abertura", style_h2()),
        Paragraph("<bullet>&bull;</bullet> 1. Protocolar Articles of Organization no estado escolhido", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 2. Contratar Registered Agent (US$ 50-150/ano)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 3. Obter EIN (Employer Identification Number) junto ao IRS", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 4. Abrir conta bancaria: Mercury, Relay ou Wise Business", style_bullet()),

        Paragraph("Obrigacoes anuais", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Form 5472: declaracao obrigatoria para LLC com socio estrangeiro", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> FinCEN FBAR: se conta bancaria americana com saldo > US$ 10.000", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Renovacao anual no estado (exceto New Mexico)", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 3
    # ────────────────────────────────────────
    y = pdf.chapter_header("03", "Holding Internacional")

    flow = [
        Paragraph("Portugal — Tratado com o Brasil", style_h2()),
        Paragraph(
            "Portugal tem tratado contra bitributacao com o Brasil, o que permite consolidar ativos "
            "em uma Holding portuguesa sem pagar imposto duas vezes. A Holding funciona como uma camada "
            "de protecao entre o empresario e seus ativos — credores brasileiros nao alcancam bens "
            "titularizados por uma pessoa juridica portuguesa.", style_body()),
        Paragraph("<bullet>&bull;</bullet> Protecao contra credores via segregacao patrimonial", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Consolidacao de investimentos e participacoes", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Facilitacao de sucessao (sem ITCMD)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Custo setup: EUR 3.000-8.000 + manutencao anual", style_bullet()),

        Paragraph("Malta — 5% de imposto efetivo", style_h2()),
        Paragraph(
            "Malta cobra 35% de imposto corporativo nominal, mas possui um sistema de reembolso para "
            "socios estrangeiros: ao distribuir dividendos, o socio solicita devolucao de 6/7 do imposto "
            "pago pela empresa. Resultado: carga efetiva de 5% sobre o lucro.", style_body()),
        Paragraph("<bullet>&bull;</bullet> Membro da Uniao Europeia: acesso ao mercado unico", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Malta Holding: participation exemption para dividendos recebidos de subsidiarias", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Framework cripto avancado (VFA Act): licenca europeia para exchanges e wallets", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Custo setup: US$ 2.000-5.000. Manutencao: US$ 1.500-3.000/ano", style_bullet()),

        Paragraph("Quando usar cada uma", style_h2()),
        Paragraph("<bullet>&bull;</bullet> <b>Portugal:</b> foco em protecao patrimonial e sucessao, relacao com Brasil", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Malta:</b> foco em eficiencia tributaria, acesso europeu, cripto", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 4
    # ────────────────────────────────────────
    y = pdf.chapter_header("04", "Trust e Fundacao Privada")

    flow = [
        Paragraph("O que e um Trust", style_h2()),
        Paragraph(
            "Um Trust e uma estrutura juridica onde o Settlor (criador) transfere ativos para um Trustee "
            "(gestor), que os administra em beneficio dos Beneficiarios. O patrimonio deixa de pertencer "
            "ao Settlor — ele sai do seu nome, do seu CPF, da sua declaracao de bens.", style_body()),
        Paragraph("<bullet>&bull;</bullet> <b>Settlor:</b> quem cria o Trust e transfere os ativos", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Trustee:</b> quem administra os ativos (pode ser uma empresa fiduciaria)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Beneficiarios:</b> quem recebe os beneficios (pode ser o proprio Settlor, filhos, etc.)", style_bullet()),

        Paragraph("Trust vs Fundacao Privada", style_h2()),
        Paragraph(
            "O Trust nao tem personalidade juridica — e uma relacao contratual. A Fundacao Privada tem "
            "personalidade juridica propria e pode deter ativos em nome proprio. Na pratica, a Fundacao "
            "oferece mais controle ao fundador, enquanto o Trust oferece mais separacao.", style_body()),

        Paragraph("Jersey / Cayman — Trust Internacional", style_h2()),
        Paragraph(
            "Ideal para planejamento sucessorio. O Trust em Jersey ou Cayman permite transmitir patrimonio "
            "entre geracoes sem inventario, sem ITCMD, com regras claras definidas pelo Settlor. "
            "Cayman garante zero imposto por lei ate 2036.", style_body()),

        Paragraph("Liechtenstein — Fundacao Privada", style_h2()),
        Paragraph(
            "A Fundacao Privada (Stiftung) em Liechtenstein oferece o mais alto nivel de segregacao "
            "patrimonial da Europa. O patrimonio passa a pertencer a Fundacao — sai completamente do nome "
            "e do CPF do fundador. Regulacao solida, sigilo bancario, estabilidade juridica.", style_body()),

        Paragraph("Panama — Foundation", style_h2()),
        Paragraph(
            "A Private Interest Foundation panamenha combina elementos de Trust e empresa. Tem personalidade "
            "juridica, pode deter ativos, e oferece flexibilidade operacional com privacidade.", style_body()),

        Paragraph("Custos e perfil", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Setup: US$ 5.000-25.000 dependendo da jurisdicao e complexidade", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Manutencao anual: US$ 2.000-8.000", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Para quem: patrimonio acima de R$ 10 milhoes", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 5
    # ────────────────────────────────────────
    y = pdf.chapter_header("05", "Offshore no Caribe")

    flow = [
        Paragraph("Nevis LLC — Protecao maxima", style_h2()),
        Paragraph(
            "Nevis tem a Charging Order Protection mais forte do mundo para LLCs. Para processar o socio "
            "de uma Nevis LLC, o credor precisa depositar US$ 25.000 antecipados e provar fraude. "
            "O prazo de prescricao para fraude e de apenas 3 anos.", style_body()),
        Paragraph("<bullet>&bull;</bullet> Zero imposto sobre renda, dividendos e ganho de capital", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Custo: US$ 1.500-3.000 (setup) + US$ 800-1.200/ano", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Abertura 100% remota em 3-5 dias", style_bullet()),

        Paragraph("BVI Business Company — Padrao global", style_h2()),
        Paragraph(
            "As Ilhas Virgens Britanicas sao a jurisdicao offshore mais usada no mundo, com mais de "
            "500.000 empresas ativas. Direito ingles solido e previsivel. Sem diretores locais obrigatorios.", style_body()),
        Paragraph("<bullet>&bull;</bullet> Zero imposto. Sem capital minimo", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Custo: US$ 1.200-2.500 (setup) + US$ 700-1.000/ano", style_bullet()),

        Paragraph("Cayman Islands — Fundos e Family Office", style_h2()),
        Paragraph(
            "Jurisdicao padrao para hedge funds, private equity e family office. Zero imposto sobre renda, "
            "dividendos e ganho de capital — garantido por lei ate 2036. Regulacao pela CIMA "
            "(Cayman Islands Monetary Authority). Aceito por todos os bancos e investidores institucionais.", style_body()),
        Paragraph("<bullet>&bull;</bullet> Custo: US$ 3.000-8.000 (setup) + US$ 2.000-4.000/ano", style_bullet()),

        Paragraph("Panama — Sociedad Anonima + Foundation", style_h2()),
        Paragraph(
            "Zero imposto sobre renda obtida fora do Panama. A combinacao de Sociedad Anonima com "
            "Foundation cria uma estrutura de duas camadas: operacional + patrimonial.", style_body()),

        Paragraph("Contas bancarias", style_h2()),
        Paragraph("<bullet>&bull;</bullet> FirstCaribbean International Bank: moderado, aceita offshore", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Cayman National Bank: robusto, ideal para Cayman entities", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Neobanks (Wise, Mercury, Airwallex): alternativa rapida e online", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Suica/Liechtenstein: para volumes acima de US$ 500k", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 6
    # ────────────────────────────────────────
    y = pdf.chapter_header("06", "Obrigacoes legais no Brasil")

    flow = [
        Paragraph("Lei 14.754/2023", style_h2()),
        Paragraph(
            "A Lei 14.754, de dezembro de 2023, mudou profundamente a tributacao de brasileiros com "
            "ativos no exterior. As principais alteracoes:", style_body()),
        Paragraph("<bullet>&bull;</bullet> <b>Fim do diferimento:</b> lucros de controladas no exterior passam a ser tributados anualmente, mesmo sem distribuicao", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Regime de transparencia:</b> o resultado da offshore e apurado como se fosse do socio pessoa fisica", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Come-cotas:</b> fundos exclusivos passam a ter come-cotas semestral", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Trusts:</b> tributacao na distribuicao ao beneficiario ou na morte do Settlor", style_bullet()),

        Paragraph("CBE — Capitais Brasileiros no Exterior", style_h2()),
        Paragraph(
            "A declaracao de Capitais Brasileiros no Exterior (CBE) e obrigatoria junto ao Banco Central "
            "para residentes fiscais no Brasil com ativos no exterior.", style_body()),
        Paragraph("<bullet>&bull;</bullet> <b>CBE anual:</b> obrigatoria se ativos no exterior >= US$ 1 milhao (data-base 31/12)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>CBE trimestral:</b> obrigatoria se ativos >= US$ 100 milhoes", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Inclui: depositos, investimentos, participacoes, imoveis, creditos no exterior", style_bullet()),

        Paragraph("DIRPF — Declaracao de bens", style_h2()),
        Paragraph(
            "Todos os bens e direitos no exterior devem ser declarados na ficha de Bens e Direitos da "
            "DIRPF, convertidos em reais pela cotacao do dolar do Banco Central na data de aquisicao.", style_body()),

        Paragraph("Saida definitiva", style_h2()),
        Paragraph(
            "Quem deixa de ser residente fiscal no Brasil precisa comunicar a Saida Definitiva ao governo "
            "em ate 12 meses. Envolve: Comunicacao de Saida Definitiva (CSD) e Declaracao de Saida "
            "Definitiva do Pais (DSDP). Apos a saida, nao ha mais obrigacao de CBE, DIRPF ou tributacao "
            "sobre renda mundial.", style_body()),

        Paragraph("Riscos de nao declarar", style_h2()),
        Paragraph("<bullet>&bull;</bullet> Multa de ate 5% ao mes sobre o valor nao declarado (CBE)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Multa de 75% a 150% sobre o imposto nao pago (DIRPF)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Processo criminal por evasao de divisas (Lei 7.492/86)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Processo criminal por sonegacao fiscal (Lei 8.137/90)", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 7
    # ────────────────────────────────────────
    y = pdf.chapter_header("07", "Como escolher a estrutura")

    flow = [
        Paragraph("Matriz patrimonio x objetivo", style_h2()),
        Paragraph(
            "A estrutura certa depende de duas variaveis: o tamanho do seu patrimonio e o seu "
            "objetivo principal. A matriz abaixo resume as recomendacoes:", style_body()),

        Paragraph("Ate R$ 500 mil", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Qualquer objetivo: LLC nos EUA (Wyoming ou Delaware)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Custo baixo, abertura rapida, segregacao patrimonial basica", style_bullet()),

        Paragraph("R$ 500 mil a R$ 2 milhoes", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Protecao: Holding em Portugal (tratado com Brasil)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Sucessao: Holding Portugal + estudo de Trust", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Tributario: LLC nos EUA (pass-through)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Exterior: LLC nos EUA (operacao + conta bancaria)", style_bullet()),

        Paragraph("R$ 2 milhoes a R$ 10 milhoes", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Protecao: Holding Internacional (Portugal)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Sucessao: Holding Internacional + Trust (Portugal/Cayman)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Tributario: Holding Internacional (Portugal ou Malta)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Exterior: Holding Internacional + LLC EUA (Portugal + Delaware)", style_bullet()),

        Paragraph("Acima de R$ 10 milhoes", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Protecao: Fundacao Privada (Liechtenstein)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Sucessao: Trust Internacional (Jersey/Cayman)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Tributario: Trust + Holding (Cayman + Malta)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Exterior: Trust Internacional (Cayman)", style_bullet()),

        Paragraph("Comparativo de custos", style_h2()),
        Paragraph("<bullet>&bull;</bullet> LLC EUA: US$ 400-1.200 (setup) + US$ 200-500/ano", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Holding Portugal: EUR 3.000-8.000 (setup) + EUR 1.500-3.000/ano", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Holding Malta: US$ 2.000-5.000 (setup) + US$ 1.500-3.000/ano", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Offshore Caribe: US$ 1.200-8.000 (setup) + US$ 700-4.000/ano", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Trust/Fundacao: US$ 5.000-25.000 (setup) + US$ 2.000-8.000/ano", style_bullet()),

        Paragraph("Comparativo de tempo", style_h2()),
        Paragraph("<bullet>&bull;</bullet> LLC EUA: 3-10 dias", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Holding Portugal/Malta: 5-20 dias", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Offshore Caribe: 3-15 dias", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Trust/Fundacao: 15-45 dias", style_bullet()),

        Paragraph("Quando combinar estruturas", style_h2()),
        Paragraph(
            "A partir de R$ 2 milhoes de patrimonio, a combinacao de estruturas passa a fazer sentido. "
            "As combinacoes mais comuns:", style_body()),
        Paragraph("<bullet>&bull;</bullet> <b>Holding + Trust:</b> protecao + sucessao (a Holding detem os ativos, o Trust controla a Holding)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Holding + LLC:</b> consolidacao + operacao (a Holding em Portugal, a LLC nos EUA para operar)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> <b>Trust + Offshore:</b> sucessao + privacidade (Trust em Jersey sobre empresa em Nevis/BVI)", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ────────────────────────────────────────
    # CAP 8
    # ────────────────────────────────────────
    y = pdf.chapter_header("08", "20 perguntas para o seu advogado")

    flow = [
        Paragraph(
            "Antes de contratar qualquer estruturacao internacional, faca estas perguntas. "
            "Se o profissional nao souber responder com clareza, reconsidere.", style_body()),

        Paragraph("Custos", style_h2()),
        Paragraph("<bullet>&bull;</bullet> 1. Qual o custo total de abertura, incluindo taxas governamentais e honorarios?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 2. Qual o custo anual de manutencao (contabilidade, registered agent, compliance)?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 3. Existem custos ocultos ou variaveis que podem surgir?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 4. Em quantos meses a economia tributaria paga o investimento?", style_bullet()),

        Paragraph("Prazo e processo", style_h2()),
        Paragraph("<bullet>&bull;</bullet> 5. Qual o prazo real de abertura, do inicio ao fim?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 6. Preciso viajar ou tudo e feito remotamente?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 7. Quais documentos preciso providenciar?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 8. Quem sera o responsavel operacional pelo meu caso?", style_bullet()),

        Paragraph("Obrigacoes", style_h2()),
        Paragraph("<bullet>&bull;</bullet> 9. Quais declaracoes anuais serei obrigado a fazer no Brasil?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 10. E no pais da estrutura, quais obrigacoes terei?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 11. Como fica minha situacao com a Receita Federal brasileira?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 12. Preciso declarar CBE? Em qual modalidade?", style_bullet()),

        Paragraph("Riscos", style_h2()),
        Paragraph("<bullet>&bull;</bullet> 13. Quais os riscos juridicos dessa estrutura no Brasil?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 14. A Lei 14.754/2023 afeta essa estrutura? Como?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 15. O que acontece se eu nao declarar corretamente?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 16. Existe risco de a estrutura ser desconsiderada pela Receita?", style_bullet()),

        Paragraph("Manutencao e futuro", style_h2()),
        Paragraph("<bullet>&bull;</bullet> 17. Quem faz a contabilidade da estrutura internacional?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 18. Como funciona a movimentacao de recursos entre Brasil e a estrutura?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 19. Se eu quiser encerrar a estrutura, qual o processo e custo?", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> 20. Voce tem experiencia comprovada nessa jurisdicao especifica?", style_bullet()),

        Paragraph("Checklist de documentos por estrutura", style_h2()),

        Paragraph("LLC nos EUA", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Passaporte valido", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Comprovante de endereco residencial", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Descricao da atividade da empresa", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Operating Agreement assinado", style_bullet()),

        Paragraph("Holding Internacional", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Passaporte valido + traducao juramentada", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Comprovante de endereco apostilado", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Certidao de nascimento/casamento apostilada", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Declaracao de IR do ultimo exercicio", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Contrato social da empresa brasileira (se aplicavel)", style_bullet()),

        Paragraph("Trust / Fundacao", style_h3()),
        Paragraph("<bullet>&bull;</bullet> Todos os documentos acima", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Letter of Wishes (carta de desejos do Settlor/Fundador)", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Identificacao completa dos beneficiarios", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Inventario detalhado dos ativos a serem transferidos", style_bullet()),
        Paragraph("<bullet>&bull;</bullet> Due diligence bancaria (KYC/AML) para todas as partes", style_bullet()),
    ]
    y = pdf.render_flow(flow, y)

    # ── CONTRACAPA ──
    pdf.new_page(with_footer=False)
    y = H / 2 + 1*cm

    pdf.c.setFont(FONT_B, 16)
    pdf.c.setFillColor(WHITE)
    pdf.c.drawCentredString(W/2, y, "BEZERRA BORGES ADVOGADOS")

    pdf.c.setFont(FONT, 10)
    pdf.c.setFillColor(GRAY)
    pdf.c.drawCentredString(W/2, y - 30, "12+ paises  /  500+ estruturas ativas  /  desde 2017")

    pdf.draw_line(y - 55)

    pdf.c.setFont(FONT, 9)
    pdf.c.setFillColor(GRAY_DIM)
    pdf.c.drawCentredString(W/2, y - 80, "bezerraborges.com.br")

    pdf.c.setFont(FONT, 8)
    pdf.c.setFillColor(GRAY_DIM)
    pdf.c.drawCentredString(W/2, y - 120, "Material educacional. Nao substitui consultoria juridica ou tributaria individualizada.")
    pdf.c.drawCentredString(W/2, y - 134, "As informacoes contidas neste guia sao de carater geral e podem nao se aplicar")
    pdf.c.drawCentredString(W/2, y - 148, "ao seu caso especifico. Consulte um profissional habilitado antes de tomar decisoes.")

    pdf.save()
    print(f"PDF gerado: {OUT}")


if __name__ == "__main__":
    build()
