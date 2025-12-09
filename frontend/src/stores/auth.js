import { defineStore } from 'pinia';
import { api } from 'boot/axios'; // <--- DESCOMENTADO AGORA

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || '',
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(username, password) {
      try {
        // 1. Faz o POST no Django
        const response = await api.post('/api/login/', { 
          username: username, 
          password: password 
        });

        // 2. O Django retorna algo como { "token": "9944b09..." }
        this.token = response.data.token;
        
        // 3. Salva no navegador para não deslogar ao atualizar a página
        localStorage.setItem('token', this.token);
        
        // 4. Configura o Axios para enviar esse token em todas as futuras requisições
        api.defaults.headers.common['Authorization'] = `Token ${this.token}`;

        // (Opcional) Aqui poderíamos buscar os dados do usuário (nome, email) em outra rota
        
      } catch (error) {
        console.error("Erro no login:", error.response?.data || error.message);
        // Repassa o erro para a tela de login mostrar o alert
        throw error;
      }
    },

    logout() {
      this.token = '';
      this.user = null;
      localStorage.removeItem('token');
      // Remove o cabeçalho de autorização
      delete api.defaults.headers.common['Authorization'];
    }
  }
});