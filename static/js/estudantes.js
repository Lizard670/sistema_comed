// ─── Utilitários ─────────────────────────────────────────────────────────────

function formatarData(dataStr) {
    if (!dataStr) return "—";
    const [ano, mes, dia] = dataStr.split("-");
    return `${dia}/${mes}/${ano}`;
}

function labelTipo(tipo) {
    const map = { consulta: "Consulta", urgencia: "Urgência", medicacao: "Medicação", retorno: "Retorno" };
    return map[tipo] || tipo;
}

function labelStatus(status) {
    const map = { aberto: "Aberto", finalizado: "Finalizado", encaminhado: "Encaminhado" };
    return map[status] || status;
}

function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"));
    return match ? match.pop() : "";
}

// ─── Estado global ────────────────────────────────────────────────────────────

var turmas     = {};
var alunos     = {};
var calendario = null;
var tabelaSimple = null;

// ─── Calendário ───────────────────────────────────────────────────────────────

function iniciarCalendario() {
    calendario = new Calendar("#calendario", { language: "pt", displayHeader: true });
    calendario.setNumberMonthsDisplayed(1);
}

function atualizarCalendario(prontuarios) {
    const eventos = prontuarios.map(p => ({
        startDate: new Date(p.data + "T12:00:00"),
        endDate:   new Date(p.data + "T12:00:00"),
        color:     "#187D75",
        name:      labelTipo(p.tipo_atendimento)
    }));
    calendario.setDataSource(eventos);
}

// ─── Tabela de Alunos ─────────────────────────────────────────────────────────

function carregarTabelaAlunos() {
    Promise.all([
        fetch(urlApiTurmas).then(r => r.json()),
        fetch(urlApiAlunos).then(r => r.json())
    ])
    .then(([dadosTurmas, dadosAlunos]) => {
        dadosTurmas.forEach(t => { turmas[t.id] = t; });
        dadosAlunos.forEach(a => { alunos[a.id] = a; });

        if (tabelaSimple) { tabelaSimple.destroy(); }

        const corpo = document.getElementById("corpoTabelaEstudantes");
        corpo.innerHTML = "";

        dadosAlunos.forEach(aluno => {
            const nomeTurma = turmas[aluno.turma] ? turmas[aluno.turma].nome : "—";
            const tr = document.createElement("tr");
            tr.dataset.alunoId = aluno.id;
            tr.innerHTML = `
                <td>${aluno.nome}</td>
                <td>${nomeTurma}</td>
                <td>${aluno.matricula}</td>
                <td>${formatarData(aluno.nascimento)}</td>
            `;
            tr.addEventListener("click", () => selecionarAluno(aluno.id, tr));
            corpo.appendChild(tr);
        });

        tabelaSimple = new window.simpleDatatables.DataTable("#tabelaEstudantes", {
            labels: {
                placeholder: "Pesquisar...",
                perPage: "alunos por página",
                noRows: "Nenhum aluno encontrado",
                info: "Mostrando do {start}° ao {end}° de {rows} alunos",
                noResults: "Nenhum resultado para sua pesquisa"
            }
        });
    })
    .catch(err => console.error("Erro ao carregar alunos:", err));
}

// ─── Seleção de aluno ─────────────────────────────────────────────────────────

function selecionarAluno(idAluno, trClicado) {
    document.querySelectorAll("#tabelaEstudantes tr.selecionado")
            .forEach(tr => tr.classList.remove("selecionado"));
    trClicado.classList.add("selecionado");

    alunoSelecionadoId = idAluno; // guarda para o modal de edição usar

    document.getElementById("nomeAlunoSelecionado").textContent = alunos[idAluno].nome;
    document.getElementById("secaoHistorico").classList.remove("oculto");
    document.getElementById("mensagem-selecione").style.display = "none";
    document.getElementById("btnAbrirEditar").disabled = false; // habilita o botão editar

    carregarHistorico(idAluno);
}

// ─── Histórico de prontuários ─────────────────────────────────────────────────

