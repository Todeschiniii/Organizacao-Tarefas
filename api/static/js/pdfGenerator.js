// js/pdfGenerator.js
class PdfGenerator {
    constructor() {
        this.doc = null;
    }

    async init() {
        // Carrega a biblioteca jsPDF dinamicamente
        if (typeof jspdf === 'undefined') {
            await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
        }
        if (typeof autoTable === 'undefined') {
            await this.loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.28/jspdf.plugin.autotable.min.js');
        }
        
        this.doc = new jspdf.jsPDF();
    }

    loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    // ======================== USUÁRIOS ========================
    generateUsersPDF(usuarios, filtros = '') {
        if (!this.doc) {
            console.error('PDF não inicializado');
            return null;
        }

        try {
            // Configurações do documento
            this.doc.setProperties({
                title: 'Relatório de Usuários - Organização de Tarefas',
                subject: 'Lista de usuários do sistema',
                author: 'Sistema Organização de Tarefas',
                keywords: 'usuários, relatório, pdf',
                creator: 'Organização de Tarefas'
            });

            // Cabeçalho
            this.addHeader('Relatório de Usuários');

            // Informações do relatório
            this.addReportInfo(usuarios.length, filtros, 'usuários');

            // Tabela de usuários
            this.addUsersTable(usuarios);

            // Rodapé
            this.addFooter();

            return this.doc;

        } catch (error) {
            console.error('Erro ao gerar PDF:', error);
            return null;
        }
    }

    addUsersTable(usuarios) {
        const headers = [['ID', 'Nome', 'Email', 'Data de Criação']];
        
        const data = usuarios.map(usuario => [
            usuario.id.toString(),
            usuario.nome || 'Sem nome',
            usuario.email || 'Sem email',
            usuario.data_criacao ? 
                new Date(usuario.data_criacao).toLocaleDateString('pt-BR') : 'N/A'
        ]);

        this.doc.autoTable({
            startY: 65,
            head: headers,
            body: data,
            theme: 'grid',
            styles: {
                fontSize: 9,
                cellPadding: 3,
                lineColor: [200, 200, 200],
                lineWidth: 0.1
            },
            headStyles: {
                fillColor: [102, 126, 234],
                textColor: [255, 255, 255],
                fontStyle: 'bold',
                lineWidth: 0.1
            },
            alternateRowStyles: {
                fillColor: [245, 247, 250]
            },
            columnStyles: {
                0: { cellWidth: 15 }, // ID
                1: { cellWidth: 60 }, // Nome
                2: { cellWidth: 70 }, // Email
                3: { cellWidth: 35 }  // Data
            },
            margin: { left: 14, right: 14 },
            didDrawPage: (data) => {
                // Adiciona número da página
                const pageCount = this.doc.internal.getNumberOfPages();
                this.doc.setFontSize(8);
                this.doc.setTextColor(100, 100, 100);
                this.doc.text(
                    `Página ${data.pageNumber} de ${pageCount}`,
                    this.doc.internal.pageSize.getWidth() / 2,
                    this.doc.internal.pageSize.getHeight() - 10,
                    { align: 'center' }
                );
            }
        });
    }

    async exportUsersPDF(usuarios, filename = 'usuarios.pdf', filtros = '') {
        try {
            await this.init();
            const pdfDoc = this.generateUsersPDF(usuarios, filtros);
            
            if (pdfDoc) {
                pdfDoc.save(filename);
                return true;
            }
            return false;
            
        } catch (error) {
            console.error('Erro ao exportar PDF:', error);
            return false;
        }
    }

    // ======================== PROJETOS ========================
    generateProjectsPDF(projetos, usuarios, filtros = '') {
        if (!this.doc) {
            console.error('PDF não inicializado');
            return null;
        }

        try {
            // Configurações do documento
            this.doc.setProperties({
                title: 'Relatório de Projetos - Organização de Tarefas',
                subject: 'Lista de projetos do sistema',
                author: 'Sistema Organização de Tarefas',
                keywords: 'projetos, relatório, pdf',
                creator: 'Organização de Tarefas'
            });

            // Cabeçalho
            this.addHeader('Relatório de Projetos');

            // Informações do relatório
            this.addReportInfo(projetos.length, filtros, 'projetos');

            // Tabela de projetos
            this.addProjectsTable(projetos, usuarios);

            // Rodapé
            this.addFooter();

            return this.doc;

        } catch (error) {
            console.error('Erro ao gerar PDF:', error);
            return null;
        }
    }

