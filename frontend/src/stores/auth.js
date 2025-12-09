import { defineStore } from 'pinia';
import { api } from 'boot/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || '',
    loginTime: localStorage.getItem('loginTime') || null, // Novo campo
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    
    // Lógica para pegar iniciais de Nome e Sobrenome (Ex: "Phelipe Afonso" -> "PA")
    userInitials: (state) => {
      // Se tiver first_name e last_name vindo do Django
      if (state.user?.first_name && state.user?.last_name) {
        return (state.user.first_name[0] + state.user.last_name[0]).toUpperCase();
      }
      
      // Se for apenas o username (ex: "phelipe.afonso" ou "Phelipe Afonso")
      const name = state.user?.username || 'U';
      const parts = name.split(/[\s.]+/); // Divide por espaço ou ponto
      
      if (parts.length >= 2) {
        return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
      }
      return name.substring(0, 2).toUpperCase();
    }
  },

  actions: {
    async login(username, password) {
      const response = await api.post('/api/login/', { username, password });

      this.token = response.data.token;
      
      this.user = {
        id: response.data.user_id,
        username: response.data.username,
        email: response.data.email,
        // Dica: No futuro, peça para o Backend enviar first_name e last_name aqui
        first_name: response.data.first_name || '', 
        last_name: response.data.last_name || ''
      };
      
      this.loginTime = Date.now(); // Marca a hora do login

      localStorage.setItem('token', this.token);
      localStorage.setItem('user', JSON.stringify(this.user));
      localStorage.setItem('loginTime', this.loginTime);
      
      api.defaults.headers.common['Authorization'] = `Token ${this.token}`;
    },

    logout() {
      this.token = '';
      this.user = null;
      this.loginTime = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      localStorage.removeItem('loginTime');
      delete api.defaults.headers.common['Authorization'];
    }
  }
});