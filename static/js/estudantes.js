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
var prontuariosCalendario = {};

// ─── Calendário ───────────────────────────────────────────────────────────────

function iniciarCalendario() {
    calendario = new Calendar(".calendario");
    calendario.setNumberMonthsDisplayed(2);
    calendario.setLanguage("pt");
    calendario.setCustomDayRenderer(renderizarDiaCalendario);

    const modalProntuariosDia = document.getElementById("modalProntuariosDia");
    modalProntuariosDia.addEventListener("show.bs.modal", evento => {
        const data = evento.relatedTarget.dataset.date;
        const [ano, mes, dia] = data.split("-");
        const prontuarios = (((prontuariosCalendario[ano] || {})[mes] || {})[dia] || []);
        const corpoModal = modalProntuariosDia.querySelector(".modal-body");

        corpoModal.innerHTML = "";
        prontuarios.forEach(prontuario => {
            const item = document.createElement("a");
            item.className = "d-block mb-2";
            item.href = urlProntuarioDetalhe.replace("670670", prontuario.id);
            item.textContent = `${formatarData(prontuario.data)} — ${labelTipo(prontuario.tipo_atendimento)} (${labelStatus(prontuario.status)})`;
            corpoModal.appendChild(item);
        });
    });
}

function atualizarCalendario(prontuarios) {
    prontuariosCalendario = {};

    prontuarios.forEach(prontuario => {
        const [ano, mes, dia] = prontuario.data.split("-");
        if (!prontuariosCalendario[ano]) prontuariosCalendario[ano] = {};
        if (!prontuariosCalendario[ano][mes]) prontuariosCalendario[ano][mes] = {};
        if (!prontuariosCalendario[ano][mes][dia]) prontuariosCalendario[ano][mes][dia] = [];
        prontuariosCalendario[ano][mes][dia].push(prontuario);
    });

    // Exibe inicialmente o mês do primeiro prontuário retornado no histórico.
    if (prontuarios.length > 0) {
        const [ano, mes] = prontuarios[0].data.split("-").map(Number);
        calendario.setStartDate(new Date(ano, mes - 1, 1));
    }

    calendario.render();
}

function renderizarDiaCalendario(elemento, dataAtual) {
    const ano = String(dataAtual.getFullYear());
    const mes = String(dataAtual.getMonth() + 1).padStart(2, "0");
    const dia = String(dataAtual.getDate()).padStart(2, "0");

    if (!(((prontuariosCalendario[ano] || {})[mes] || {})[dia])) return;

    const bolha = document.createElement("div");
    bolha.classList.add("bolha-calendario");
    elemento.setAttribute("data-bs-toggle", "modal");
    elemento.setAttribute("data-bs-target", "#modalProntuariosDia");
    elemento.dataset.date = `${ano}-${mes}-${dia}`;
    elemento.appendChild(bolha);
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
        cursos = {};
        turmas = {};
        alunos = {};
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

    alunoSelecionadoId = Number(idAluno);

    document.getElementById("nomeAlunoSelecionado").textContent = alunos[idAluno].nome;
    document.getElementById("secaoHistorico").classList.remove("oculto");
    document.getElementById("mensagem-selecione").style.display = "none";
    document.getElementById("btnAbrirEditar").disabled = false;

    carregarHistorico(idAluno);
    preencherFormAluno(idAluno);
}

function buscarAlunoDetalhado(idAluno) {
    return fetch("/api/aluno/" + idAluno + "/")
        .then(r => {
            if (!r.ok) throw new Error(`Erro ${r.status} ao buscar aluno`);
            return r.json();
        })
        .then(aluno => {
            alunos[idAluno] = aluno;
            return aluno;
        });
}

