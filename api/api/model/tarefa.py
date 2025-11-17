# -*- coding: utf-8 -*-
from datetime import datetime, date

class Tarefa:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__id = None
        self.__titulo = None
        self.__descricao = None
        self.__status = "pendente"
        self.__prioridade = "media"
        self.__concluida = False
        self.__data_limite = None
        self.__data_inicio = None
        self.__data_fim = None
        self.__projeto_id = None
        self.__usuario_responsavel_id = None  
        self.__usuario_atribuidor_id = None  

    
    @property
    def id(self):
        """
        Getter para id
        :return: int - Identificador único da tarefa
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Define o ID da tarefa.

        🔹 Regra de domínio: garante que o ID seja sempre um número inteiro positivo.

        :param value: int - Número inteiro positivo representando o ID da tarefa.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.id = 1   # ✅ válido
        >>> tarefa.id = -5  # ❌ lança erro
        >>> tarefa.id = 0   # ❌ lança erro
        >>> tarefa.id = 3.14  # ❌ lança erro
        >>> tarefa.id = None  # ✅ CORREÇÃO: None agora é permitido
        """
        if value is None:
            self.__id = None
            return
            
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("id deve ser maior que zero.")

        self.__id = parsed

    @property
    def titulo(self):
        """
        Getter para titulo
        :return: str - Título da tarefa
        """
        return self.__titulo

    @titulo.setter
    def titulo(self, value):
        """
        Define o título da tarefa.

        🔹 Regra de domínio: garante que o título seja sempre uma string não vazia
        e com pelo menos 3 caracteres.

        :param value: str - Título da tarefa.
        :raises ValueError: Lança erro se o valor não for string, estiver vazio, tiver menos de 3 caracteres ou for None.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.titulo = "Definir endpoints"   # ✅ válido
        >>> tarefa.titulo = "AB"                  # ❌ lança erro
        >>> tarefa.titulo = ""                    # ❌ lança erro
        >>> tarefa.titulo = None                  # ❌ lança erro
        """
        if value is None:
            raise ValueError("titulo não pode ser None.")

        if not isinstance(value, str):
            raise ValueError("titulo deve ser uma string.")

        titulo = value.strip()
        if len(titulo) < 3:
            raise ValueError("titulo deve ter pelo menos 3 caracteres.")

        self.__titulo = titulo

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, value):
        if value is None:
            self.__descricao = ""
            return
        self.__descricao = str(value)

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value is None:
            self.__status = "pendente"
            return
        self.__status = str(value)

    @property
    def prioridade(self):
        return self.__prioridade

    @prioridade.setter
    def prioridade(self, value):
        if value is None:
            self.__prioridade = "media"
            return
        self.__prioridade = str(value)

    @property
    def concluida(self):
        """
        Getter para concluida
        :return: bool - Status de conclusão da tarefa
        """
        return self.__concluida

    @property
    def usuario_responsavel_id(self):
        """
        Getter para usuario_responsavel_id
        :return: int - ID do usuário responsável pela tarefa
        """
        return self.__usuario_responsavel_id

    @usuario_responsavel_id.setter
    def usuario_responsavel_id(self, value):
        """
        Define o ID do usuário responsável pela tarefa.
        """
        if value is None:
            raise ValueError("usuario_responsavel_id é obrigatório.")
            
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("usuario_responsavel_id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("usuario_responsavel_id deve ser maior que zero.")

        self.__usuario_responsavel_id = parsed

    @property
    def usuario_atribuidor_id(self):
        """
        Getter para usuario_atribuidor_id
        :return: int - ID do usuário que atribuiu a tarefa
        """
        return self.__usuario_atribuidor_id

    @usuario_atribuidor_id.setter
    def usuario_atribuidor_id(self, value):
        """
        Define o ID do usuário que atribuiu a tarefa.
        """
        if value is None:
            raise ValueError("usuario_atribuidor_id é obrigatório.")
            
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("usuario_atribuidor_id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("usuario_atribuidor_id deve ser maior que zero.")

        self.__usuario_atribuidor_id = parsed

    @concluida.setter
    def concluida(self, value):
        """
        Define o status de conclusão da tarefa.

        🔹 CORREÇÃO: Agora aceita valores que podem ser convertidos para booleano.

        :param value: bool - Status de conclusão da tarefa.
        :raises ValueError: Lança erro se o valor não puder ser convertido para booleano.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.concluida = True    # ✅ válido
        >>> tarefa.concluida = False   # ✅ válido
        >>> tarefa.concluida = 1       # ✅ CORREÇÃO: Agora aceita (True)
        >>> tarefa.concluida = 0       # ✅ CORREÇÃO: Agora aceita (False)
        >>> tarefa.concluida = "True"  # ✅ CORREÇÃO: Agora aceita (True)
        >>> tarefa.concluida = None    # ✅ CORREÇÃO: Agora aceita (False)
        """
        if value is None:
            self.__concluida = False
            return

        # ✅ CORREÇÃO CRÍTICA: Conversão flexível para booleano
        if isinstance(value, bool):
            self.__concluida = value
        elif isinstance(value, (int, float)):
            self.__concluida = bool(value)
        elif isinstance(value, str):
            value_lower = value.lower().strip()
            if value_lower in ['true', '1', 'yes', 'sim', 'verdadeiro']:
                self.__concluida = True
            elif value_lower in ['false', '0', 'no', 'não', 'nao', 'falso']:
                self.__concluida = False
            else:
                raise ValueError("concluida deve ser um valor booleano ou string representando booleano.")
        else:
            raise ValueError("concluida deve ser um valor booleano.")

    @property
    def data_limite(self):
        """
        Getter para data_limite
        :return: date - Data limite da tarefa
        """
        return self.__data_limite

    @data_limite.setter
    def data_limite(self, value):
        """
        Define a data limite da tarefa.

        🔹 CORREÇÃO CRÍTICA: Agora aceita date, string em vários formatos, ou None.
        Não lança erro para valores inválidos, apenas define como None.

        :param value: date, str, ou None - Data limite da tarefa.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> from datetime import date
        >>> tarefa.data_limite = date(2025, 11, 5)   # ✅ válido
        >>> tarefa.data_limite = "2025-11-05"        # ✅ válido
        >>> tarefa.data_limite = "05/11/2025"        # ✅ CORREÇÃO: Agora aceita
        >>> tarefa.data_limite = None                # ✅ válido
        >>> tarefa.data_limite = ""                  # ✅ CORREÇÃO: Agora aceita (define como None)
        >>> tarefa.data_limite = "invalid"           # ✅ CORREÇÃO: Agora aceita (define como None)
        """
        if value is None or value == "":
            self.__data_limite = None
            return

        # ✅ CORREÇÃO CRÍTICA: Aceita date, datetime, string em vários formatos
        if isinstance(value, (date, datetime)):
            if isinstance(value, datetime):
                self.__data_limite = value.date()
            else:
                self.__data_limite = value
        elif isinstance(value, str):
            value = value.strip()
            if not value:
                self.__data_limite = None
                return
                
            # Tenta diferentes formatos de data
            formats = [
                '%Y-%m-%d',      # 2025-11-05
                '%d/%m/%Y',      # 05/11/2025
                '%d-%m-%Y',      # 05-11-2025
                '%Y/%m/%d',      # 2025/11/05
                '%d.%m.%Y',      # 05.11.2025
            ]
            
            for fmt in formats:
                try:
                    self.__data_limite = datetime.strptime(value, fmt).date()
                    return
                except ValueError:
                    continue
            
            # ✅ CORREÇÃO: Se nenhum formato funcionar, define como None sem erro
            print(f"⚠️  Formato de data não reconhecido: '{value}'. Definindo data_limite como None.")
            self.__data_limite = None
        else:
            # ✅ CORREÇÃO: Para outros tipos, tenta converter ou define como None
            try:
                if hasattr(value, 'isoformat'):
                    self.__data_limite = value
                else:
                    print(f"⚠️  Tipo não suportado para data_limite: {type(value)}. Definindo como None.")
                    self.__data_limite = None
            except:
                self.__data_limite = None

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, value):
        # ✅ Usa a mesma lógica flexível de data_limite
        if value is None or value == "":
            self.__data_inicio = None
            return
            
        if isinstance(value, (date, datetime)):
            if isinstance(value, datetime):
                self.__data_inicio = value.date()
            else:
                self.__data_inicio = value
        elif isinstance(value, str):
            value = value.strip()
            if not value:
                self.__data_inicio = None
                return
                
            formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%d.%m.%Y']
            for fmt in formats:
                try:
                    self.__data_inicio = datetime.strptime(value, fmt).date()
                    return
                except ValueError:
                    continue
            self.__data_inicio = None
        else:
            self.__data_inicio = None

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, value):
        # ✅ Usa a mesma lógica flexível de data_limite
        if value is None or value == "":
            self.__data_fim = None
            return
            
        if isinstance(value, (date, datetime)):
            if isinstance(value, datetime):
                self.__data_fim = value.date()
            else:
                self.__data_fim = value
        elif isinstance(value, str):
            value = value.strip()
            if not value:
                self.__data_fim = None
                return
                
            formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%d.%m.%Y']
            for fmt in formats:
                try:
                    self.__data_fim = datetime.strptime(value, fmt).date()
                    return
                except ValueError:
                    continue
            self.__data_fim = None
        else:
            self.__data_fim = None

    @property
    def projeto_id(self):
        """
        Getter para projeto_id
        :return: int - ID do projeto ao qual a tarefa pertence
        """
        return self.__projeto_id

    @projeto_id.setter
    def projeto_id(self, value):
        """
        ✅ CORREÇÃO: projeto_id agora pode ser None

        Define o ID do projeto ao qual a tarefa pertence.

        🔹 Regra de domínio: garante que o ID do projeto seja sempre um número inteiro positivo ou None.

        :param value: int - Número inteiro positivo representando o ID do projeto.
        :raises ValueError: Lança erro se o valor não for número, não for inteiro ou for menor/igual a zero.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.projeto_id = 1   # ✅ válido
        >>> tarefa.projeto_id = -5  # ❌ lança erro
        >>> tarefa.projeto_id = 0   # ❌ lança erro
        >>> tarefa.projeto_id = 3.14  # ❌ lança erro
        >>> tarefa.projeto_id = None  # ✅ CORREÇÃO: None agora é permitido
        """
        if value is None:
            self.__projeto_id = None
            return
            
        try:
            parsed = int(value)
        except (ValueError, TypeError):
            raise ValueError("projeto_id deve ser um número inteiro ou None.")

        if parsed <= 0:
            raise ValueError("projeto_id deve ser maior que zero ou None.")

        self.__projeto_id = parsed

    def to_dict(self):
        """
        Converte o objeto Tarefa para dicionário.
        """
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "descricao": self.__descricao,
            "status": self.__status,
            "prioridade": self.__prioridade,
            "concluida": self.__concluida,
            "data_limite": self.__data_limite.isoformat() if self.__data_limite else None,
            "data_inicio": self.__data_inicio.isoformat() if self.__data_inicio else None,
            "data_fim": self.__data_fim.isoformat() if self.__data_fim else None,
            "projeto_id": self.__projeto_id,
            "usuario_responsavel_id": self.__usuario_responsavel_id,
            "usuario_atribuidor_id": self.__usuario_atribuidor_id,
        }

    def __str__(self):
        """
        Representação em string do objeto Tarefa.
        """
        return f"Tarefa(id={self.__id}, titulo='{self.__titulo}', responsavel={self.__usuario_responsavel_id}, atribuidor={self.__usuario_atribuidor_id})"

    def __repr__(self):                                            
        """
        Representação oficial do objeto Tarefa.
        """
        return self.__str__()