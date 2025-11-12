/**
 * Classe ApiService para facilitar chamadas HTTP (GET, POST, PUT, DELETE) a APIs RESTful.
 * Suporta autenticação via token Bearer e fornece métodos reutilizáveis para diferentes tipos de requisições.
 */
export default class ApiService {
    #token;  // Atributo privado para armazenar o token de autenticação
    #baseURL; // Atributo privado para a URL base da API

    /**
     * Construtor da classe ApiService.
     * @param {string|null} token - Token de autenticação opcional para incluir no header Authorization.
     * @param {string} baseURL - URL base da API (padrão: localhost:5000)
     */
    constructor(token = null, baseURL = "http://localhost:5000") {
        this.#token = token;
        this.#baseURL = baseURL.endsWith('/') ? baseURL.slice(0, -1) : baseURL; // Remove barra final
        console.log(`🔄 ApiService inicializado - BaseURL: ${this.#baseURL}`);
    }

    /**
     * Método para fazer uma requisição GET simples sem headers adicionais.
     * Útil para APIs públicas que não requerem autenticação.
     * @param {string} uri - URL do recurso para a requisição GET.
     * @returns {Promise<Object|Array>} Retorna o JSON obtido da resposta ou array vazio em caso de erro.
     */
    async simpleGet(uri) {
        try {
            const response = await fetch(uri);
            const jsonObj = await response.json();
            console.log("GET:", uri, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("Erro ao buscar dados:", error.message);
            return [];
        }
    }

    /**
     * Método para requisição GET com headers, incluindo token se presente.
     * Usado para APIs que exigem autenticação ou headers customizados.
     * @param {string} uri - URL do recurso para a requisição GET.
     * @returns {Promise<Object>} Retorna JSON da resposta ou objeto de erro padronizado.
     */
    async get(uri) {
        try {
            // ✅ CORREÇÃO: Usa URL completa com baseURL e tratamento de barras
            const cleanUri = uri.startsWith('/') ? uri : `/${uri}`;
            const fullUrl = `${this.#baseURL}${cleanUri}`;
            
            const headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            console.log("🔍 Fazendo GET para:", fullUrl);
            
            const response = await fetch(fullUrl, {
                method: "GET",
                headers: headers,
                mode: 'cors', // ✅ CORREÇÃO: Explicita modo CORS
                credentials: 'include' // ✅ CORREÇÃO: Inclui credenciais
            });

            // ✅ CORREÇÃO MELHORADA: Para CORS, verifica se a resposta foi bloqueada
            if (response.status === 0 || response.type === 'opaque') {
                throw new Error('CORS Policy blocked the request - Verifique a configuração do servidor');
            }

            if (!response.ok) {
                // Tenta obter mensagem de erro da resposta
                let errorMessage = `HTTP Error: ${response.status} ${response.statusText}`;
                try {
                    const errorText = await response.text();
                    if (errorText) {
                        const errorJson = JSON.parse(errorText);
                        errorMessage = errorJson.error?.message || errorJson.message || errorMessage;
                    }
                } catch (e) {
                    // Ignora erro de parse
                }
                throw new Error(errorMessage);
            }

            // ✅ CORREÇÃO: Verifica se a resposta é JSON válido
            const text = await response.text();
            let jsonObj;
            
            try {
                jsonObj = text ? JSON.parse(text) : {};
            } catch (parseError) {
                console.error("❌ Resposta não é JSON válido:", text.substring(0, 100));
                // ✅ CORREÇÃO: Retorna objeto de erro padronizado
                return {
                    success: false,
                    error: {
                        message: `Resposta não é JSON: ${response.status} ${response.statusText}`,
                        code: response.status
                    }
                };
            }

            console.log("✅ GET bem-sucedido:", fullUrl, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("❌ Erro ao buscar dados:", error.message);
            // ✅ CORREÇÃO: Retorna objeto de erro padronizado
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 500
                }
            };
        }
    }

