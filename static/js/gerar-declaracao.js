// Função auxiliar para converter um elemento <img> em Base64 PNG
function obterBase64DaImagem(imgElement) {
    try {
        const canvas = document.createElement('canvas');
        canvas.width = imgElement.naturalWidth || imgElement.width;
        canvas.height = imgElement.naturalHeight || imgElement.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(imgElement, 0, 0);
        return canvas.toDataURL('image/png');
    } catch (e) {
        console.error("Erro ao converter imagem para base64:", e);
        return null;
    }
}

// Geração do PDF com jsPDF
function gerarPdfDeclaracao(data) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({ unit: 'mm', format: 'a4' });

    const aluno = (data.prontuario_detalhes || {}).aluno || {};
    const pront = data.prontuario_detalhes || {};
    const codigo = data.codigo || '';
    const emissao = data.data_horario_emissao
        ? new Date(data.data_horario_emissao).toLocaleString('pt-BR')
        : new Date().toLocaleString('pt-BR');
    const dataAtend = pront.data
        ? new Date(pront.data + 'T00:00:00').toLocaleDateString('pt-BR')
        : '—';

    const pageW = 210;
    const margin = 20;
    const cW = pageW - margin * 2;

    // Cabeçalho colorido
    doc.setFillColor(24, 125, 117);
    doc.rect(0, 0, pageW, 38, 'F');

    // Logo do CoMed e IFBA no cabeçalho
    const imgIfba = document.getElementById('imgLogoIfba');
    const imgComed = document.getElementById('imgLogoComed');
    const base64Ifba = obterBase64DaImagem(imgIfba);
    const base64Comed = obterBase64DaImagem(imgComed);
    
    let currentX = 8; // Inicia mais à esquerda (margem menor que a do conteúdo para aproveitar o espaço)

    if (base64Comed) {
        // Desenha primeiro o logo do CoMed
        doc.addImage(base64Comed, 'PNG', currentX, 8, 26, 21);
        currentX += 29; // Espaço do logo CoMed + gap
    }

    if (base64Ifba) {
        // Desenha o logo do IFBA
        doc.addImage(base64Ifba, 'PNG', currentX, 7, 18, 24);
        currentX += 22; // Espaço do logo IFBA + gap
    }

    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('IFBA - Campus Porto Seguro', currentX, 17);
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text('CoMed - Coordenação Médica', currentX, 25);

    // Título
    doc.setTextColor(24, 125, 117);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(16);
    doc.text('DECLARAÇÃO', pageW / 2, 52, { align: 'center' });
    doc.setDrawColor(24, 125, 117);
    doc.setLineWidth(0.5);
    doc.line(margin, 56, pageW - margin, 56);

    // Dados do estudante
    doc.setTextColor(40, 40, 40);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(11);
    doc.text('Dados do Estudante', margin, 65);

    const campos = [
        ['Nome:', aluno.nome || '—'],
        ['Matrícula:', aluno.matricula || '—'],
        ['Turma:', aluno.turma_nome || '—'],
        ['Curso:', aluno.curso_nome || '—'],
        ['Data do Atendimento:', dataAtend],
    ];

    doc.setFontSize(10);
    let y = 73;
    campos.forEach(([label, valor]) => {
        doc.setFont('helvetica', 'bold');
        doc.text(label, margin, y);
        doc.setFont('helvetica', 'normal');
        doc.text(String(valor), margin + 55, y);
        y += 7;
    });

    // Descrição
    y += 4;
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(11);
    // doc.text('Descrição', margin, y);
    y += 7;
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(10);
    const linhas = doc.splitTextToSize(data.descricao || '', cW);
    doc.text(linhas, margin, y);
    y += linhas.length * 6 + 12;

    // Caixa do código de validação
    doc.setFillColor(237, 248, 246);
    doc.setDrawColor(24, 125, 117);
    doc.setLineWidth(0.8);
    doc.roundedRect(margin, y, cW, 26, 3, 3, 'FD');
    doc.setTextColor(24, 125, 117);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(8);
    doc.text('CÓDIGO DE VALIDAÇÃO', pageW / 2, y + 8, { align: 'center' });
    doc.setFont('courier', 'bold');
    doc.setFontSize(15);
    doc.text(codigo, pageW / 2, y + 19, { align: 'center' });
    y += 33;

    // Posiciona data de emissão e QR Code de forma absoluta na base do PDF
    const footerY = 242;

    doc.setTextColor(120, 120, 120);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(9);
    doc.text(`Emitido em: ${emissao}`, margin, footerY + 10);

    // Gerando e desenhando o QR Code
    const urlValidacao = `${window.location.origin}/validar/${codigo}/`;
    const canvas = document.createElement('canvas');
    canvas.width = 250;
    canvas.height = 250;
    const qr = new QRious({
        element: canvas,
        value: urlValidacao,
        size: 250,
        level: 'H'
    });
    const qrImageBase64 = canvas.toDataURL('image/jpeg');

    // Desenha o QR Code e instruções alinhados à direita
    doc.addImage(qrImageBase64, 'JPEG', pageW - margin - 26, footerY - 14, 26, 26, undefined, 'FAST');
    doc.setFontSize(7);
    doc.text('Aponte a câmera para validar', pageW - margin - 28, footerY + 16);

    // Rodapé
    doc.setFillColor(24, 125, 117);
    doc.rect(0, 282, pageW, 15, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(8);
    doc.text(
        `IFBA - Campus Porto Seguro | Valide em: ${urlValidacao}`,
        pageW / 2, 291, { align: 'center' }
    );

    doc.save(`declaracao_${codigo}.pdf`);
}