function criarTabela(prontuarios, alunos, urlProntuario){
    tabela = new window.simpleDatatables.DataTable("#tabelaProntuarios", {
        columns: [
            {
                select: 3,
                type: 'string',
                render: function(data, td, rowIndex, cellIndex) {
                    const url = urlProntuario.replace("670670", data);
                    return `<a href='${url}' data-row='${rowIndex}' class='btn btn-primary'>Ver prontuário</a>`;
                }
            }
        ],
            labels: {
            placeholder: "Pesquisar...",
            searchTitle: "Pesquisar na tabela",
            pageTitle: "Página {page}",
            perPage: "prontuários por página",
            noRows: "Nenhum prontuário encontrado",
            info: "Mostrando do {start}° até o {end}° de {rows} prontuários",
            noResults: "Nenhum resultado corresponde à sua pesquisa"
        }
    });
    
    dados = {data: []}
    for (prontuario of prontuarios) {
        dados.data.push([
            alunos[prontuario["aluno"]]["nome"], 
            alunos[prontuario["aluno"]]["matricula"], 
            prontuario["data"], 
            prontuario["id"]
        ])
    }
    tabela.insert(dados);
    tabela.update();
}

