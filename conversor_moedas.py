
import tkinter as tk
from tkinter import ttk, messagebox
import requests


# Dicionário com moedas disponíveis
moedas = {
    "BRL": "Real brasileiro",
    "USD": "Dólar americano",
    "EUR": "Euro",
    "GBP": "Libra esterlina",
    "JPY": "Iene japonês",
    "CAD": "Dólar canadense",
    "AUD": "Dólar australiano",
    "CHF": "Franco suíço",
    "CNY": "Yuan chinês",
    "ARS": "Peso argentino",
    "CLP": "Peso chileno",
    "COP": "Peso colombiano",
    "MXN": "Peso mexicano",
    "UYU": "Peso uruguaio",
    "PYG": "Guarani paraguaio",
    "BOB": "Boliviano",
    "PEN": "Sol peruano",
    "ZAR": "Rand sul-africano",
    "INR": "Rúpia indiana",
    "KRW": "Won sul-coreano",
    "TRY": "Lira turca",
    "RUB": "Rublo russo",
    "PLN": "Zloty polonês",
    "SEK": "Coroa sueca",
    "NOK": "Coroa norueguesa",
    "DKK": "Coroa dinamarquesa",
    "CZK": "Coroa tcheca",
    "HUF": "Florim húngaro",
    "ILS": "Novo shekel israelense",
    "AED": "Dirham dos Emirados",
    "SAR": "Riyal saudita",
    "THB": "Baht tailandês",
    "NZD": "Dólar neozelandês",
    "SGD": "Dólar de Singapura",
    "HKD": "Dólar de Hong Kong",
    "IDR": "Rupia indonésia",
    "MYR": "Ringgit malaio",
    "PHP": "Peso filipino"
}


# Função para consultar a cotação na API
def consultar_cotacao(origem, destino):

    url = (
        f"https://economia.awesomeapi.com.br/json/last/"
        f"{origem}-{destino}"
    )

    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()

        dados = resposta.json()

        chave = origem + destino

        cotacao = float(dados[chave]["bid"])

        return cotacao

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Erro de conexão",
            "Não foi possível consultar a API.\n"
            "Verifique sua conexão com a internet."
        )
        return None

    except (KeyError, ValueError, TypeError):
        messagebox.showerror(
            "Erro na cotação",
            "A API não retornou uma cotação válida para "
            "o par de moedas selecionado."
        )
        return None


# Função para realizar a conversão
def converter():

    try:
        valor = float(campo_valor.get().replace(",", "."))

        if valor <= 0:
            messagebox.showwarning(
                "Atenção",
                "Digite um valor maior que zero."
            )
            return

        origem = moeda_origem.get().split(" - ")[0]
        destino = moeda_destino.get().split(" - ")[0]

        if not origem or not destino:
            messagebox.showwarning(
                "Atenção",
                "Selecione as duas moedas."
            )
            return

        # Se as moedas forem iguais, não consulta a API
        if origem == destino:
            cotacao = 1.0
        else:
            cotacao = consultar_cotacao(origem, destino)

            if cotacao is None:
                return

        resultado = valor * cotacao

        # Exibe o resultado
        campo_resultado.config(state="normal")
        campo_resultado.delete(0, tk.END)
        campo_resultado.insert(
            0,
            f"{resultado:,.2f} {destino}"
        )
        campo_resultado.config(state="readonly")

        texto_cotacao.config(
            text=f"1 {origem} = {cotacao:.6f} {destino}"
        )

        texto_status.config(
            text="Conversão realizada com sucesso!",
            fg="#65E6A5"
        )

    except ValueError:
        messagebox.showwarning(
            "Valor inválido",
            "Digite um valor numérico válido."
        )


# Função para inverter as moedas
def inverter_moedas():

    origem = moeda_origem.get()
    destino = moeda_destino.get()

    moeda_origem.set(destino)
    moeda_destino.set(origem)


# Função para limpar os campos
def limpar():

    campo_valor.delete(0, tk.END)

    campo_resultado.config(state="normal")
    campo_resultado.delete(0, tk.END)
    campo_resultado.config(state="readonly")

    texto_cotacao.config(text="Cotação: aguardando consulta")

    texto_status.config(
        text="Pronto para realizar uma conversão.",
        fg="#B0B0B0"
    )


# Configuração da janela principal
janela = tk.Tk()
janela.title("Conversor de Moedas")
janela.geometry("500x650")
janela.resizable(False, False)
janela.configure(bg="#20232A")


# Configuração dos estilos
estilo = ttk.Style()
estilo.theme_use("clam")

