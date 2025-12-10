<template>
  <q-layout view="lHh Lpr lff" class="bg-grey-2">
    
    <q-drawer
      v-model="drawer"
      show-if-above
      :mini="miniState"
      :width="260"
      :breakpoint="500"
      bordered
      class="bg-white column no-wrap" 
    >
      <div class="row items-center q-pa-md" style="height: 80px;">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          class="text-grey-8"
        />

        <div v-if="!miniState" class="q-ml-md fade-in">
           <img src="~assets/logotipo.png" style="height: 50px;" alt="Logo">
        </div>
      </div>

      <q-separator />

      <q-scroll-area class="col">
        <q-list padding>
          
          <q-item clickable v-ripple to="/" exact active-class="text-primary bg-blue-1 rounded-borders" class="q-ma-xs">
            <q-item-section avatar>
              <q-icon name="dashboard" />
            </q-item-section>
            <q-item-section>Dashboard</q-item-section>
            <q-tooltip v-if="miniState" anchor="center right" self="center left" :offset="[10, 10]">Dashboard</q-tooltip>
          </q-item>

          <q-item clickable v-ripple active-class="text-primary bg-blue-1 rounded-borders" class="q-ma-xs">
            <q-item-section avatar>
              <q-icon name="receipt_long" />
            </q-item-section>
            <q-item-section>Agendamentos</q-item-section>
            <q-tooltip v-if="miniState" anchor="center right" self="center left" :offset="[10, 10]">Agendamentos</q-tooltip>
          </q-item>

          <q-item clickable v-ripple active-class="text-primary bg-blue-1 rounded-borders" class="q-ma-xs">
            <q-item-section avatar>
              <q-icon name="smart_toy" />
            </q-item-section>
            <q-item-section>Automações</q-item-section>
            <q-tooltip v-if="miniState" anchor="center right" self="center left" :offset="[10, 10]">Automações</q-tooltip>
          </q-item>

          <q-separator class="q-my-md" />

          <q-expansion-item
            icon="settings"
            label="Configurações"
            :content-inset-level="0.5"
            expand-separator
            group="settings" 
            :class="miniState ? 'q-ma-xs' : ''" 
            :header-class="route.path.includes('/configuracoes') ? 'text-primary' : ''"
          >
            <q-tooltip v-if="miniState" anchor="center right" self="center left" :offset="[10, 10]">
              Configurações
            </q-tooltip>

            <q-item 
              clickable 
              v-ripple 
              to="/configuracoes/portais"
              active-class="text-primary bg-blue-1 rounded-borders"
              class="q-ma-xs"
            >
              <q-item-section avatar>
                <q-icon name="domain" /> 
              </q-item-section>
              <q-item-section>
                Portais
              </q-item-section>
            </q-item>
          </q-expansion-item>

        </q-list>
      </q-scroll-area>

      <q-separator />

      <div class="bg-grey-1 q-pa-sm">
        <div v-if="!miniState" class="row items-center justify-between q-pa-sm fade-in">
          
          <div class="row items-center">
            <q-avatar size="38px" color="primary" text-color="white" class="text-weight-bold">
              {{ authStore.userInitials }}
            </q-avatar>
            
            <div class="column q-ml-sm">
              <div class="text-weight-bold text-grey-9 text-body2">
                {{ formatName(authStore.user?.first_name) }} {{ formatName(authStore.user?.last_name) }} 
              </div>
              <div class="text-caption text-grey-6 flex items-center">
                <q-icon name="schedule" size="10px" class="q-mr-xs" />
                {{ sessionDuration }}
              </div>
            </div>
          </div>

          <q-btn 
            flat 
            round 
            dense 
            icon="logout" 
            color="red-4" 
            size="sm"
            @click="handleLogout"
          >
            <q-tooltip>Sair</q-tooltip>
          </q-btn>
        </div>

        <div v-else class="column items-center q-py-sm">
           <q-avatar size="36px" color="primary" text-color="white" class="cursor-pointer" @click="handleLogout">
              {{ authStore.userInitials }}
              <q-tooltip>Sair ({{ sessionDuration }})</q-tooltip>
            </q-avatar>
        </div>
      </div>

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

  </q-layout>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from 'stores/auth'
import { useRouter, useRoute } from 'vue-router' // ADICIONADO useRoute
import { useQuasar } from 'quasar'

export default {
  setup () {
    const authStore = useAuthStore()
    const router = useRouter()
    const route = useRoute() // ADICIONADO
    const $q = useQuasar()

    const drawer = ref(false)
    const miniState = ref(false)
    const sessionDuration = ref('00:00:00')
    let timerInterval = null

    const toggleLeftDrawer = () => {
      if ($q.screen.gt.sm) {
        miniState.value = !miniState.value
      } else {
        drawer.value = !drawer.value
      }
    }

    const formatName = (name) => {
      if (!name) return ''; // Ajustei para não retornar "Usuário" fixo se faltar um dos nomes
      return name.charAt(0).toUpperCase() + name.slice(1);
    }

    const updateTimer = () => {
      if (!authStore.loginTime) return;
      
      const now = Date.now();
      const diff = now - parseInt(authStore.loginTime);
      
      const hours = Math.floor(diff / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);

      const pad = (num) => num.toString().padStart(2, '0');
      sessionDuration.value = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
    }

    const handleLogout = () => {
      $q.dialog({
        title: 'Sair',
        message: 'Encerrar sessão?',
        cancel: true,
        persistent: true
      }).onOk(() => {
        authStore.logout()
        router.push('/login')
        $q.notify({ type: 'positive', position: 'top', message: 'Sessão encerrada.' })
      })
    }

    onMounted(() => {
      updateTimer(); 
      timerInterval = setInterval(updateTimer, 1000); 
    })

    onUnmounted(() => {
      if (timerInterval) clearInterval(timerInterval);
    })

    return {
      drawer,
      miniState,
      toggleLeftDrawer,
      authStore,
      handleLogout,
      sessionDuration,
      formatName,
      route // ADICIONADO retorno para usar no template
    }
  }
}
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

.rounded-borders {
  border-radius: 8px;
}
</style>