    addProjectsTable(projetos, usuarios) {
        const headers = [['ID', 'Nome', 'Status', 'Responsável', 'Data Início', 'Data Término']];
        
        const data = projetos.map(projeto => {
            const responsavel = usuarios.find(u => u.id === projeto.usuario_id);
            return [
                projeto.id.toString(),
                projeto.nome || 'Sem nome',
                this.formatarStatus(projeto.status),
                responsavel ? responsavel.nome : 'Não atribuído',
                projeto.data_inicio ? 
                    new Date(projeto.data_inicio).toLocaleDateString('pt-BR') : 'N/A',
                projeto.data_fim ? 
                    new Date(projeto.data_fim).toLocaleDateString('pt-BR') : 'N/A'
            ];
        });

        this.doc.autoTable({
            startY: 65,
            head: headers,
            body: data,
            theme: 'grid',
            styles: {
                fontSize: 9,
                cellPadding: 3,
                lineColor: [200, 200, 200],
                lineWidth: 0.1
            },
            headStyles: {
                fillColor: [102, 126, 234],
                textColor: [255, 255, 255],
                fontStyle: 'bold',
                lineWidth: 0.1
            },
            alternateRowStyles: {
                fillColor: [245, 247, 250]
            },
            columnStyles: {
                0: { cellWidth: 15 }, // ID
                1: { cellWidth: 50 }, // Nome
                2: { cellWidth: 30 }, // Status
                3: { cellWidth: 40 }, // Responsável
                4: { cellWidth: 25 }, // Data Início
                5: { cellWidth: 25 }  // Data Término
            },
            margin: { left: 14, right: 14 },
            didDrawPage: (data) => {
                // Adiciona número da página
                const pageCount = this.doc.internal.getNumberOfPages();
                this.doc.setFontSize(8);
                this.doc.setTextColor(100, 100, 100);
                this.doc.text(
                    `Página ${data.pageNumber} de ${pageCount}`,
                    this.doc.internal.pageSize.getWidth() / 2,
                    this.doc.internal.pageSize.getHeight() - 10,
                    { align: 'center' }
                );
            }
        });
    }

    async exportProjectsPDF(projetos, usuarios, filename = 'projetos.pdf', filtros = '') {
        try {
            await this.init();
            const pdfDoc = this.generateProjectsPDF(projetos, usuarios, filtros);
            
            if (pdfDoc) {
                pdfDoc.save(filename);
                return true;
            }
            return false;
            
        } catch (error) {
            console.error('Erro ao exportar PDF:', error);
            return false;
        }
    }

    // ======================== TAREFAS ========================
    generateTasksPDF(tarefas, projetos, usuarios, filtros = '') {
        if (!this.doc) {
            console.error('PDF não inicializado');
            return null;
        }

        try {
            // Configurações do documento
            this.doc.setProperties({
                title: 'Relatório de Tarefas - Organização de Tarefas',
                subject: 'Lista de tarefas do sistema',
                author: 'Sistema Organização de Tarefas',
                keywords: 'tarefas, relatório, pdf',
                creator: 'Organização de Tarefas'
            });

            // Cabeçalho
            this.addHeader('Relatório de Tarefas');

            // Informações do relatório
            this.addReportInfo(tarefas.length, filtros, 'tarefas');

            // Tabela de tarefas
            this.addTasksTable(tarefas, projetos, usuarios);

            // Rodapé
            this.addFooter();

            return this.doc;

        } catch (error) {
            console.error('Erro ao gerar PDF:', error);
            return null;
        }
    }