estilo.configure(
    "TCombobox",
    fieldbackground="#343A46",
    background="#343A46",
    foreground="white",
    arrowcolor="white",
    padding=8
)


# Título
tk.Label(
    janela,
    text="CONVERSOR DE MOEDAS",
    font=("Arial", 20, "bold"),
    bg="#20232A",
    fg="white"
).pack(pady=(25, 5))


# Subtítulo
tk.Label(
    janela,
    text="Consulte cotações e converta moedas",
    font=("Arial", 10),
    bg="#20232A",
    fg="#B0B0B0"
).pack(pady=(0, 25))


# Área principal
frame = tk.Frame(
    janela,
    bg="#2D323C",
    padx=25,
    pady=20
)
frame.pack(padx=30, fill="both")


# Campo de valor
tk.Label(
    frame,
    text="Valor para conversão:",
    font=("Arial", 11, "bold"),
    bg="#2D323C",
    fg="white"
).pack(anchor="w", pady=(0, 8))


campo_valor = tk.Entry(
    frame,
    font=("Arial", 14),
    bg="#20232A",
    fg="white",
    insertbackground="white",
    relief="flat"
)
campo_valor.pack(fill="x", ipady=10)


# Seleção das moedas
tk.Label(
    frame,
    text="Moeda de origem:",
    font=("Arial", 11, "bold"),
    bg="#2D323C",
    fg="white"
).pack(anchor="w", pady=(20, 8))


lista_moedas = [
    f"{codigo} - {nome}"
    for codigo, nome in moedas.items()
]


moeda_origem = tk.StringVar(value="BRL - Real brasileiro")

selecao_origem = ttk.Combobox(
    frame,
    textvariable=moeda_origem,
    values=lista_moedas,
    state="readonly",
    font=("Arial", 10)
)
selecao_origem.pack(fill="x", ipady=4)


# Botão para inverter as moedas
botao_inverter = tk.Button(
    frame,
    text="⇅  INVERTER MOEDAS",
    font=("Arial", 9, "bold"),
    bg="#343A46",
    fg="white",
    activebackground="#454D5B",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=inverter_moedas
)
botao_inverter.pack(pady=12)


tk.Label(
    frame,
    text="Moeda de destino:",
    font=("Arial", 11, "bold"),
    bg="#2D323C",
    fg="white"
).pack(anchor="w", pady=(0, 8))


moeda_destino = tk.StringVar(value="USD - Dólar americano")

selecao_destino = ttk.Combobox(
    frame,
    textvariable=moeda_destino,
    values=lista_moedas,
    state="readonly",
    font=("Arial", 10)
)
selecao_destino.pack(fill="x", ipady=4)


# Botão de conversão
botao_converter = tk.Button(
    janela,
    text="CONVERTER MOEDA",
    font=("Arial", 12, "bold"),
    bg="#6C45D9",
    fg="white",
    activebackground="#5433B5",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=converter
)
botao_converter.pack(fill="x", padx=50, pady=20, ipady=12)


# Resultado da conversão
tk.Label(
    janela,
    text="Valor convertido:",
    font=("Arial", 11, "bold"),
    bg="#20232A",
    fg="white"
).pack(pady=(0, 8))


campo_resultado = tk.Entry(
    janela,
    font=("Arial", 16, "bold"),
    justify="center",
    state="readonly",
    readonlybackground="#2D323C",
    fg="#65E6A5",
    relief="flat"
)
campo_resultado.pack(fill="x", padx=40, ipady=12)


# Exibição da cotação
texto_cotacao = tk.Label(
    janela,
    text="Cotação: aguardando consulta",
    font=("Arial", 10, "bold"),
    bg="#20232A",
    fg="#B0B0B0"
)
texto_cotacao.pack(pady=15)


# Botão limpar
botao_limpar = tk.Button(
    janela,
    text="LIMPAR CAMPOS",
    font=("Arial", 10, "bold"),
    bg="#343A46",
    fg="white",
    activebackground="#454D5B",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=limpar
)
botao_limpar.pack(fill="x", padx=50, ipady=8)


# Status do programa
texto_status = tk.Label(
    janela,
    text="Pronto para realizar uma conversão.",
    font=("Arial", 9),
    bg="#20232A",
    fg="#B0B0B0"
)
texto_status.pack(pady=15)


# Rodapé
tk.Label(
    janela,
    text="Desenvolvido em Python | API AwesomeAPI",
    font=("Arial", 8),
    bg="#20232A",
    fg="#888888"
).pack(side="bottom", pady=12)


# Inicia a aplicação
janela.mainloop()
