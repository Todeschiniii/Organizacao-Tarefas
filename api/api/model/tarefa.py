# -*- coding: utf-8 -*-
from datetime import datetime, date

class Tarefa:
    def __init__(self):
        """
        Inicializa todos os atributos como atributos de instância.
        """
        self.__id = None
        self.__titulo = None
        self.__concluida = False
        self.__data_limite = None
        self.__projeto_id = None

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
    def concluida(self):
        """
        Getter para concluida
        :return: bool - Status de conclusão da tarefa
        """
        return self.__concluida

    @concluida.setter
    def concluida(self, value):
        """
        Define o status de conclusão da tarefa.

        🔹 Regra de domínio: garante que o valor seja booleano.

        :param value: bool - Status de conclusão da tarefa.
        :raises ValueError: Lança erro se o valor não for booleano.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> tarefa.concluida = True    # ✅ válido
        >>> tarefa.concluida = False   # ✅ válido
        >>> tarefa.concluida = 1       # ❌ lança erro
        >>> tarefa.concluida = "Sim"   # ❌ lança erro
        >>> tarefa.concluida = None    # ❌ lança erro
        """
        if not isinstance(value, bool):
            raise ValueError("concluida deve ser um valor booleano.")

        self.__concluida = value

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

        🔹 CORREÇÃO CRÍTICA: Agora aceita date, string no formato YYYY-MM-DD, ou None.

        :param value: date ou str - Data limite da tarefa.
        :raises ValueError: Lança erro se o valor não for date ou string no formato correto.

        Exemplo:
        >>> tarefa = Tarefa()
        >>> from datetime import date
        >>> tarefa.data_limite = date(2025, 11, 5)   # ✅ válido
        >>> tarefa.data_limite = "2025-11-05"        # ✅ CORREÇÃO: Agora aceita string
        >>> tarefa.data_limite = None                # ✅ válido (None é permitido)
        >>> tarefa.data_limite = "05/11/2025"        # ❌ lança erro (formato inválido)
        """
        if value is None:
            self.__data_limite = None
            return

        # ✅ CORREÇÃO CRÍTICA: Aceita tanto date quanto string
        if isinstance(value, date):
            self.__data_limite = value
        elif isinstance(value, str):
            try:
                # Tenta converter string para date
                self.__data_limite = datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("data_limite deve ser um objeto date, string no formato YYYY-MM-DD ou None.")
        else:
            raise ValueError("data_limite deve ser um objeto date, string no formato YYYY-MM-DD ou None.")

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
        Define o ID do projeto ao qual a tarefa pertence.

        🔹 Regra de domínio: garante que o ID do projeto seja sempre um número inteiro positivo.

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
            raise ValueError("projeto_id deve ser um número inteiro.")

        if parsed <= 0:
            raise ValueError("projeto_id deve ser maior que zero.")

        self.__projeto_id = parsed

    def to_dict(self):
        """
        Converte o objeto Tarefa para dicionário.
        
        :return: dict - Representação em dicionário da tarefa
        """
        return {
            "id": self.__id,
            "titulo": self.__titulo,
            "concluida": self.__concluida,
            "data_limite": self.__data_limite.isoformat() if self.__data_limite else None,
            "projeto_id": self.__projeto_id
        }

    def __str__(self):
        """
        Representação em string do objeto Tarefa.
        """
        return f"Tarefa(id={self.__id}, titulo='{self.__titulo}', concluida={self.__concluida})"

    def __repr__(self):                                            
        """
        Representação oficial do objeto Tarefa.
        """
        return self.__str__()