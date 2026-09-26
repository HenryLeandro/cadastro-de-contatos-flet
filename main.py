import flet as ft
import json
import os

ARQ = "dados.json"
contatos = json.load(open(ARQ, encoding="utf-8")) if os.path.exists(ARQ) else []


def salvar():
    json.dump(contatos, open(ARQ, "w", encoding="utf-8"), ensure_ascii=False, indent=4)


def main(page: ft.Page):
    nome = ft.TextField(label="Nome")
    tel = ft.TextField(label="Telefone")
    lista = ft.Column()
    editando = -1

    def atualizar():
        lista.controls.clear()
        for i, c in enumerate(contatos):
            lista.controls.append(ft.Row([
                ft.Text(c["nome"] + " - " + c["tel"]),
                ft.IconButton(ft.Icons.EDIT, data=i, on_click=editar),
                ft.IconButton(ft.Icons.DELETE, data=i, on_click=excluir),
            ]))
        page.update()

    def salvar_clique(e):
        nonlocal editando
        if not nome.value:
            return
        c = {"nome": nome.value, "tel": tel.value}
        if editando == -1:
            contatos.append(c)
        else:
            contatos[editando] = c
            editando = -1
            botao.text = "Adicionar"
        nome.value = tel.value = ""
        salvar()
        atualizar()
        page.update()

    def editar(e):
        nonlocal editando
        editando = e.control.data
        nome.value = contatos[editando]["nome"]
        tel.value = contatos[editando]["tel"]
        botao.text = "Salvar"
        page.update()

    def excluir(e):
        contatos.pop(e.control.data)
        salvar()
        atualizar()

    botao = ft.ElevatedButton("Adicionar", on_click=salvar_clique)
    page.add(ft.Text("Cadastro de Contatos", size=22), nome, tel, botao, lista)
    atualizar()


ft.app(target=main)