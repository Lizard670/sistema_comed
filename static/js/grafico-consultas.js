// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

document.getElementById('anoGrafico').value = new Date().getFullYear();
function gerarDadosHistograma(anoGrafico) {
    let quant_consultas = [0,0,0,0,0,0,0,0,0,0,0,0]

    for (const prontuario of prontuarios) {
        data_consulta = new Date(prontuario["data"]);
        if (data_consulta.getFullYear() == anoGrafico){
            quant_consultas[data_consulta.getMonth()]++;
        }
    }

    return quant_consultas;
}

function atualizarGraficoConsultas(grafico) {
    const dados = gerarDadosHistograma(document.getElementById("anoGrafico").value);
    // Arredonda para a próxima dezena
    const ymax = Math.ceil((Math.max.apply(Math, dados)+1)/10) * 10;

    grafico.data.datasets[0].data = dados;
    grafico.options = {
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                min: 0,
                max: ymax,
                }
            }],
        },
        legend: {
            display: false
        }
    }
    
    grafico.update();
}


const contextoGraficoConsultas = document.getElementById('graficoConsultas').getContext('2d');
let graficoConsultas = new Chart(contextoGraficoConsultas, {
    type: 'bar',
    data: {
        labels: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
            datasets: [{
            label: "Consultas",
            backgroundColor: 'rgba(54, 162, 235, 0.9)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            data: [0,0,0,0,0,0,0,0,0,0,0,0]
        }]
    },
    options: {
        responsive: true,
        scales: {
            xAxes: [{
                time: {
                    unit: 'mês'
                }
            }],
            yAxes: [{
                ticks: {
                min: 0,
                max: 10,
                }
            }],
        },
        legend: {
            display: false
        }
    }
});

document.getElementById('btnAtualizarGrafico').addEventListener('click', () => {
    atualizarGraficoConsultas(graficoConsultas);
});