function carregarHistorico(idAluno) {
    const url = urlAlunoProntuarios.replace("ID_ALUNO", idAluno);

    fetch(url)
        .then(r => r.json())
        .then(prontuarios => {
            const corpo    = document.getElementById("corpoHistorico");
            const msgVazio = document.getElementById("mensagemSemProntuarios");
            corpo.innerHTML = "";

            if (prontuarios.length === 0) {
                msgVazio.style.display = "block";
                atualizarCalendario([]);
                return;
            }

            msgVazio.style.display = "none";

            prontuarios.forEach(p => {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td>${formatarData(p.data)}</td>
                    <td>${labelTipo(p.tipo_atendimento)}</td>
                    <td>${labelStatus(p.status)}</td>
                    <td>
                        <!-- TODO: link para prontuario.html depende de quem está fazendo aquela página -->
                        <button class="btn btn-visualizar">Visualizar</button>
                    </td>
                `;
                corpo.appendChild(tr);
            });

            atualizarCalendario(prontuarios);
        })
        .catch(err => console.error("Erro ao carregar histórico:", err));
}

// ─── Adicionar Aluno ──────────────────────────────────────────────────────────

function registrarEventosModal() {
    // Preenche o select de turmas quando o modal abre
    document.getElementById("modalAdicionarAluno").addEventListener("show.bs.modal", () => {
        fetch(urlApiTurmas)
            .then(r => r.json())
            .then(dados => {
                const select = document.getElementById("novoTurma");
                select.innerHTML = '<option value="">Selecione a turma</option>';
                dados.forEach(t => {
                    const opt = document.createElement("option");
                    opt.value = t.id;
                    opt.textContent = t.nome;
                    select.appendChild(opt);
                });
            });
    });

    // Salvar aluno
    document.getElementById("btnSalvarAluno").addEventListener("click", () => {
        const msgErro = document.getElementById("erroAdicionarAluno");
        msgErro.style.display = "none";

        const payload = {
            nome:             document.getElementById("novoNome").value.trim(),
            matricula:        document.getElementById("novaMatricula").value.trim(),
            nascimento:       document.getElementById("novoNascimento").value,
            nome_responsavel: document.getElementById("novoResponsavel").value.trim(),
            turma:            parseInt(document.getElementById("novoTurma").value),
            tipo_sanguineo:   document.getElementById("novoTipoSanguineo").value || null,
            peso:             document.getElementById("novoPeso").value || null,
            altura:           document.getElementById("novaAltura").value || null,
            medicamentos:     document.getElementById("novoMedicamentos").value || null,
            restricoes:       document.getElementById("novasRestricoes").value || null,
            observacoes:      document.getElementById("novasObservacoes").value || null,
        };

        if (!payload.nome || !payload.matricula || !payload.nascimento || !payload.nome_responsavel || !payload.turma) {
            msgErro.textContent = "Preencha todos os campos obrigatórios (*)";
            msgErro.style.display = "block";
            return;
        }

        fetch(urlApiAlunos, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        })
        .then(r => {
            if (!r.ok) {
                return r.json()
                    .catch(() => { throw new Error(`Erro ${r.status}: ${r.statusText}`); })
                    .then(e => { throw e; });
            }
            return r.json();
        })
        .then(() => {
            bootstrap.Modal.getInstance(document.getElementById("modalAdicionarAluno")).hide();
            carregarTabelaAlunos();
        })
        .catch(erro => {
            console.error("Erro ao salvar aluno:", erro);
            let mensagem;
            if (erro instanceof Error) {
                mensagem = erro.message;
            } else if (erro.detail) {
                mensagem = erro.detail;
            } else {
                mensagem = Object.entries(erro)
                    .map(([campo, msgs]) => `${campo}: ${[].concat(msgs).join(", ")}`)
                    .join(" | ");
            }
            msgErro.textContent = "Erro: " + mensagem;
            msgErro.style.display = "block";
        });
    });
}

// ─── Inicialização — tudo começa aqui, depois que o DOM e os scripts carregaram

document.addEventListener("DOMContentLoaded", () => {
    iniciarCalendario();
    carregarTabelaAlunos();
    registrarEventosModal();  // registra APÓS o Bootstrap já estar disponível
    registrarEventosEditar(); // idem para o modal de edição
});

// ─── Editar Aluno ─────────────────────────────────────────────────────────────

var alunoSelecionadoId = null; // guarda qual aluno está selecionado

function registrarEventosEditar() {
    // Quando o modal de editar abre, preenche os campos com os dados do aluno selecionado
    document.getElementById("modalEditarAluno").addEventListener("show.bs.modal", () => {
        const aluno = alunos[alunoSelecionadoId];
        if (!aluno) return;

        // Preenche cada campo com o valor atual do aluno
        document.getElementById("editNome").value         = aluno.nome || "";
        document.getElementById("editMatricula").value    = aluno.matricula || "";
        document.getElementById("editNascimento").value   = aluno.nascimento || "";
        document.getElementById("editResponsavel").value  = aluno.nome_responsavel || "";
        document.getElementById("editTipoSanguineo").value = aluno.tipo_sanguineo || "";
        document.getElementById("editPeso").value         = aluno.peso || "";
        document.getElementById("editAltura").value       = aluno.altura || "";
        document.getElementById("editMedicamentos").value = aluno.medicamentos || "";
        document.getElementById("editRestricoes").value   = aluno.restricoes || "";
        document.getElementById("editObservacoes").value  = aluno.observacoes || "";

        // Carrega as turmas no select e marca a turma atual do aluno
        fetch(urlApiTurmas)
            .then(r => r.json())
            .then(dados => {
                const select = document.getElementById("editTurma");
                select.innerHTML = '<option value="">Selecione a turma</option>';
                dados.forEach(t => {
                    const opt = document.createElement("option");
                    opt.value = t.id;
                    opt.textContent = t.nome;
                    // Pré-seleciona a turma que o aluno já tem
                    if (t.id === aluno.turma) opt.selected = true;
                    select.appendChild(opt);
                });
            });
    });

    // Salvar edição
    document.getElementById("btnSalvarEdicao").addEventListener("click", () => {
        const msgErro = document.getElementById("erroEditarAluno");
        msgErro.style.display = "none";

        const payload = {
            nome:             document.getElementById("editNome").value.trim(),
            matricula:        document.getElementById("editMatricula").value.trim(),
            nascimento:       document.getElementById("editNascimento").value,
            nome_responsavel: document.getElementById("editResponsavel").value.trim(),
            turma:            parseInt(document.getElementById("editTurma").value),
            tipo_sanguineo:   document.getElementById("editTipoSanguineo").value || null,
            peso:             document.getElementById("editPeso").value || null,
            altura:           document.getElementById("editAltura").value || null,
            medicamentos:     document.getElementById("editMedicamentos").value || null,
            restricoes:       document.getElementById("editRestricoes").value || null,
            observacoes:      document.getElementById("editObservacoes").value || null,
        };

        if (!payload.nome || !payload.matricula || !payload.nascimento || !payload.nome_responsavel || !payload.turma) {
            msgErro.textContent = "Preencha todos os campos obrigatórios (*)";
            msgErro.style.display = "block";
            return;
        }

        // PATCH envia só os campos alterados para /api/alunos/<id>/
        fetch(urlApiAlunos + alunoSelecionadoId + "/", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(payload)
        })
        .then(r => {
            if (!r.ok) {
                return r.json()
                    .catch(() => { throw new Error(`Erro ${r.status}: ${r.statusText}`); })
                    .then(e => { throw e; });
            }
            return r.json();
        })
        .then(alunoAtualizado => {
            // Atualiza o objeto local para refletir as mudanças sem precisar recarregar tudo
            alunos[alunoSelecionadoId] = alunoAtualizado;
            bootstrap.Modal.getInstance(document.getElementById("modalEditarAluno")).hide();
            // Recarrega a tabela para mostrar o nome/turma atualizados
            carregarTabelaAlunos();
        })
        .catch(erro => {
            console.error("Erro ao editar aluno:", erro);
            let mensagem;
            if (erro instanceof Error) {
                mensagem = erro.message;
            } else if (erro.detail) {
                mensagem = erro.detail;
            } else {
                mensagem = Object.entries(erro)
                    .map(([campo, msgs]) => `${campo}: ${[].concat(msgs).join(", ")}`)
                    .join(" | ");
            }
            msgErro.textContent = "Erro: " + mensagem;
            msgErro.style.display = "block";
        });
    });
}
