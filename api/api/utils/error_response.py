# -*- coding: utf-8 -*-

"""
Classe personalizada de erro para a aplicação.

Estende a classe nativa Exception do Python para incluir:
- Código HTTP (httpCode)
- Informações adicionais sobre o erro (error)

Pode ser utilizada em middlewares ou serviços para padronizar respostas de erro.
"""
class ErrorResponse(Exception):
    def __init__(self, httpCode: int, message: str, error: any = None):
        """
        Construtor da classe ErrorResponse

        :param httpCode: Código de status HTTP (ex: 400, 404, 500)
        :param message: Mensagem de erro descritiva
        :param error: Objeto adicional com detalhes do erro (opcional)
        """
        super().__init__(message)
        self.__httpCode = httpCode
        self.__message = message  # ✅ CORREÇÃO: Armazena a mensagem
        self.__error = error

    @property
    def status_code(self) -> int:
        """Retorna o código HTTP associado ao erro"""
        return self.__httpCode

    @property
    def message(self) -> str:
        """✅ CORREÇÃO: Retorna a mensagem de erro"""
        return self.__message

    @property
    def details(self):
        """Retorna informações adicionais sobre o erro"""
        return self.__error

    def __str__(self) -> str:
        """Representação textual do erro"""
        return f"[{self.__httpCode}] {self.__message} | Detalhes: {self.__error}"