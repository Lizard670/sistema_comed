-- Usuarios
INSERT INTO auth_user (username, first_name, email, password, is_superuser, is_staff, is_active, date_joined)
VALUES 
('joao.silva',     'João Silva',     'joao.silva@escola.com',     'pbkdf2_sha256$123456$abcdef', 1, 1, 1, datetime('now', '-30 days')),
('maria.santos',   'Maria Santos',   'maria.santos@escola.com',   'pbkdf2_sha256$123456$abcdef', 1, 1, 1, datetime('now', '-25 days')),
('carlos.pereira', 'Carlos Pereira', 'carlos.pereira@escola.com', 'pbkdf2_sha256$123456$abcdef', 1, 1, 1, datetime('now', '-20 days')),
('ana.oliveira',   'Ana Oliveira',   'ana.oliveira@escola.com',   'pbkdf2_sha256$123456$abcdef', 1, 1, 1, datetime('now', '-15 days'));

INSERT INTO usuario (matricula, nascimento, user_id, created_at, updated_at)
VALUES 
('2023001', '1990-05-15', 1, datetime('now', '-30 days'), datetime('now', '-5 days')),
('2023002', '1985-08-20', 2, datetime('now', '-25 days'), datetime('now', '-3 days')),
('2023003', '1992-12-10', 3, datetime('now', '-20 days'), datetime('now', '-1 day')),
('2023004', '1988-03-25', 4, datetime('now', '-15 days'), datetime('now'));



-- Cursos
INSERT INTO curso (nome, created_at, updated_at)
VALUES 
('Técnico em informática',      datetime('now', '-60 days'), datetime('now', '-10 days')),
('Técnico em alimentos',        datetime('now', '-55 days'), datetime('now', '-8 days')),
('Técnico em bio combustiveis', datetime('now', '-50 days'), datetime('now', '-6 days'));



-- Turmas
INSERT INTO turma (nome, curso_id, created_at, updated_at)
VALUES 
('1TIA', 1, datetime('now'), datetime('now')),
('1TIB', 1, datetime('now'), datetime('now')),
('1TAA', 2, datetime('now'), datetime('now')),
('1TAB', 2, datetime('now'), datetime('now')),
('1TBA', 3, datetime('now'), datetime('now')),
('1TBB', 3, datetime('now'), datetime('now')),
('2TI',  1, datetime('now'), datetime('now')),
('2TA',  2, datetime('now'), datetime('now')),
('2TB',  3, datetime('now'), datetime('now')),
('3TI',  1, datetime('now'), datetime('now')),
('3TA',  2, datetime('now'), datetime('now')),
('3TB',  3, datetime('now'), datetime('now')),
('4TI',  1, datetime('now'), datetime('now')),
('4TA',  2, datetime('now'), datetime('now')),
('4TB',  3, datetime('now'), datetime('now'));



