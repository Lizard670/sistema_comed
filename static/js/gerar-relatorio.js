// Geração do PDF com jsPDF
function gerarPdfRelatorio(data, opcoes) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ unit: 'mm', format: 'a4' });

    const emissao = new Date().toLocaleString('pt-BR');

    const pageW = 210;
    const margin = 20;
    const cW = pageW - margin * 2;
    const alturaCabecalho = 38

    const corCabecalho = [24, 125, 117];
    const corTextoCabecalho = [255, 255, 255];
    const corTextoSecCabecalho = [200, 200, 200];
    const corTexto = [40, 40, 40];

    // Cabeçalho colorido
    doc.setFillColor(...corCabecalho);
    doc.rect(0, 0, pageW, alturaCabecalho, 'F');
    

    let xCabecalho = 8;
    let yCabecalho = 17;
    doc.setTextColor(...corTextoCabecalho);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('IFBA - Campus Porto Seguro', xCabecalho, yCabecalho);
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text('CoMed - Coordenação Médica', xCabecalho, yCabecalho+8);
    doc.setTextColor(...corTextoSecCabecalho);
    doc.text('Emissão: ' + emissao, xCabecalho, yCabecalho+15);

    let y = alturaCabecalho + 14;

    if (opcoes["escrever_opcoes"]) {
        // Dados do estudante
        doc.setTextColor(...corTexto);
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(11);
        doc.text('Opções do relatório', margin, y);
        y+=8;

        const texto_opcoes = [
            // TODO: usar equivalencias pra deixar o texto do agrupamento mais bonito
            ['Agrupamento:', opcoes["agrupar"] || '—'],
        ];
        if (opcoes["data_inicio"]) {texto_opcoes.push(['Início do período:', DateParaString(opcoes["data_inicio"])])}
        if (opcoes["data_fim"]) {texto_opcoes.push(['Final do período:', DateParaString(opcoes["data_fim"])])}

        doc.setFontSize(10);
        texto_opcoes.forEach(([label, valor]) => {
            doc.setFont('helvetica', 'bold');
            doc.text(label, margin+5, y);
            doc.setFont('helvetica', 'normal');
            doc.text(String(valor), margin + 55, y);
            y += 7;
        });
        y+=7;
    }


    // Título
    doc.setTextColor(...corCabecalho);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('RELATÓRIO', pageW / 2, y, { align: 'center' });
    y+=4;
    doc.setDrawColor(...corCabecalho);
    doc.setLineWidth(0.5);
    doc.line(margin, y, pageW - margin, y);
    y+=7;
    

    // Descrição
    doc.setTextColor(...corTexto);
    y += 4;
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    //const linhas = doc.splitTextToSize(data.descricao || 'AA', cW);
    //doc.text(linhas, margin, y);
    //y += linhas.length * 6 + 12;

    doc.setFont('helvetica', 'bold');
    doc.text("Prontuários no período selecionado: ", margin, y);
    doc.setFont('helvetica', 'normal');
    doc.text(String(data["total_prontuarios"]), margin + 65, y);
    y += 7;

    console.log(data);
    doc.table(margin, y, data["prontuarios"], data["cabecalhos"], {"fontSize": 10});

    doc.save("Relatório.pdf");
}