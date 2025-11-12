CREATE DATABASE IF NOT EXISTS projeto;
USE projeto;

-- Tabela de Usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Projetos (CORRIGIDA)
CREATE TABLE IF NOT EXISTS projetos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_inicio DATETIME NULL,  -- ✅ CORREÇÃO: DATETIME
    data_fim DATETIME NULL,     -- ✅ CORREÇÃO: COLUNA ADICIONADA
    status VARCHAR(50) DEFAULT 'pendente',  -- ✅ CORREÇÃO: Status compatível com frontend
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabela de Tarefas (CORRIGIDA)
CREATE TABLE IF NOT EXISTS tarefas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,  -- ✅ CORREÇÃO: COLUNA ADICIONADA
    status VARCHAR(50) DEFAULT 'pendente',  -- ✅ CORREÇÃO: COLUNA ADICIONADA
    prioridade VARCHAR(50) DEFAULT 'media',  -- ✅ CORREÇÃO: COLUNA ADICIONADA
    concluida BOOLEAN DEFAULT FALSE,
    data_limite DATETIME NULL,  -- ✅ CORREÇÃO: DATETIME
    data_inicio DATETIME NULL,  -- ✅ CORREÇÃO: COLUNA ADICIONADA
    data_fim DATETIME NULL,     -- ✅ CORREÇÃO: COLUNA ADICIONADA
    projeto_id INT NOT NULL,
    usuario_id INT NULL,        -- ✅ CORREÇÃO: COLUNA ADICIONADA
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

-- Inserir dados de exemplo
INSERT INTO usuarios (nome, email, senha_hash) VALUES
('Ana Silva', 'ana.silva@email.com', 'hash_da_senha_da_ana'),
('Bruno Costa', 'bruno.costa@email.com', 'hash_da_senha_do_bruno'),
('Carlos Oliveira', 'carlos.oliveira@email.com', 'hash_da_senha_do_carlos'),
('Davi Santos', 'davi@email.com', 'hash_da_senha_do_davi');

-- Inserir projetos (agora com data_fim)
INSERT INTO projetos (nome, descricao, data_inicio, data_fim, status, usuario_id) VALUES
('API de E-commerce', 'Desenvolver a API REST para a nova loja virtual.', '2025-11-01 09:00:00', '2025-12-15 18:00:00', 'andamento', 1),
('Website Institucional', 'Criar o novo site da empresa com um blog integrado.', '2025-10-20 08:30:00', '2025-11-10 17:00:00', 'concluido', 1),
('Aplicativo Mobile de Fitness', 'App para iOS e Android para monitoramento de treinos.', '2026-01-15 10:00:00', '2026-03-20 18:00:00', 'pendente', 2);

-- Inserir tarefas (agora com as novas colunas)
INSERT INTO tarefas (titulo, descricao, status, prioridade, concluida, data_limite, data_inicio, data_fim, projeto_id, usuario_id) VALUES
('Definir endpoints de produtos', 'Definir todos os endpoints da API de produtos', 'concluida', 'alta', TRUE, '2025-11-05 18:00:00', '2025-11-01 09:00:00', '2025-11-03 17:00:00', 1, 1),
('Implementar autenticação JWT', 'Desenvolver sistema de autenticação JWT', 'andamento', 'alta', FALSE, '2025-11-10 18:00:00', '2025-11-04 09:00:00', NULL, 1, 2),
('Criar CRUD de clientes', 'Implementar operações CRUD para clientes', 'pendente', 'media', FALSE, '2025-11-15 18:00:00', NULL, NULL, 1, NULL),
('Criar layout da home page', 'Desenvolver o layout da página inicial', 'concluida', 'alta', TRUE, '2025-10-25 18:00:00', '2025-10-20 08:30:00', '2025-10-24 17:00:00', 2, 1),
('Desenvolver página de contato', 'Criar página de contato com formulário', 'concluida', 'media', TRUE, '2025-11-05 18:00:00', '2025-10-25 09:00:00', '2025-11-02 16:00:00', 2, 2),
('Desenhar telas no Figma', 'Criar protótipo das telas do aplicativo', 'andamento', 'alta', FALSE, '2026-01-30 18:00:00', '2026-01-15 10:00:00', NULL, 3, 3),
('Configurar ambiente React Native', 'Configurar ambiente de desenvolvimento', 'pendente', 'media', FALSE, '2026-02-05 18:00:00', NULL, NULL, 3, NULL);
select *from usuarios