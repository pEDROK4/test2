import streamlit as st
import random
import numpy as np
import subprocess
import shutil
import os


def append_and_convert_to_tex(test_contents):
    shutil.copy2("cabeçalho.txt", "lista.txt")

    with open("lista.txt","a") as file:
        file.write(test_contents)

    with open("lista.txt", "r") as file:
        text2 = file.read()

    with open("lista.tex", "w") as file:
        file.write(text2)

    subprocess.run(["pdflatex", "lista.tex"])

    with open("lista.pdf", "rb") as file:
        pdf = file.read()
        st.download_button("Baixar PDF", pdf, "lista.pdf")
        


def select_content(selected_option):
    if selected_option == "Numeros Complexos":
        with open("Númeroscomplexos.tex", "r") as file:
            file_contents = file.read()

    elif selected_option == "Funções Complexas":
        with open("Funcoescomplexa.tex", "r") as file:
            file_contents = file.read()

    elif selected_option == "Cauchy-Riemann":
        with open("CauchyRiemann.tex", "r") as file:
            file_contents = file.read()

    return file_contents


def create_random_test(file_contents, num_questions):
    questions = []
    current_question = ""
    for line in file_contents.split("\n"):
        if "\problem" in line:
            if current_question:
                questions.append(current_question)
            current_question = ""
        else:
            current_question += line + "\n"
    if current_question:
        questions.append(current_question)

    if num_questions > len(questions):
        num_questions = len(questions)
    selected_questions = random.sample(questions, num_questions)

    test_contents = "\n\n \\begin{enumerate}\n"
    for question in selected_questions:
        test_contents += "\\item " + question + "\n"
    test_contents += "\\end{enumerate}\n\n \\end{document}"

    return test_contents


with open("style.css") as f:
    st.markdown(f"<style> {f.read()} <\style>", unsafe_allow_html= True)

st.title("Gerador de provas Automatico", anchor=False)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    curses = ["Numeros Complexos", "Funções Complexas", "Cauchy-Riemann"]
    selected_option = st.selectbox("Selecione um tópico:", curses)

    exam_type = st.radio("Selecione qual tipo de prova você quer ",["Prova 1","Prova 2","Prova 3"], index=0)

    num_questions = st.number_input("Qual a quantidade de Questões", min_value=1, max_value=10, step=1)

    if st.button('Gerar Arquivo'):
        file_contents = select_content(selected_option)
        test_contents = create_random_test(file_contents, num_questions)
        append_and_convert_to_tex(test_contents)