    /**
     * Método para buscar um recurso específico pelo ID via GET.
     * Monta a URL com o ID no final e faz a requisição.
     * @param {string} uri - URL base do recurso.
     * @param {string|number} id - Identificador do recurso a ser buscado.
     * @returns {Promise<Object>} Retorna JSON do recurso ou objeto de erro padronizado.
     */
    async getById(uri, id) {
        try {
            // ✅ CORREÇÃO: Remove barra extra na URL
            const cleanUri = uri.endsWith('/') ? uri.slice(0, -1) : uri;
            const fullUrl = `${this.#baseURL}${cleanUri}/${id}`;
            
            const headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            console.log("🔍 Fazendo GET BY ID para:", fullUrl);
            
            const response = await fetch(fullUrl, {
                method: "GET",
                headers: headers,
                mode: 'cors',
                credentials: 'include'
            });

            // ✅ CORREÇÃO: Para CORS, verifica se a resposta foi bloqueada
            if (response.status === 0 || response.type === 'opaque') {
                throw new Error('CORS Policy blocked the request');
            }

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
            }

            const text = await response.text();
            let jsonObj;
            
            try {
                jsonObj = text ? JSON.parse(text) : {};
            } catch (parseError) {
                console.error("❌ Resposta não é JSON válido:", text.substring(0, 100));
                return {
                    success: false,
                    error: {
                        message: `Resposta não é JSON: ${response.status} ${response.statusText}`,
                        code: response.status
                    }
                };
            }

            console.log("✅ GET BY ID bem-sucedido:", fullUrl, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("❌ Erro ao buscar por ID:", error.message);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 500
                }
            };
        }
    }

    /**
     * Método para enviar dados via POST para criar um novo recurso.
     * Envia o objeto JSON serializado no corpo da requisição.
     * @param {string} uri - URL do endpoint para POST.
     * @param {Object} jsonObject - Objeto a ser enviado como corpo JSON.
     * @returns {Promise<Object>} Retorna JSON da resposta ou objeto de erro padronizado.
     */
    async post(uri, jsonObject) {
        try {
            // ✅ CORREÇÃO: Usa URL completa com baseURL e tratamento de barras
            const cleanUri = uri.startsWith('/') ? uri : `/${uri}`;
            const fullUrl = `${this.#baseURL}${cleanUri}`;
            
            const headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            console.log("📤 Fazendo POST para:", fullUrl, jsonObject);
            
            const response = await fetch(fullUrl, {
                method: "POST",
                headers: headers,
                body: JSON.stringify(jsonObject),
                mode: 'cors',
                credentials: 'include'
            });

            // ✅ CORREÇÃO MELHORADA: Para CORS, verifica se a resposta foi bloqueada
            if (response.status === 0 || response.type === 'opaque') {
                throw new Error('CORS Policy blocked the request - Verifique a configuração do servidor Flask');
            }

            if (!response.ok) {
                // Tenta obter mensagem de erro da resposta
                let errorMessage = `HTTP Error: ${response.status} ${response.statusText}`;
                try {
                    const errorText = await response.text();
                    if (errorText) {
                        const errorJson = JSON.parse(errorText);
                        errorMessage = errorJson.error?.message || errorJson.message || errorMessage;
                    }
                } catch (e) {
                    // Ignora erro de parse
                }
                throw new Error(errorMessage);
            }

            const text = await response.text();
            let jsonObj;
            
            try {
                jsonObj = text ? JSON.parse(text) : {};
            } catch (parseError) {
                console.error("❌ Resposta não é JSON válido:", text.substring(0, 100));
                return {
                    success: false,
                    error: {
                        message: `Resposta não é JSON: ${response.status} ${response.statusText}`,
                        code: response.status
                    }
                };
            }

            console.log("✅ POST bem-sucedido:", fullUrl, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("❌ Erro ao fazer POST:", error.message);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 500
                }
            };
        }
    }

    /**
     * Método para atualizar um recurso via PUT usando ID e objeto JSON.
     * @param {string} uri - URL base do recurso.
     * @param {string|number} id - ID do recurso a ser atualizado.
     * @param {Object} jsonObject - Dados atualizados a serem enviados no corpo da requisição.
     * @returns {Promise<Object>} Retorna JSON da resposta ou objeto de erro padronizado.
     */
    async put(uri, id, jsonObject) {
        try {
            // ✅ CORREÇÃO CRÍTICA: Remove barra extra para evitar URLs com "//"
            const cleanUri = uri.endsWith('/') ? uri.slice(0, -1) : uri;
            const fullUrl = `${this.#baseURL}${cleanUri}/${id}`;
            
            const headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            console.log("📤 Fazendo PUT para:", fullUrl, jsonObject);
            
            const response = await fetch(fullUrl, {
                method: "PUT",
                headers: headers,
                body: JSON.stringify(jsonObject),
                mode: 'cors',
                credentials: 'include'
            });

            // ✅ CORREÇÃO: Para CORS, verifica se a resposta foi bloqueada
            if (response.status === 0 || response.type === 'opaque') {
                throw new Error('CORS Policy blocked the request');
            }

            if (!response.ok) {
                // Tenta obter mensagem de erro da resposta
                let errorMessage = `HTTP Error: ${response.status} ${response.statusText}`;
                try {
                    const errorText = await response.text();
                    if (errorText) {
                        const errorJson = JSON.parse(errorText);
                        errorMessage = errorJson.error?.message || errorJson.message || errorMessage;
                    }
                } catch (e) {
                    // Ignora erro de parse
                }
                throw new Error(errorMessage);
            }

            const text = await response.text();
            let jsonObj;
            
            try {
                jsonObj = text ? JSON.parse(text) : {};
            } catch (parseError) {
                console.error("❌ Resposta não é JSON válido:", text.substring(0, 100));
                return {
                    success: false,
                    error: {
                        message: `Resposta não é JSON: ${response.status} ${response.statusText}`,
                        code: response.status
                    }
                };
            }

            console.log("✅ PUT bem-sucedido:", fullUrl, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("❌ Erro ao fazer PUT:", error.message);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 500
                }
            };
        }
    }

    /**
     * Método para deletar um recurso via DELETE usando ID.
     * @param {string} uri - URL base do recurso.
     * @param {string|number} id - ID do recurso a ser deletado.
     * @returns {Promise<Object>} Retorna JSON da resposta ou objeto de erro padronizado.
     */
    async delete(uri, id) {
        try {
            // ✅ CORREÇÃO: Remove barra extra na URL
            const cleanUri = uri.endsWith('/') ? uri.slice(0, -1) : uri;
            const fullUrl = `${this.#baseURL}${cleanUri}/${id}`;
            
            const headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            };

            if (this.#token) {
                headers["Authorization"] = `Bearer ${this.#token}`;
            }

            console.log("🗑️  Fazendo DELETE para:", fullUrl);
            
            const response = await fetch(fullUrl, {
                method: "DELETE",
                headers: headers,
                mode: 'cors',
                credentials: 'include'
            });

            // ✅ CORREÇÃO: Para CORS, verifica se a resposta foi bloqueada
            if (response.status === 0 || response.type === 'opaque') {
                throw new Error('CORS Policy blocked the request');
            }

            if (!response.ok) {
                // Tenta obter mensagem de erro da resposta
                let errorMessage = `HTTP Error: ${response.status} ${response.statusText}`;
                try {
                    const errorText = await response.text();
                    if (errorText) {
                        const errorJson = JSON.parse(errorText);
                        errorMessage = errorJson.error?.message || errorJson.message || errorMessage;
                    }
                } catch (e) {
                    // Ignora erro de parse
                }
                throw new Error(errorMessage);
            }

            const text = await response.text();
            let jsonObj;
            
            try {
                jsonObj = text ? JSON.parse(text) : {};
            } catch (parseError) {
                console.error("❌ Resposta não é JSON válido:", text.substring(0, 100));
                return {
                    success: false,
                    error: {
                        message: `Resposta não é JSON: ${response.status} ${response.statusText}`,
                        code: response.status
                    }
                };
            }

            console.log("✅ DELETE bem-sucedido:", fullUrl, jsonObj);
            return jsonObj;

        } catch (error) {
            console.error("❌ Erro ao deletar dados:", error.message);
            return {
                success: false,
                error: {
                    message: error.message,
                    code: 500
                }
            };
        }
    }

    /**
     * Getter para o token privado.
     * @returns {string|null} Retorna o token atual.
     */
    get token() {
        return this.#token;
    }

    /**
     * Setter para atualizar o token privado.
     * @param {string} value - Novo token a ser setado.
     */
    set token(value) {
        this.#token = value;
    }

    /**
     * Getter para a URL base.
     * @returns {string} Retorna a URL base atual.
     */
    get baseURL() {
        return this.#baseURL;
    }

    /**
     * Setter para atualizar a URL base.
     * @param {string} value - Nova URL base.
     */
    set baseURL(value) {
        this.#baseURL = value;
    }
}