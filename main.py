import flet as ft
import json
import os

ARQ = "dados.json"

if os.path.exists(ARQ):
    with open(ARQ, "r", encoding="utf-8") as arquivo:
        contatos = json.load(arquivo)
else:
    contatos = []


def salvar():
    with open(ARQ, "w", encoding="utf-8") as arquivo:
        json.dump(
            contatos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def main(page: ft.Page):
    page.title = "Cadastro de Contatos"

    nome = ft.TextField(
        label="Nome",
        width=400
    )

    tel = ft.TextField(
        label="Telefone",
        width=400
    )

    lista = ft.Column()

    editando = -1

    def atualizar():
        lista.controls.clear()

        for i, contato in enumerate(contatos):
            lista.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(
                            f"{contato['nome']} - {contato['tel']}",
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            data=i,
                            on_click=editar
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            data=i,
                            on_click=excluir
                        ),
                    ]
                )
            )

    def salvar_clique(e):
        nonlocal editando

        if not nome.value:
            return

        contato = {
            "nome": nome.value,
            "tel": tel.value
        }

        if editando == -1:
            contatos.append(contato)
        else:
            contatos[editando] = contato
            editando = -1
            botao.content = "Adicionar"

        nome.value = ""
        tel.value = ""

        salvar()
        atualizar()

    def editar(e):
        nonlocal editando

        editando = e.control.data

        nome.value = contatos[editando]["nome"]
        tel.value = contatos[editando]["tel"]

        botao.content = "Salvar"

    def excluir(e):
        indice = e.control.data

        contatos.pop(indice)

        salvar()
        atualizar()

    botao = ft.Button(
        content="Adicionar",
        on_click=salvar_clique
    )

    page.add(
        ft.Text("Cadastro de Contatos", size=22),
        nome,
        tel,
        botao,
        lista
    )

    atualizar()


if __name__ == "__main__":
    ft.run(main)