-- Alunos
INSERT INTO aluno (
    matricula, 
    nome, 
    nascimento, 
    nome_responsavel, 
    peso, 
    altura, 
    medicamentos, 
    restricoes, 
    observacoes, 
    tipo_sanguineo, 
    turma_id, 
    created_at, 
    updated_at
) VALUES 
('20261981001', 'João Victor Santos Silva',  '2010-03-15', 'Maria Aparecida Silva', 68.50, 1.76, 'Nenhum', 'Alergia a dipirona', 'Pratica futebol regularmente',      'O+',   1, datetime('now', '-30 days'), datetime('now', '-5 days')),
('20261981002', 'Ana Clara Oliveira Souza',  '2010-07-22', 'José Carlos Oliveira',  58.20, 1.63, 'Nenhum', 'Nenhuma', 'Aluna com excelente desempenho acadêmico',     'A+',   1, datetime('now', '-28 days'), datetime('now', '-4 days')),
('20261981003', 'Lucas Gabriel Almeida',     '2010-11-05', 'Patrícia Almeida',      70.30, 1.78, 'Nenhum', 'Asma leve', 'Necessita de inalador em caso de crise',     'B+',   2, datetime('now', '-26 days'), datetime('now', '-3 days')),
('20261981004', 'Mariana Costa Rodrigues',   '2011-09-18', 'Fernanda Costa',        56.80, 1.60, 'Nenhum', 'Alergia a frutos do mar', 'Nenhuma',                      'AB-',  2, datetime('now', '-24 days'), datetime('now', '-2 days')),
('20261982005', 'Rafael Henrique Pereira',   '2010-04-30', 'Carla Pereira',         72.00, 1.82, 'Nenhum', 'Nenhuma', 'Atleta de basquete',                           'O-',   3, datetime('now', '-22 days'), datetime('now', '-1 day')),
('20261982006', 'Isabela Martins Lima',      '2011-12-12', 'Roberto Martins',       55.30, 1.59, 'Nenhum', 'Alergia a penicilina', 'Nenhuma',                         'A-',   3, datetime('now', '-20 days'), datetime('now')),
('20261982007', 'Gabriel Fernandes Rocha',   '2010-06-25', 'Ana Fernandes',         69.20, 1.75, 'Nenhum', 'Nenhuma', 'Tem histórico de enxaqueca',                   'B-',   4, datetime('now', '-18 days'), datetime('now', '-2 days')),
('20261982008', 'Beatriz Santos Oliveira',   '2011-08-14', 'Paulo Santos',          54.80, 1.58, 'Nenhum', 'Alergia a amendoim', 'Aluna com baixa visão, usa óculos', 'O+',   4, datetime('now', '-16 days'), datetime('now', '-1 day')),
('20261983009', 'Thiago Henrique Costa',     '2010-02-10', 'Cláudia Costa',         65.40, 1.70, 'Nenhum', 'Nenhuma', 'Aluno com TDAH diagnosticado',                 'A+',   5, datetime('now', '-14 days'), datetime('now', '-3 days')),
('20231983029', 'Noah Miguel Souza',         '2007-10-08', 'Renata Souza',          74.00, 1.82, 'Nenhum', 'Nenhuma', 'Nenhuma',                                      'B+',  15, datetime('now', '-27 days'), datetime('now', '-13 days')),
('20231983030', 'Alice Santos Lima',         '2007-06-19', 'Marcos Lima',           56.90, 1.60, 'Nenhum', 'Asma', 'Nenhuma',                                         'O+',  15, datetime('now', '-29 days'), datetime('now', '-14 days'));



