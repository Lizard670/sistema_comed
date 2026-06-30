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

// ─── Estado global ────────────────────────────────────────────────────────────

var turmas   = {};   // id -> objeto turma
var alunos   = {};   // id -> objeto aluno
var calendario = null;

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

var tabelaSimple = null;

function carregarTabelaAlunos() {
    Promise.all([
        fetch(urlApiTurmas).then(r => r.json()),
        fetch(urlApiAlunos).then(r => r.json())
    ])
    .then(([dadosTurmas, dadosAlunos]) => {

        dadosTurmas.forEach(t => { turmas[t.id] = t; });
        dadosAlunos.forEach(a => { alunos[a.id] = a; });

        if (tabelaSimple) {
            tabelaSimple.destroy();
        }

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

    document.getElementById("nomeAlunoSelecionado").textContent = alunos[idAluno].nome;
    document.getElementById("secaoHistorico").classList.remove("oculto");
    document.getElementById("mensagem-selecione").style.display = "none";

    carregarHistorico(idAluno);
}

// ─── Histórico de prontuários do aluno ───────────────────────────────────────

function carregarHistorico(idAluno) {
    const url = urlAlunoProntuarios.replace("ID_ALUNO", idAluno);

    fetch(url)
        .then(r => r.json())
        .then(prontuarios => {
            const corpo   = document.getElementById("corpoHistorico");
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
                        <button class="btn btn-visualizar">Visualizar prontuário</button>
                    </td>
                `;
                corpo.appendChild(tr);
            });

            atualizarCalendario(prontuarios);
        })
        .catch(err => console.error("Erro ao carregar histórico:", err));
}

// ─── Inicialização ────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    iniciarCalendario();
    carregarTabelaAlunos();
});

// ─── Adicionar Aluno ──────────────────────────────────────────────────────────

// Quando o modal abre, preenche o select de turmas com dados da API
document.getElementById("modalAdicionarAluno").addEventListener("show.bs.modal", () => {
    fetch(urlApiTurmas)
        .then(r => r.json())
        .then(dados => {
            const select = document.getElementById("novoTurma");
            select.innerHTML = '<option value="">Selecione a turma</option>';
            // Para cada turma recebida, cria um <option> no select
            dados.forEach(t => {
                const opt = document.createElement("option");
                opt.value = t.id;          // valor enviado para a API
                opt.textContent = t.nome;  // texto que o usuário vê
                select.appendChild(opt);
            });
        });
});

// Quando clica em Salvar
document.getElementById("btnSalvarAluno").addEventListener("click", () => {
    const msgErro = document.getElementById("erroAdicionarAluno");
    msgErro.style.display = "none";

    // Lê os valores de cada campo do modal
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

    // Validação básica dos campos obrigatórios antes de enviar
    if (!payload.nome || !payload.matricula || !payload.nascimento || !payload.nome_responsavel || !payload.turma) {
        msgErro.textContent = "Preencha todos os campos obrigatórios (*)";
        msgErro.style.display = "block";
        return;
    }

    // POST para a API — envia o payload como JSON
    fetch(urlApiAlunos, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // O Django exige o token CSRF em requisições POST
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify(payload)
    })
    .then(r => {
        // Se a API retornar erro (ex: matrícula duplicada), lança exceção com a resposta
        if (!r.ok) return r.json().then(e => { throw e; });
        return r.json();
    })
    .then(() => {
        // Deu certo: fecha o modal e recarrega a tabela para mostrar o aluno novo
        bootstrap.Modal.getInstance(document.getElementById("modalAdicionarAluno")).hide();
        carregarTabelaAlunos();
    })
    .catch(erros => {
        // Mostra o erro retornado pela API (ex: "matricula já cadastrada")
        const msgs = Object.values(erros).flat().join(" | ");
        msgErro.textContent = "Erro: " + msgs;
        msgErro.style.display = "block";
    });
});

// Pega o cookie CSRF que o Django coloca automaticamente na página
function getCookie(name) {
    const match = document.cookie.match(new RegExp("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)"));
    return match ? match.pop() : "";
}
