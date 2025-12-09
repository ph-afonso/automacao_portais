<template>
  <q-page class="window-height window-width row no-wrap">
    
    <div class="col-12 col-md-4 flex flex-center bg-white column q-pa-lg">
      
      <q-img 
        src="~assets/logotipo.png"
        width="240px"
        class="q-mb-xl"
      />
      <div style="width: 100%; max-width: 400px">
        <div class="q-mb-xl">
          <h4 class="text-h4 text-weight-bold q-my-none text-primary">Bem-vindo</h4>
          <p class="text-grey-7">Faça login para acessar o portal de automação.</p>
        </div>

        <q-form @submit="handleLogin" class="q-gutter-md">
          <q-input 
            filled 
            v-model="username" 
            label="Usuário ou E-mail" 
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Digite seu usuário']"
          >
            <template v-slot:prepend>
              <q-icon name="person" />
            </template>
          </q-input>

          <q-input 
            filled 
            v-model="password" 
            type="password" 
            label="Senha" 
            lazy-rules
            :rules="[ val => val && val.length > 0 || 'Digite sua senha']"
          >
            <template v-slot:prepend>
              <q-icon name="lock" />
            </template>
          </q-input>

          <div class="q-mt-lg">
            <q-btn 
              unelevated 
              color="primary" 
              size="lg" 
              label="Acessar Sistema" 
              class="full-width text-weight-bold" 
              type="submit"
              :loading="loading"
            />
          </div>
          
          <div class="text-center q-mt-md">
            <a href="#" class="text-grey-7" style="text-decoration: none; font-size: 0.9em">Esqueceu a senha?</a>
          </div>
        </q-form>
      </div>
    </div>

    <div class="col-md-8 gt-sm">
      <q-img 
        src="https://plus.unsplash.com/premium_photo-1668618511940-924a74bd1283?q=80&w=1121&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        class="window-height"
        fit="cover"
      >
        <div class="absolute-full flex flex-center bg-black-opacity">
          <div class="text-center text-white q-pa-md">

          </div>
        </div>
      </q-img>
    </div>

  </q-page>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from 'stores/auth'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar' // <--- IMPORTANTE

export default {
  setup () {
    const authStore = useAuthStore()
    const router = useRouter()
    const $q = useQuasar() // <--- Inicializa o Quasar
    
    const username = ref('')
    const password = ref('')
    const loading = ref(false)

    const handleLogin = async () => {
      loading.value = true
      try {
        await authStore.login(username.value, password.value)
        
        // Notificação de Sucesso (Opcional)
        $q.notify({
          type: 'positive',
          message: 'Login realizado com sucesso!',
          position: 'top',
          timeout: 2000
        })

        router.push('/') 
      } catch (e) {
        console.error(e)
        
        // Notificação de Erro Bonita
        $q.notify({
          type: 'negative', // Fica vermelho
          message: 'Usuário ou senha incorretos.',
          caption: 'Por favor, tente novamente.',
          position: 'top', // Aparece no topo
          icon: 'error'
        })
        
      } finally {
        loading.value = false
      }
    }

    return { username, password, handleLogin, loading }
  }
}
</script>

<style scoped>
.bg-black-opacity {
  background: rgba(0, 0, 0, 0.4); 
}
</style>