// js/csvGenerator.js
class CsvGenerator {
    constructor() {
        this.separator = ',';
        this.lineBreak = '\n';
    }

    // ======================== USUÁRIOS ========================
    generateUsersCSV(usuarios) {
        const headers = ['ID', 'Nome', 'Email', 'Data de Criação'];
        
        const rows = usuarios.map(usuario => [
            usuario.id,
            this.escapeCsvField(usuario.nome || 'Sem nome'),
            this.escapeCsvField(usuario.email || 'Sem email'),
            usuario.data_criacao ? 
                new Date(usuario.data_criacao).toLocaleDateString('pt-BR') : 'N/A'
        ]);

        return this.arrayToCsv([headers, ...rows]);
    }

    exportUsersCSV(usuarios, filename = 'usuarios.csv') {
        try {
            const csvContent = this.generateUsersCSV(usuarios);
            this.downloadCSV(csvContent, filename);
            return true;
        } catch (error) {
            console.error('Erro ao exportar CSV:', error);
            return false;
        }
    }

    // ======================== PROJETOS ========================
    generateProjectsCSV(projetos, usuarios) {
        const headers = ['ID', 'Nome', 'Descrição', 'Status', 'Responsável', 'Data Início', 'Data Término'];
        
        const rows = projetos.map(projeto => {
            const responsavel = usuarios.find(u => u.id === projeto.usuario_id);
            return [
                projeto.id,
                this.escapeCsvField(projeto.nome || 'Sem nome'),
                this.escapeCsvField(projeto.descricao || ''),
                this.formatarStatus(projeto.status),
                this.escapeCsvField(responsavel ? responsavel.nome : 'Não atribuído'),
                projeto.data_inicio ? 
                    new Date(projeto.data_inicio).toLocaleDateString('pt-BR') : 'N/A',
                projeto.data_fim ? 
                    new Date(projeto.data_fim).toLocaleDateString('pt-BR') : 'N/A'
            ];
        });

        return this.arrayToCsv([headers, ...rows]);
    }

    exportProjectsCSV(projetos, usuarios, filename = 'projetos.csv') {
        try {
            const csvContent = this.generateProjectsCSV(projetos, usuarios);
            this.downloadCSV(csvContent, filename);
            return true;
        } catch (error) {
            console.error('Erro ao exportar CSV:', error);
            return false;
        }
    }

    // ======================== TAREFAS ========================
    generateTasksCSV(tarefas, projetos, usuarios) {
        const headers = [
            'ID', 'Título', 'Descrição', 'Projeto', 'Responsável', 'Atribuído por', 
            'Status', 'Prioridade', 'Data Limite', 'Data Início', 'Data Fim', 'Concluída'
        ];
        
        const rows = tarefas.map(tarefa => {
            const projeto = projetos.find(p => p.id === tarefa.projeto_id);
            const responsavel = usuarios.find(u => u.id === tarefa.usuario_responsavel_id);
            const atribuidor = usuarios.find(u => u.id === tarefa.usuario_atribuidor_id);

            return [
                tarefa.id,
                this.escapeCsvField(tarefa.titulo || 'Sem título'),
                this.escapeCsvField(tarefa.descricao || ''),
                this.escapeCsvField(projeto ? projeto.nome : 'N/A'),
                this.escapeCsvField(responsavel ? responsavel.nome : 'N/A'),
                this.escapeCsvField(atribuidor ? atribuidor.nome : 'N/A'),
                this.formatarStatusTarefa(tarefa.status),
                this.formatarPrioridade(tarefa.prioridade),
                tarefa.data_limite ? 
                    new Date(tarefa.data_limite).toLocaleDateString('pt-BR') : 'N/A',
                tarefa.data_inicio ? 
                    new Date(tarefa.data_inicio).toLocaleDateString('pt-BR') : 'N/A',
                tarefa.data_fim ? 
                    new Date(tarefa.data_fim).toLocaleDateString('pt-BR') : 'N/A',
                tarefa.concluida ? 'Sim' : 'Não'
            ];
        });

        return this.arrayToCsv([headers, ...rows]);
    }

    exportTasksCSV(tarefas, projetos, usuarios, filename = 'tarefas.csv') {
        try {
            const csvContent = this.generateTasksCSV(tarefas, projetos, usuarios);
            this.downloadCSV(csvContent, filename);
            return true;
        } catch (error) {
            console.error('Erro ao exportar CSV:', error);
            return false;
        }
    }

    // ======================== MÉTODOS AUXILIARES ========================
    escapeCsvField(field) {
        if (field === null || field === undefined) {
            return '""';
        }
        
        const stringField = String(field);
        
        // Se o campo contém vírgulas, quebras de linha ou aspas, envolve em aspas
        if (stringField.includes(this.separator) || 
            stringField.includes('\n') || 
            stringField.includes('\r') || 
            stringField.includes('"')) {
            return '"' + stringField.replace(/"/g, '""') + '"';
        }
        
        return stringField;
    }

    arrayToCsv(data) {
        return data.map(row => 
            row.map(field => this.escapeCsvField(field)).join(this.separator)
        ).join(this.lineBreak);
    }

    downloadCSV(csvContent, filename) {
        // Adiciona BOM para garantir compatibilidade com Excel
        const BOM = '\uFEFF';
        const blob = new Blob([BOM + csvContent], { 
            type: 'text/csv;charset=utf-8;' 
        });
        
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
    }

    formatarStatus(status) {
        const statusMap = {
            'pendente': 'Pendente',
            'andamento': 'Em Andamento',
            'concluido': 'Concluído'
        };
        return statusMap[status] || status;
    }

    formatarStatusTarefa(status) {
        const statusMap = {
            'pendente': 'Pendente',
            'andamento': 'Em Andamento',
            'concluida': 'Concluída'
        };
        return statusMap[status] || status;
    }

    formatarPrioridade(prioridade) {
        const prioridadeMap = {
            'alta': 'Alta',
            'media': 'Média',
            'baixa': 'Baixa'
        };
        return prioridadeMap[prioridade] || prioridade;
    }
}

// Export para uso em outros arquivos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CsvGenerator;
} else {
    window.CsvGenerator = CsvGenerator;
}