function preencherFormAluno(idAluno) {
    // Busca dados completos do aluno (AlunoDetailSerializer retorna __all__)
    return buscarAlunoDetalhado(idAluno)
        .then(aluno => {
            // Se o usuário clicou em outra linha enquanto a requisição estava
            // em andamento, a resposta antiga não pode sobrescrever o formulário.
            if (Number(aluno.id) !== Number(idAluno) || Number(alunoSelecionadoId) !== Number(idAluno)) {
                return;
            }

            // "Aluno" e "Turma" sao ModelChoiceField — Django gera <select> cujo valor e o id
            const campoNome = document.getElementById("id_nome");
            if (campoNome) campoNome.value = aluno.id;

            // O campo crispy é do tipo date e precisa receber ISO (YYYY-MM-DD).
            const campoData = document.getElementById("id_data");
            if (campoData) campoData.value = aluno.nascimento || "";

            const campoTipo = document.getElementById("id_tipo");
            if (campoTipo) campoTipo.value = aluno.tipo_sanguineo || "";

            const campoPeso = document.getElementById("id_peso");
            if (campoPeso) campoPeso.value = aluno.peso || "";

            const campoMae = document.getElementById("id_mae");
            if (campoMae) campoMae.value = aluno.nome_responsavel || "";

            const campoAltura = document.getElementById("id_altura");
            if (campoAltura) campoAltura.value = aluno.altura || "";

            const campoMatricula = document.getElementById("id_matricula");
            if (campoMatricula) campoMatricula.value = aluno.matricula || "";

            const campoTurma = document.getElementById("id_turma");
            if (campoTurma) campoTurma.value = aluno.turma || "";

            const campoDescricao = document.getElementById("id_descricao");
            if (campoDescricao) campoDescricao.value = aluno.observacoes || "";

            const campoRestricoes = document.getElementById("id_restricoes");
            if (campoRestricoes) campoRestricoes.value = aluno.restricoes || "";

            const campoMedicamentos = document.getElementById("id_medicamentos");
            if (campoMedicamentos) campoMedicamentos.value = aluno.medicamentos || "";

            // Rola ate o form para o usuario ver que foi preenchido
            if (campoNome) campoNome.scrollIntoView({ behavior: "smooth", block: "center" });
        })
        .catch(err => console.error("Erro ao buscar detalhes do aluno:", err));
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
                const urlProntuario = urlProntuarioDetalhe.replace("670670", p.id);
                tr.innerHTML = `
                    <td>${formatarData(p.data)}</td>
                    <td>${labelTipo(p.tipo_atendimento)}</td>
                    <td>${labelStatus(p.status)}</td>
                    <td>
                        <a href="${urlProntuario}" class="btn btn-visualizar">Visualizar</a>
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
    const select = document.getElementById(selectId);
    select.innerHTML = '<option value="">Carregando...</option>';

    return fetch(urlApiTurmas)
        .then(r => {
            if (!r.ok) throw new Error(`Erro ${r.status} ao carregar turmas`);
            return r.json();
        })
        .then(dados => {
            select.innerHTML = '<option value="">Selecione a turma</option>';
            dados.forEach(t => {
                const opt       = document.createElement("option");
                opt.value       = t.id;
                // Mostra "ALM1A · Alimentos" se o curso existir, senão só "ALM1A"
                const nomeCurso = cursos[t.curso] ? cursos[t.curso].nome : "";
                opt.textContent = nomeCurso ? `${t.nome} · ${nomeCurso}` : t.nome;
                if (String(t.id) === String(turmaSelecionadaId)) opt.selected = true;
                select.appendChild(opt);
            });
        })
        .catch(erro => {
            console.error("Erro ao carregar turmas:", erro);
            select.innerHTML = '<option value="">Não foi possível carregar as turmas</option>';
        });
}

// ─── Adicionar Curso/Turma ───────────────────────────────────────────────────

function preencherSelectCursos() {
    const select = document.getElementById("cursoExistente");
    select.innerHTML = '<option value="">Selecione um curso</option>';

    return fetch(urlApiCursos)
        .then(r => {
            if (!r.ok) throw new Error(`Erro ${r.status} ao carregar cursos`);
            return r.json();
        })
        .then(dados => {
            cursos = {};
            dados.forEach(curso => {
                cursos[curso.id] = curso;
                const option = document.createElement("option");
                option.value = curso.id;
                option.textContent = curso.nome;
                select.appendChild(option);
            });
        })
        .catch(erro => {
            console.error("Erro ao carregar cursos:", erro);
            select.innerHTML = '<option value="">Não foi possível carregar os cursos</option>';
        });
}

function mensagemErroApi(erro) {
    if (erro instanceof Error) return erro.message;
    if (erro.detail) return erro.detail;
    return Object.entries(erro).map(([campo, mensagens]) =>
        `${campo}: ${[].concat(mensagens).join(", ")}`
    ).join(" | ");
}

function requisicaoApi(url, payload) {
    return fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
        body: JSON.stringify(payload)
    }).then(resposta => {
        if (!resposta.ok) {
            return resposta.json().catch(() => {
                throw new Error(`Erro ${resposta.status}: ${resposta.statusText}`);
            }).then(erro => { throw erro; });
        }
        return resposta.json();
    });
}

function registrarEventosCursoTurma() {
    const modal = document.getElementById("modalAdicionarCursoTurma");
    const campoCursoExistente = document.getElementById("cursoExistente");
    const campoNovoCurso = document.getElementById("novoCurso");
    const campoNovaTurma = document.getElementById("novaTurma");
    const msgErro = document.getElementById("erroAdicionarCursoTurma");

    modal.addEventListener("show.bs.modal", () => {
        msgErro.style.display = "none";
        campoNovoCurso.value = "";
        campoNovaTurma.value = "";
        campoCursoExistente.disabled = false;
        preencherSelectCursos();
    });

    campoNovoCurso.addEventListener("input", () => {
        campoCursoExistente.disabled = campoNovoCurso.value.trim() !== "";
    });

    document.getElementById("btnSalvarCursoTurma").addEventListener("click", () => {
        msgErro.style.display = "none";
        const nomeNovoCurso = campoNovoCurso.value.trim();
        const idCursoExistente = campoCursoExistente.value;
        const nomeTurma = campoNovaTurma.value.trim();

        if (!nomeNovoCurso && !nomeTurma) {
            msgErro.textContent = "Informe um novo curso ou o nome da turma.";
            msgErro.style.display = "block";
            return;
        }

        if (nomeTurma && !nomeNovoCurso && !idCursoExistente) {
            msgErro.textContent = "Selecione um curso existente ou informe um novo curso para cadastrar a turma.";
            msgErro.style.display = "block";
            return;
        }

        const cursoPromise = nomeNovoCurso
            ? requisicaoApi(urlApiCursos, { nome: nomeNovoCurso })
            : Promise.resolve({ id: Number(idCursoExistente) });

        cursoPromise
            .then(curso => {
                if (!nomeTurma) {
                    cursos[curso.id] = curso;
                    carregarTabelaAlunos();
                    const modalAlunoElemento = document.getElementById("modalAdicionarAluno");
                    modal.addEventListener("hidden.bs.modal", () => {
                        bootstrap.Modal.getOrCreateInstance(modalAlunoElemento).show();
                    }, { once: true });
                    bootstrap.Modal.getInstance(modal).hide();
                    return;
                }

                return requisicaoApi(urlApiTurmas, { nome: nomeTurma, curso: curso.id })
                    .then(turma => {
                        cursos[turma.curso] = cursos[turma.curso] || { id: turma.curso, nome: nomeNovoCurso };
                        turmas[turma.id] = turma;
                        carregarTabelaAlunos();
                        const modalAlunoElemento = document.getElementById("modalAdicionarAluno");
                        modalAlunoElemento.dataset.turmaSelecionada = turma.id;
                        modal.addEventListener("hidden.bs.modal", () => {
                            bootstrap.Modal.getOrCreateInstance(modalAlunoElemento).show();
                        }, { once: true });
                        bootstrap.Modal.getInstance(modal).hide();
                    });
            })
            .catch(erro => {
                console.error("Erro ao salvar curso/turma:", erro);
                msgErro.textContent = "Erro: " + mensagemErroApi(erro);
                msgErro.style.display = "block";
            });
    });
}

// ─── Adicionar Aluno ──────────────────────────────────────────────────────────

function registrarEventosModal() {
    // Preenche turmas quando o modal abre
    document.getElementById("modalAdicionarAluno").addEventListener("show.bs.modal", () => {
        const modal = document.getElementById("modalAdicionarAluno");
        const turmaSelecionada = modal.dataset.turmaSelecionada || null;
        delete modal.dataset.turmaSelecionada;
        preencherSelectTurmas("novoTurma", turmaSelecionada);
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
        if (!alunoSelecionadoId) return;

        buscarAlunoDetalhado(alunoSelecionadoId)
            .then(aluno => {
                document.getElementById("editNome").value         = aluno.nome || "";
                document.getElementById("editMatricula").value    = aluno.matricula || "";
                document.getElementById("editNascimento").value   = dataParaExibicao(aluno.nascimento);
                document.getElementById("editResponsavel").value  = aluno.nome_responsavel || "";
                document.getElementById("editTipoSanguineo").value = aluno.tipo_sanguineo || "";
                document.getElementById("editPeso").value         = aluno.peso || "";
                document.getElementById("editAltura").value       = aluno.altura || "";
                document.getElementById("editMedicamentos").value = aluno.medicamentos || "";
                document.getElementById("editRestricoes").value   = aluno.restricoes || "";
                document.getElementById("editObservacoes").value  = aluno.observacoes || "";

                return preencherSelectTurmas("editTurma", aluno.turma);
            })
            .catch(erro => console.error("Erro ao preparar edição do aluno:", erro));
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

// ─── Ações do histórico e formulário crispy ──────────────────────────────────

function mostrarMensagemSalvar(texto, tipo) {
    const mensagem = document.getElementById("mensagemSalvarAluno");
    mensagem.textContent = texto;
    mensagem.className = `alert alert-${tipo}`;
}

function registrarEventosFormularioAluno() {
    document.getElementById("formDadosAluno").addEventListener("submit", evento => {
        evento.preventDefault();

        if (!alunoSelecionadoId) {
            mostrarMensagemSalvar("Selecione um aluno antes de salvar as alterações.", "warning");
            return;
        }

        const payload = {
            nascimento:       document.getElementById("id_data").value || null,
            tipo_sanguineo:   document.getElementById("id_tipo").value || null,
            peso:             document.getElementById("id_peso").value || null,
            nome_responsavel: document.getElementById("id_mae").value.trim(),
            altura:           document.getElementById("id_altura").value || null,
            matricula:        document.getElementById("id_matricula").value.trim(),
            turma:            parseInt(document.getElementById("id_turma").value),
            observacoes:      document.getElementById("id_descricao").value.trim() || null,
            restricoes:       document.getElementById("id_restricoes").value.trim() || null,
            medicamentos:     document.getElementById("id_medicamentos").value.trim() || null,
        };

        if (!payload.nascimento || !payload.nome_responsavel || !payload.matricula || !payload.turma) {
            mostrarMensagemSalvar("Preencha data de nascimento, responsável, matrícula e turma antes de salvar.", "warning");
            return;
        }

        fetch(urlApiAlunos + alunoSelecionadoId + "/", {
            method: "PATCH",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCookie("csrftoken") },
            body: JSON.stringify(payload)
        })
        .then(r => {
            if (!r.ok) return r.json().then(erro => { throw erro; });
            return r.json();
        })
        .then(alunoAtualizado => {
            alunos[alunoSelecionadoId] = alunoAtualizado;
            mostrarMensagemSalvar("Dados do aluno salvos com sucesso.", "success");
            carregarTabelaAlunos();
        })
        .catch(erro => {
            console.error("Erro ao salvar dados do aluno:", erro);
            const detalhes = erro.detail || Object.entries(erro)
                .map(([campo, mensagens]) => `${campo}: ${[].concat(mensagens).join(", ")}`).join(" | ");
            mostrarMensagemSalvar(`Não foi possível salvar: ${detalhes}`, "danger");
        });
    });
}

// ─── Inicialização ────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    // Os campos dos modais usam texto; o formulário crispy usa um input date.
    aplicarMascaraData(document.getElementById("novoNascimento"));
    aplicarMascaraData(document.getElementById("editNascimento"));

    iniciarCalendario();
    carregarTabelaAlunos();

    // O DataTable recria o tbody ao ordenar, paginar e filtrar. Por isso, o
    // clique é tratado na tabela, que permanece a mesma durante essas ações.
    const tabelaEstudantes = document.getElementById("tabelaEstudantes");
    tabelaEstudantes.addEventListener("click", evento => {
        const linha = evento.target.closest("tr[data-aluno-id]");
        if (!linha || !tabelaEstudantes.contains(linha)) return;
        selecionarAluno(Number(linha.dataset.alunoId), linha);
    });

    registrarEventosModal();
    registrarEventosCursoTurma();
    registrarEventosEditar();
    registrarEventosFormularioAluno();
});
