"""
Script de população da base de conhecimento com dados do organograma da TIC.
Usa diretamente as funções de ingest.py para popular SQLite + Vector Store.

Uso:
    python populate_organograma.py

Certifique-se de rodar a partir da raiz do projeto (onde ficam as pastas agent/ e data/).
"""

from agent.ingest import ingest_validated_answer

# ==============================================================================
# DADOS DO ORGANOGRAMA - TIC / ADMINISTRAÇÃO CENTRAL
# ==============================================================================

EQUIPE = [
    # matricula, nome, admissao, nascimento, idade, ccusto, setor, funcao
    ("0027391", "ADEMIR TADEU SILVA DAS CHAGAS",       "21/07/2023", "22/11/1984", 39, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "COORDENADOR DE SISTEMAS"),
    ("0007708", "ALEXANDRE LEITE SANTOS",              "12/08/2008", "11/11/1980", 43, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - PROCESSOS"),
    ("0018634", "ANDRE ANDRADE PEREIRA",               "15/01/2018", "05/04/1979", 44, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ANALISTA DE SUPORTE JR"),
    ("0005403", "ANDRE LUIZ SANTOS SENA",              "24/07/2006", "06/12/1977", 45, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0001386", "ANTONIO MANOEL DA SILVA FILHO",       "01/06/1999", "17/04/1964", 59, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "TECNICO II - TIC"),
    ("0025429", "BRUNO BRAGA CERQUEIRA",               "04/04/2022", "01/03/1995", 28, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0022841", "CAMILA CUNHA BORGES",                 "03/08/2020", "14/02/1980", 43, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "SUPERVISOR (A) DE SISTEMAS E APLICACAO DE TI"),
    ("0006896", "CLOVIS MOISES DOS SANTOS",            "21/01/2008", "05/05/1968", 55, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "TECNICO I - TIC"),
    ("0014571", "CRISTIANO MENESES DE FARIAS",         "03/11/2014", "06/07/1986", 37, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0016891", "DANILO ALVES SOUZA",                  "06/03/2017", "17/12/1988", 34, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA SENIOR - PROCESSOS"),
    ("0027573", "DEIVISSON TAUA SANTOS E SANTOS",      "05/09/2023", "11/05/1994", 29, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0013835", "DIEGO DE ALMEIDA FRANCA",             "22/04/2014", "10/02/1987", 36, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "SUPERVISOR(A) DE INFRAESTRUTURA E SEGURANCA"),
    ("0023074", "EDER CERQUEIRA SANTOS",               "03/11/2020", "03/11/1981", 42, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA PLENO - SISTEMAS"),
    ("0025681", "EDNALDO MONTEIRO NUNES",              "06/06/2022", "03/06/1983", 40, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0022641", "ELAINE LEITE MARQUES",                "01/06/2020", "26/03/1991", 32, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - SISTEMAS"),
    ("0027814", "ELIZEU VALVERDE DA SILVA NETO",       "07/11/2023", "29/12/1998", 24, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0021563", "FELIPE MARCELO SANTOS LIMA",          "15/07/2019", "08/09/1988", 35, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0025258", "GERALDO ANTONIO DA SILVA JUNIOR",     "01/02/2022", "17/08/1988", 35, "12.132", "COORDENACAO DE ANALYTICS, PROCESSOS E INOVACOES", "ANALISTA PLENO DE BI"),
    ("0024724", "HUNALD PINA DE PAIVA NETO",           "09/08/2021", "12/06/1976", 47, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ANALISTA DE SUPORTE PLENO I"),
    ("0016359", "ICARO SOUZA ROCHA",                   "06/06/2016", "06/05/1987", 36, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - SISTEMAS"),
    ("0027916", "ISABELLE FRANCINE SANTANA DA SILVA",  "05/12/2023", "05/06/1990", 33, "12.132", "COORDENACAO DE ANALYTICS, PROCESSOS E INOVACOES", "ANALISTA DE PROJETOS PLENO"),
    ("0024710", "ISAQUE SOUZA DA SILVA",               "09/08/2021", "02/01/2000", 23, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0023629", "JAVANY JOSE DOS SANTOS PEIXOTO JUNIOR","01/03/2021","30/09/1989", 34, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0022006", "JOSE EDUARDO ALVES DOS SANTOS",       "11/11/2019", "17/11/1961", 62, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ANALISTA DE INFRA-ESTRUTURA PLENO"),
    ("0026117", "JOSE LUIS BREIS GARCIA LINS CALDAS",  "03/10/2022", "02/07/1986", 37, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - SISTEMAS"),
    ("0092120", "JOSE ROBERTO SOUZA CARDOSO",          "19/09/2022", "23/10/2002", 21, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ESTAGIARIO"),
    ("0005424", "JOSUE CORTES SILVA",                  "01/08/2006", "22/03/1984", 39, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA SENIOR - PROCESSOS"),
    ("0026292", "JULIANO SOUZA ARMENTANO",             "21/11/2022", "29/07/1978", 45, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA PLENO - SISTEMAS"),
    ("0016364", "KARLA LIMA ALELUIA",                  "06/06/2016", "19/07/1975", 48, "12.132", "COORDENACAO DE ANALYTICS, PROCESSOS E INOVACOES", "COORD. DE ANALYTICS PROCESSOS E INOVACAO"),
    ("0025016", "KAROLINE OLIVEIRA SILVA",             "01/11/2021", "27/02/1996", 27, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - PROCESSOS"),
    ("0092204", "LARISSA DE CARVALHO ROCHA DA SILVA",  "05/12/2023", "18/08/1994", 29, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ESTAGIARIO"),
    ("0027351", "LEIA ATAIDES DOS SANTOS",             "18/07/2023", "15/12/1989", 33, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - SISTEMAS"),
    ("0018415", "LILIA OLIVEIRA DA SILVA",             "17/10/2017", "16/01/1982", 41, "12.130", "GERENCIA DE TECNOLOGIA DA INFORMACAO E COMUNICACAO","ANALISTA ADMINISTRATIVO I"),
    ("0012461", "LIVIA MACHADO DE SOUZA",              "16/04/2013", "03/02/1982", 41, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - PROCESSOS"),
    ("0026034", "LUCAS OLIVEIRA DE ALMEIDA",           "05/09/2022", "12/01/1996", 27, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA DE SUPORTE JR"),
    ("0013543", "LUIS EDUARDO CRUZ SANTOS DE SOUZA",   "10/02/2014", "15/12/1986", 36, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ANALISTA DE INFRA-ESTRUTURA PLENO"),
    ("0092160", "MARCUS VINICIUS DA SILVA SANTOS",     "05/06/2023", "03/01/2004", 19, "12.136", "SUPERVISAO DE SERVICE DESK",                      "ESTAGIARIO"),
    ("0025948", "MARIO BATISTA DOS REIS NETO",         "15/08/2022", "23/09/1980", 43, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0026864", "MATHEUS SOUZA MOREIRA",               "17/04/2023", "06/07/1994", 29, "12.132", "COORDENACAO DE ANALYTICS, PROCESSOS E INOVACOES", "ANALISTA DE BUSINESS INTELIGENCE JR"),
    ("0024978", "MAURICIO REIS MATOS",                 "18/10/2021", "28/03/1980", 43, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ANALISTA SENIOR INFRA-ESTRUTURA"),
    ("0001339", "MONICA MARIA BEZERRA DA SILVA",       "05/04/1999", "18/03/1965", 58, "12.180", "DIRETORIA CORPORATIVA TEC OPERACOES",             "DIRETOR (A) CORP. DE TEC. E OPERACOES"),
    ("0015767", "NIVALDO RISUTTI DOS SANTOS JUNIOR",   "19/10/2015", "15/03/1981", 42, "12.136", "SUPERVISAO DE SERVICE DESK",                      "SUPERVISOR(A) DO SERVICE DESK"),
    ("0005628", "RAFAEL DO SACRAMENTO SANTOS",         "02/10/2006", "19/01/1985", 38, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0027510", "RENATO GUEDES DOS REIS SANTOS",       "05/09/2023", "01/10/1991", 32, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO I - TIC"),
    ("0027735", "RINALDO ALEXANDRE DOS SANTOS",        "18/10/2023", "16/12/1972", 50, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA SENIOR - PROCESSOS"),
    ("0006996", "ROBSON SILVA SANTANA",                "05/03/2008", "14/08/1977", 46, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0009720", "RODRIGO DIAS DRUMOND MARTINS",        "19/07/2010", "12/05/1987", 36, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "COORDENADOR (A) DE INFRAESTRUTURA DE TI"),
    ("0027420", "SAVIO DE OLIVEIRA BARBOSA",           "01/08/2023", "24/04/2002", 21, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA JUNIOR - SISTEMAS"),
    ("0016785", "TATYANA CONCEICAO DE SANTANA SOUZA",  "05/12/2016", "08/12/1972", 50, "12.130", "GERENCIA DE TECNOLOGIA DA INFORMACAO E COMUNICACAO","GERENTE DE TECNO DA INFOR E COMUNICACAO"),
    ("0025602", "VAGNER SANTANA DOS SANTOS",           "16/05/2022", "26/09/1989", 34, "12.136", "SUPERVISAO DE SERVICE DESK",                      "TECNICO II - TIC"),
    ("0015233", "VALTERNEY DOS SANTOS ANDRADE",        "11/05/2015", "10/08/1979", 44, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA PLENO - SISTEMAS"),
    ("0009670", "VINICIUS GONCALVES DE LUCENA",        "05/07/2010", "25/07/1987", 36, "12.133", "SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",        "ANALISTA JUNIOR - INFRAESTRUTURA"),
    ("0092139", "VITOR LEVI MENEZES SANTOS",           "05/12/2022", "17/09/2003", 20, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ESTAGIARIO"),
    ("0092100", "VITOR PAIVA LOPES E SILVA ANDRADE",   "04/04/2022", "28/09/2002", 21, "12.136", "SUPERVISAO DE SERVICE DESK",                      "ESTAGIARIO"),
    ("0010911", "WELLINGTON FAVA DOS SANTOS",          "17/10/2011", "21/03/1983", 40, "12.131", "COORDENACAO DE SISTEMAS E APLICACOES",            "ANALISTA SENIOR - PROCESSOS"),
]

# Primeiro nome para referência natural nas queries
def first_name(nome: str) -> str:
    return nome.split()[0].capitalize()

def full_name_title(nome: str) -> str:
    stop = {"DA","DE","DO","DOS","DAS","E","JUNIOR"}
    return " ".join(w.capitalize() if w.upper() not in stop else w.lower() for w in nome.split())


# ==============================================================================
# GERAÇÃO DOS REGISTROS
# ==============================================================================

def build_records() -> list[tuple]:
    records = []

    for mat, nome, admissao, nasc, idade, ccusto, setor, funcao in EQUIPE:
        fn = first_name(nome)
        nome_fmt = full_name_title(nome)

        # --- 1. Quem é / identificação completa ---
        records.append((
            f"Quem é {fn} na TIC?",
            f"{nome_fmt} é {funcao.capitalize()} no setor de {setor.title()}, "
            f"matrícula {mat}, admitido(a) em {admissao}.",
            f"Organograma TIC – {setor}",
            "organograma_tic"
        ))

        # --- 2. Cargo / função ---
        records.append((
            f"Qual a função de {fn} na TIC?",
            f"{nome_fmt} ocupa o cargo de {funcao.capitalize()} no setor {setor.title()} "
            f"(CC {ccusto}).",
            f"Organograma TIC – cargos",
            "organograma_tic"
        ))

        # --- 3. Setor ---
        records.append((
            f"Em qual setor trabalha {fn}?",
            f"{nome_fmt} trabalha no setor de {setor.title()}, centro de custo {ccusto}.",
            f"Organograma TIC – setores",
            "organograma_tic"
        ))

        # --- 4. Matrícula ---
        records.append((
            f"Qual a matrícula de {fn}?",
            f"A matrícula de {nome_fmt} é {mat}.",
            f"Organograma TIC – matrículas",
            "organograma_tic"
        ))

        # --- 5. Data de admissão ---
        records.append((
            f"Quando {fn} foi admitido(a)?",
            f"{nome_fmt} foi admitido(a) em {admissao}.",
            f"Organograma TIC – admissões",
            "organograma_tic"
        ))

    # ==========================================================================
    # REGISTROS COLETIVOS POR SETOR
    # ==========================================================================

    setores: dict[str, list] = {}
    for mat, nome, admissao, nasc, idade, ccusto, setor, funcao in EQUIPE:
        setores.setdefault(setor, []).append((mat, nome, funcao))

    for setor, membros in setores.items():
        nomes_lista = ", ".join(full_name_title(m[1]) for m in membros)
        records.append((
            f"Quem faz parte do setor de {setor.title()}?",
            f"O setor de {setor.title()} é composto por {len(membros)} colaborador(es): {nomes_lista}.",
            f"Organograma TIC – equipe por setor",
            "organograma_tic"
        ))

        # Por cargo dentro do setor
        cargos: dict[str, list] = {}
        for mat, nome, funcao in membros:
            cargos.setdefault(funcao, []).append(full_name_title(nome))
        for cargo, pessoas in cargos.items():
            records.append((
                f"Quem ocupa o cargo de {cargo.capitalize()} no setor de {setor.title()}?",
                f"O cargo de {cargo.capitalize()} no setor de {setor.title()} é ocupado por: "
                f"{', '.join(pessoas)}.",
                f"Organograma TIC – cargos por setor",
                "organograma_tic"
            ))

    # ==========================================================================
    # REGISTROS DE HIERARQUIA / LIDERANÇA
    # ==========================================================================

    liderancas = [
        ("DIRETORIA CORPORATIVA TEC OPERACOES",
         "Mônica Maria Bezerra da Silva",
         "Diretora Corporativa de Tecnologia e Operações",
         "É a maior liderança da área de TIC, respondendo pela Diretoria Corporativa de Tecnologia e Operações."),

        ("GERENCIA DE TECNOLOGIA DA INFORMACAO E COMUNICACAO",
         "Tatyana Conceição de Santana Souza",
         "Gerente de Tecnologia da Informação e Comunicação",
         "Responde à Diretoria e lidera a Gerência de TIC. Colaboradora de apoio administrativo na gerência: Lilia Oliveira da Silva."),

        ("COORDENACAO DE SISTEMAS E APLICACOES",
         "Ademir Tadeu Silva das Chagas",
         "Coordenador de Sistemas",
         "Coordena o time de sistemas e aplicações. A supervisão do setor é de responsabilidade de Camila Cunha Borges (Supervisora de Sistemas e Aplicação de TI)."),

        ("SUPERVISAO DE INFRAESTRUTURA E SEGURANCA",
         "Diego de Almeida França",
         "Supervisor de Infraestrutura e Segurança",
         "Lidera a equipe de infraestrutura. A coordenação de infraestrutura de TI é exercida por Rodrigo Dias Drumond Martins."),

        ("SUPERVISAO DE SERVICE DESK",
         "Nivaldo Risutti dos Santos Junior",
         "Supervisor do Service Desk",
         "Lidera a equipe de atendimento do Service Desk (CC 12.136)."),

        ("COORDENACAO DE ANALYTICS, PROCESSOS E INOVACOES",
         "Karla Lima Aleluia",
         "Coordenadora de Analytics, Processos e Inovação",
         "Lidera o time de analytics, BI e inovação."),
    ]

    for setor, lider, cargo, descricao in liderancas:
        records.append((
            f"Quem lidera o setor de {setor.title()}?",
            f"{lider} é o(a) responsável pelo setor de {setor.title()}, "
            f"ocupando o cargo de {cargo}. {descricao}",
            f"Organograma TIC – lideranças",
            "organograma_tic"
        ))

    # ==========================================================================
    # REGISTROS GERAIS / VISÃO DO ORGANOGRAMA
    # ==========================================================================

    records.append((
        "Como é a estrutura hierárquica da TIC?",
        "A TIC está organizada da seguinte forma: "
        "(1) Diretoria Corporativa de Tecnologia e Operações – Mônica Maria Bezerra da Silva. "
        "(2) Gerência de TIC – Tatyana Conceição de Santana Souza. "
        "(3) Coordenação de Sistemas e Aplicações – Ademir Tadeu Silva das Chagas. "
        "(4) Coordenação de Analytics, Processos e Inovações – Karla Lima Aleluia. "
        "(5) Supervisão de Infraestrutura e Segurança – Diego de Almeida França. "
        "(6) Supervisão de Service Desk – Nivaldo Risutti dos Santos Junior.",
        "Organograma TIC – visão geral",
        "organograma_tic"
    ))

    records.append((
        "Quantos colaboradores tem a TIC?",
        f"A equipe de TIC da Administração Central conta com {len(EQUIPE)} colaboradores, "
        "distribuídos nos setores: Diretoria, Gerência de TIC, Coordenação de Sistemas, "
        "Coordenação de Analytics, Supervisão de Infraestrutura e Service Desk.",
        "Organograma TIC – estatísticas",
        "organograma_tic"
    ))

    records.append((
        "Quem são os estagiários da TIC?",
        "Os estagiários da TIC são: "
        "Jose Roberto Souza Cardoso (Infraestrutura), "
        "Marcus Vinicius da Silva Santos (Service Desk), "
        "Vitor Levi Menezes Santos (Sistemas), "
        "Vitor Paiva Lopes e Silva Andrade (Service Desk), "
        "Larissa de Carvalho Rocha da Silva (Sistemas).",
        "Organograma TIC – estagiários",
        "organograma_tic"
    ))

    records.append((
        "Quem são os analistas sênior da TIC?",
        "Os analistas sênior da TIC são: "
        "Danilo Alves Souza (Processos – Sistemas), "
        "Josue Cortes Silva (Processos – Sistemas), "
        "Wellington Fava dos Santos (Processos – Sistemas), "
        "Rinaldo Alexandre dos Santos (Processos – Sistemas), "
        "Mauricio Reis Matos (Infra-Estrutura).",
        "Organograma TIC – analistas sênior",
        "organograma_tic"
    ))

    records.append((
        "Quem são os técnicos do Service Desk?",
        "Técnicos II: Andre Luiz Santos Sena, Cristiano Meneses de Farias, Felipe Marcelo Santos Lima, "
        "Javany Jose dos Santos Peixoto Junior, Rafael do Sacramento Santos, Robson Silva Santana, Vagner Santana dos Santos. "
        "Técnicos I: Bruno Braga Cerqueira, Deivisson Taua Santos e Santos, Ednaldo Monteiro Nunes, "
        "Elizeu Valverde da Silva Neto, Isaque Souza da Silva, Mario Batista dos Reis Neto, Renato Guedes dos Reis Santos.",
        "Organograma TIC – técnicos Service Desk",
        "organograma_tic"
    ))

    records.append((
        "Quem é o colaborador mais antigo da TIC?",
        "O colaborador mais antigo da TIC é Antonio Manoel da Silva Filho, admitido em 01/06/1999, "
        "seguido de Monica Maria Bezerra da Silva (05/04/1999) — ambos com mais de 25 anos de casa.",
        "Organograma TIC – histórico",
        "organograma_tic"
    ))

    records.append((
        "Qual o centro de custo do Service Desk?",
        "O centro de custo da Supervisão de Service Desk é 12.136.",
        "Organograma TIC – centros de custo",
        "organograma_tic"
    ))

    records.append((
        "Qual o centro de custo da Coordenação de Sistemas?",
        "O centro de custo da Coordenação de Sistemas e Aplicações é 12.131.",
        "Organograma TIC – centros de custo",
        "organograma_tic"
    ))

    records.append((
        "Qual o centro de custo da Supervisão de Infraestrutura?",
        "O centro de custo da Supervisão de Infraestrutura e Segurança é 12.133.",
        "Organograma TIC – centros de custo",
        "organograma_tic"
    ))

    records.append((
        "Qual o centro de custo da Coordenação de Analytics?",
        "O centro de custo da Coordenação de Analytics, Processos e Inovações é 12.132.",
        "Organograma TIC – centros de custo",
        "organograma_tic"
    ))

    records.append((
        "Qual o centro de custo da Gerência de TIC?",
        "O centro de custo da Gerência de Tecnologia da Informação e Comunicação é 12.130.",
        "Organograma TIC – centros de custo",
        "organograma_tic"
    ))

    return records


# ==============================================================================
# EXECUÇÃO
# ==============================================================================

if __name__ == "__main__":
    knowledge = build_records()
    total = len(knowledge)
    inseridos = 0
    duplicados = 0
    erros = 0

    print(f"🚀 Iniciando ingestão do organograma: {total} registros...\n")

    for i, (query, answer, context, source) in enumerate(knowledge, 1):
        try:
            result = ingest_validated_answer(query, answer, context, source)
            if result:
                inseridos += 1
                print(f"  [{i:03d}/{total}] ✅ {query[:70]}...")
            else:
                duplicados += 1
                print(f"  [{i:03d}/{total}] ⚠️  Duplicado: {query[:70]}...")
        except Exception as e:
            erros += 1
            print(f"  [{i:03d}/{total}] ❌ Erro: {query[:70]}\n         → {e}")

    print(f"""
╔══════════════════════════════════════╗
║      INGESTÃO ORGANOGRAMA CONCLUÍDA  ║
╠══════════════════════════════════════╣
║  Total de registros : {total:>4}           ║
║  ✅ Inseridos        : {inseridos:>4}           ║
║  ⚠️  Duplicados      : {duplicados:>4}           ║
║  ❌ Erros            : {erros:>4}           ║
╚══════════════════════════════════════╝
    """)