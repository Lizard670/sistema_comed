// ─── Utilitários ─────────────────────────────────────────────────────────────

function formatarData(dataStr) {
    // API devolve "YYYY-MM-DD", exibe "DD/MM/AAAA"
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

// Converte "DD/MM/AAAA" → "YYYY-MM-DD" para enviar à API
function dataParaISO(dataStr) {
    if (!dataStr) return "";
    const [dia, mes, ano] = dataStr.split("/");
    return `${ano}-${mes}-${dia}`;
}

// Converte "YYYY-MM-DD" → "DD/MM/AAAA" para preencher os campos
function dataParaExibicao(dataStr) {
    if (!dataStr) return "";
    const [ano, mes, dia] = dataStr.split("-");
    return `${dia}/${mes}/${ano}`;
}

// Aplica máscara DD/MM/AAAA em tempo real enquanto o usuário digita
function aplicarMascaraData(input) {
    input.addEventListener("input", () => {
        let v = input.value.replace(/\D/g, ""); // remove tudo que não é número
        if (v.length > 2)  v = v.slice(0,2) + "/" + v.slice(2);
        if (v.length > 5)  v = v.slice(0,5) + "/" + v.slice(5);
        if (v.length > 10) v = v.slice(0,10);
        input.value = v;
    });
}

// ─── Estado global ────────────────────────────────────────────────────────────

var turmas           = {};  // id -> objeto turma
var cursos           = {};  // id -> objeto curso
var alunos           = {};  // id -> objeto aluno
var calendario       = null;
var tabelaSimple     = null;
var alunoSelecionadoId = null;

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
    // Busca cursos, turmas e alunos em paralelo
    Promise.all([
        fetch(urlApiCursos).then(r => r.json()),
        fetch(urlApiTurmas).then(r => r.json()),
        fetch(urlApiAlunos).then(r => r.json())
    ])
    .then(([dadosCursos, dadosTurmas, dadosAlunos]) => {
        dadosCursos.forEach(c => { cursos[c.id] = c; });
        dadosTurmas.forEach(t => { turmas[t.id] = t; });
        dadosAlunos.forEach(a => { alunos[a.id] = a; });

        if (tabelaSimple) { tabelaSimple.destroy(); }

        const corpo = document.getElementById("corpoTabelaEstudantes");
        corpo.innerHTML = "";

        dadosAlunos.forEach(aluno => {
            const turma    = turmas[aluno.turma];
            const nomeTurma = turma ? turma.nome : "—";
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

    alunoSelecionadoId = idAluno;

    document.getElementById("nomeAlunoSelecionado").textContent = alunos[idAluno].nome;
    document.getElementById("secaoHistorico").classList.remove("oculto");
    document.getElementById("mensagem-selecione").style.display = "none";
    document.getElementById("btnAbrirEditar").disabled = false;

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

// ─── Preenche select de turmas com "Turma · Curso" ───────────────────────────

function preencherSelectTurmas(selectId, turmaSelecionadaId) {
    fetch(urlApiTurmas)
        .then(r => r.json())
        .then(dados => {
            const select = document.getElementById(selectId);
            select.innerHTML = '<option value="">Selecione a turma</option>';
            dados.forEach(t => {
                const opt       = document.createElement("option");
                opt.value       = t.id;
                // Mostra "ALM1A · Alimentos" se o curso existir, senão só "ALM1A"
                const nomeCurso = cursos[t.curso] ? cursos[t.curso].nome : "";
                opt.textContent = nomeCurso ? `${t.nome} · ${nomeCurso}` : t.nome;
                if (t.id === turmaSelecionadaId) opt.selected = true;
                select.appendChild(opt);
            });
        });
}

// ─── Adicionar Aluno ──────────────────────────────────────────────────────────

function registrarEventosModal() {
    // Preenche turmas quando o modal abre
    document.getElementById("modalAdicionarAluno").addEventListener("show.bs.modal", () => {
        preencherSelectTurmas("novoTurma", null);
    });

    document.getElementById("btnSalvarAluno").addEventListener("click", () => {
        const msgErro = document.getElementById("erroAdicionarAluno");
        msgErro.style.display = "none";

        const dataDigitada = document.getElementById("novoNascimento").value;

        const payload = {
            nome:             document.getElementById("novoNome").value.trim(),
            matricula:        document.getElementById("novaMatricula").value.trim(),
            nascimento:       dataParaISO(dataDigitada), // converte DD/MM/AAAA → YYYY-MM-DD
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
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify(payload)
        })
        .then(r => {
            if (!r.ok) return r.json().catch(() => { throw new Error(`Erro ${r.status}: ${r.statusText}`); }).then(e => { throw e; });
            return r.json();
        })
        .then(() => {
            bootstrap.Modal.getInstance(document.getElementById("modalAdicionarAluno")).hide();
            carregarTabelaAlunos();
        })
        .catch(erro => {
            console.error("Erro ao salvar aluno:", erro);
            const mensagem = erro instanceof Error ? erro.message
                           : erro.detail ? erro.detail
                           : Object.entries(erro).map(([c, m]) => `${c}: ${[].concat(m).join(", ")}`).join(" | ");
            msgErro.textContent = "Erro: " + mensagem;
            msgErro.style.display = "block";
        });
    });
}

// ─── Editar Aluno ─────────────────────────────────────────────────────────────

function registrarEventosEditar() {
    document.getElementById("modalEditarAluno").addEventListener("show.bs.modal", () => {
        const aluno = alunos[alunoSelecionadoId];
        if (!aluno) return;

        document.getElementById("editNome").value         = aluno.nome || "";
        document.getElementById("editMatricula").value    = aluno.matricula || "";
        // Converte YYYY-MM-DD para DD/MM/AAAA para exibir no campo com máscara
        document.getElementById("editNascimento").value   = dataParaExibicao(aluno.nascimento);
        document.getElementById("editResponsavel").value  = aluno.nome_responsavel || "";
        document.getElementById("editTipoSanguineo").value = aluno.tipo_sanguineo || "";
        document.getElementById("editPeso").value         = aluno.peso || "";
        document.getElementById("editAltura").value       = aluno.altura || "";
        document.getElementById("editMedicamentos").value = aluno.medicamentos || "";
        document.getElementById("editRestricoes").value   = aluno.restricoes || "";
        document.getElementById("editObservacoes").value  = aluno.observacoes || "";

        preencherSelectTurmas("editTurma", aluno.turma);
    });

    document.getElementById("btnSalvarEdicao").addEventListener("click", () => {
        const msgErro = document.getElementById("erroEditarAluno");
        msgErro.style.display = "none";

        const dataDigitada = document.getElementById("editNascimento").value;

        const payload = {
            nome:             document.getElementById("editNome").value.trim(),
            matricula:        document.getElementById("editMatricula").value.trim(),
            nascimento:       dataParaISO(dataDigitada), // converte DD/MM/AAAA → YYYY-MM-DD
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

        fetch(urlApiAlunos + alunoSelecionadoId + "/", {
            method: "PATCH",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify(payload)
        })
        .then(r => {
            if (!r.ok) return r.json().catch(() => { throw new Error(`Erro ${r.status}: ${r.statusText}`); }).then(e => { throw e; });
            return r.json();
        })
        .then(alunoAtualizado => {
            alunos[alunoSelecionadoId] = alunoAtualizado;
            bootstrap.Modal.getInstance(document.getElementById("modalEditarAluno")).hide();
            carregarTabelaAlunos();
        })
        .catch(erro => {
            console.error("Erro ao editar aluno:", erro);
            const mensagem = erro instanceof Error ? erro.message
                           : erro.detail ? erro.detail
                           : Object.entries(erro).map(([c, m]) => `${c}: ${[].concat(m).join(", ")}`).join(" | ");
            msgErro.textContent = "Erro: " + mensagem;
            msgErro.style.display = "block";
        });
    });
}

// ─── Inicialização ────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    // Aplica máscara DD/MM/AAAA nos campos de data dos dois modais
    aplicarMascaraData(document.getElementById("novoNascimento"));
    aplicarMascaraData(document.getElementById("editNascimento"));

    iniciarCalendario();
    carregarTabelaAlunos();
    registrarEventosModal();
    registrarEventosEditar();
});