    addTasksTable(tarefas, projetos, usuarios) {
        const headers = [['ID', 'Título', 'Projeto', 'Responsável', 'Status', 'Prioridade', 'Data Limite']];
        
        const data = tarefas.map(tarefa => {
            const projeto = projetos.find(p => p.id === tarefa.projeto_id);
            const responsavel = usuarios.find(u => u.id === tarefa.usuario_responsavel_id);
            
            return [
                tarefa.id.toString(),
                tarefa.titulo || 'Sem título',
                projeto ? projeto.nome : 'N/A',
                responsavel ? responsavel.nome : 'Não atribuído',
                this.formatarStatusTarefa(tarefa.status),
                this.formatarPrioridade(tarefa.prioridade),
                tarefa.data_limite ? 
                    new Date(tarefa.data_limite).toLocaleDateString('pt-BR') : 'N/A'
            ];
        });

        this.doc.autoTable({
            startY: 65,
            head: headers,
            body: data,
            theme: 'grid',
            styles: {
                fontSize: 8,
                cellPadding: 3,
                lineColor: [200, 200, 200],
                lineWidth: 0.1
            },
            headStyles: {
                fillColor: [102, 126, 234],
                textColor: [255, 255, 255],
                fontStyle: 'bold',
                lineWidth: 0.1
            },
            alternateRowStyles: {
                fillColor: [245, 247, 250]
            },
            columnStyles: {
                0: { cellWidth: 15 }, // ID
                1: { cellWidth: 45 }, // Título
                2: { cellWidth: 35 }, // Projeto
                3: { cellWidth: 35 }, // Responsável
                4: { cellWidth: 25 }, // Status
                5: { cellWidth: 20 }, // Prioridade
                6: { cellWidth: 25 }  // Data Limite
            },
            margin: { left: 14, right: 14 },
            didDrawPage: (data) => {
                // Adiciona número da página
                const pageCount = this.doc.internal.getNumberOfPages();
                this.doc.setFontSize(8);
                this.doc.setTextColor(100, 100, 100);
                this.doc.text(
                    `Página ${data.pageNumber} de ${pageCount}`,
                    this.doc.internal.pageSize.getWidth() / 2,
                    this.doc.internal.pageSize.getHeight() - 10,
                    { align: 'center' }
                );
            }
        });
    }

    async exportTasksPDF(tarefas, projetos, usuarios, filename = 'tarefas.pdf', filtros = '') {
        try {
            await this.init();
            const pdfDoc = this.generateTasksPDF(tarefas, projetos, usuarios, filtros);
            
            if (pdfDoc) {
                pdfDoc.save(filename);
                return true;
            }
            return false;
            
        } catch (error) {
            console.error('Erro ao exportar PDF:', error);
            return false;
        }
    }

    // ======================== MÉTODOS AUXILIARES ========================
    addHeader(titulo = 'Relatório') {
        // Logo e título
        this.doc.setFillColor(102, 126, 234);
        this.doc.rect(0, 0, 210, 30, 'F');
        
        this.doc.setTextColor(255, 255, 255);
        this.doc.setFontSize(20);
        this.doc.setFont('helvetica', 'bold');
        this.doc.text('Organização de Tarefas', 105, 15, { align: 'center' });
        
        this.doc.setFontSize(12);
        this.doc.setFont('helvetica', 'normal');
        this.doc.text(titulo, 105, 22, { align: 'center' });
        
        this.doc.setTextColor(0, 0, 0);
    }

    addReportInfo(totalItens, filtros, tipo = 'itens') {
        const dataAtual = new Date().toLocaleDateString('pt-BR');
        const horaAtual = new Date().toLocaleTimeString('pt-BR');
        
        let yPosition = 40;
        
        this.doc.setFontSize(10);
        this.doc.setFont('helvetica', 'bold');
        this.doc.text('Informações do Relatório:', 14, yPosition);
        
        yPosition += 7;
        this.doc.setFont('helvetica', 'normal');
        this.doc.text(`Data de emissão: ${dataAtual} às ${horaAtual}`, 14, yPosition);
        
        yPosition += 5;
        this.doc.text(`Total de ${tipo}: ${totalItens}`, 14, yPosition);
        
        if (filtros) {
            yPosition += 5;
            this.doc.text(`Filtros aplicados: ${filtros}`, 14, yPosition);
        }
        
        // Linha separadora
        yPosition += 8;
        this.doc.setDrawColor(200, 200, 200);
        this.doc.line(14, yPosition, 196, yPosition);
    }

    addFooter() {
        const pageHeight = this.doc.internal.pageSize.getHeight();
        
        this.doc.setFontSize(8);
        this.doc.setTextColor(100, 100, 100);
        this.doc.text(
            'Relatório gerado automaticamente pelo Sistema Organização de Tarefas',
            105,
            pageHeight - 5,
            { align: 'center' }
        );
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
    module.exports = PdfGenerator;
} else {
    window.PdfGenerator = PdfGenerator;
}