-- Prontuarios
INSERT INTO prontuario (
    data, 
    horario_inicio, 
    horario_fim, 
    descricao, 
    tipo_atendimento, 
    status, 
    aluno_id, 
    usuario_id, 
    created_at, 
    updated_at
) VALUES 
('2026-06-10', '08:30:00', '09:00:00', 'Consulta de rotina - aluno apresenta bom desenvolvimento físico. Peso e altura dentro dos parâmetros esperados para a idade. Sem queixas.',  'consulta', 'finalizado',   1, 1, datetime('now', '-15 days'), datetime('now', '-12 days')),
('2026-06-12', '09:15:00', '09:45:00', 'Aluna relatou dor de cabeça intensa. Aferida pressão arterial normal. Administrado analgésico. Orientado repouso e hidratação.',             'urgencia', 'finalizado',   2, 2, datetime('now', '-13 days'), datetime('now', '-10 days')),
('2026-05-14', '10:00:00', '10:30:00', 'Crise asmática leve. Administrado broncodilatador via inalação. Paciente melhorou após 15 minutos. Orientado procurar pneumologista.',       'urgencia', 'finalizado',   3, 3, datetime('now', '-11 days'), datetime('now', '-8 days')),
('2026-05-15', '11:00:00', '11:30:00', 'Consulta de retorno para avaliação de alergia alimentar. Aluna apresenta melhora significativa. Mantido acompanhamento.',                    'retorno',  'finalizado',   4, 4, datetime('now', '-10 days'), datetime('now', '-7 days')),
('2026-05-16', '13:30:00', '14:00:00', 'Avaliação pré-participação esportiva. Aluno saudável, apto para atividades físicas. Realizado exame físico completo.',                       'consulta', 'finalizado',   5, 1, datetime('now', '-9 days'),  datetime('now', '-6 days')),
('2026-04-17', '14:30:00', '15:00:00', 'Aluna com reação alérgica leve após contato com gato. Administrado anti-histamínico. Sintomas controlados.',                                 'urgencia', 'finalizado',   6, 2, datetime('now', '-8 days'),  datetime('now', '-5 days')),
('2026-04-18', '08:00:00', '08:30:00', 'Aluno relatou episódio de enxaqueca. Realizado avaliação neurológica básica. Orientado manter registro de crises.',                          'consulta', 'encaminhado',  7, 3, datetime('now', '-7 days'),  datetime('now', '-4 days')),
('2026-04-19', '09:45:00', '10:15:00', 'Aluna com baixa visão - consulta para atualização de receita de óculos. Avaliação oftalmológica realizada.',                                 'consulta', 'finalizado',   8, 4, datetime('now', '-6 days'),  datetime('now', '-3 days')),
('2026-04-20', '10:30:00', '11:00:00', 'Acompanhamento de TDAH. Aluno relata melhora com medicação atual. Mantido tratamento.',                                                      'retorno',  'finalizado',   9, 1, datetime('now', '-5 days'),  datetime('now', '-2 days')),
('2026-04-21', '11:15:00', '11:45:00', 'Aluna com alergia a látex - orientações sobre prevenção e cuidados. Emitido alerta para equipe escolar.',                                    'consulta', 'finalizado',  10, 2, datetime('now', '-4 days'),  datetime('now', '-1 day')),
('2026-04-22', '13:00:00', '13:30:00', 'Consulta de acompanhamento para controle de peso. Aluno perdeu 2kg desde última consulta. Reforçada orientação alimentar.',                  'retorno',  'finalizado',  11, 3, datetime('now', '-3 days'),  datetime('now')),
('2026-03-23', '14:00:00', '14:30:00', 'Aluna com anemia - consulta para acompanhamento. Exames mostram melhora com suplementação. Mantido tratamento.',                             'retorno',  'finalizado',  12, 4, datetime('now', '-2 days'),  datetime('now', '-1 day')),
('2026-03-24', '08:15:00', '08:45:00', 'Consulta de rotina - aluno saudável. Vacinação em dia. Sem intercorrências.',                                                                'consulta', 'finalizado',  13, 1, datetime('now', '-1 day'),   datetime('now')),
('2026-02-25', '09:00:00', '09:30:00', 'Aluna com crise alérgica devido contato com gatos. Administrado antialérgico. Sintomas controlados em 30 minutos.',                          'urgencia', 'finalizado',  14, 2, datetime('now'),             datetime('now', '+1 day')),
('2026-02-26', '10:00:00', '10:30:00', 'Aluno com dor no ombro após treino de natação. Realizada avaliação ortopédica. Orientado repouso e aplicação de gelo.',                      'consulta', 'aberto',      15, 3, datetime('now', '+1 day'),   datetime('now', '+2 days')),
('2026-02-27', '11:00:00', '11:30:00', 'Aluna com alergia a poeira - orientações para ambiente escolar. Emitido relatório para coordenadores.',                                      'consulta', 'finalizado',  16, 4, datetime('now', '+2 days'),  datetime('now', '+3 days')),
('2026-02-28', '13:30:00', '14:00:00', 'Aluno com dor de cabeça e febre. Aferido temperatura 38.2°C. Orientado repouso e administrado antitérmico. Aguardando evolução.',            'urgencia', 'aberto',      17, 1, datetime('now', '+3 days'),  datetime('now', '+4 days')),
('2026-02-01', '09:30:00', '10:00:00', 'Aluna com crise asmática leve. Administrado broncodilatador. Melhora após 20 minutos. Orientado uso preventivo.',                            'urgencia', 'finalizado',  20, 4, datetime('now', '+6 days'),  datetime('now', '+7 days')),
('2026-01-02', '10:30:00', '11:00:00', 'Aluno com lesão no ombro durante treino de vôlei. Realizada avaliação ortopédica. Suspeita de tendinite. Encaminhado para especialista.',    'urgencia', 'encaminhado', 21, 1, datetime('now', '+7 days'),  datetime('now', '+8 days')),
('2025-11-29', '14:30:00', '15:00:00', 'Aluna com reação alérgica a amendoim. Administrado anti-histamínico e acompanhamento. Melhora significativa após intervenção.',              'urgencia', 'finalizado',  18, 2, datetime('now', '+4 days'),  datetime('now', '+5 days')),
('2025-12-30', '08:00:00', '08:30:00', 'Consulta de rotina - aluno apto para atividades físicas. Exame físico completo sem alterações.',                                             'consulta', 'finalizado',  19, 3, datetime('now', '+5 days'),  datetime('now', '+6 days')),
('2025-11-03', '11:30:00', '12:00:00', 'Aluna com alergia a dipirona - atualização de prontuário e orientações para equipe escolar. Alerta incluído no sistema.',                    'consulta', 'finalizado',  22, 2, datetime('now', '+8 days'),  datetime('now', '+9 days'));