<template>
  <q-page class="q-pa-md">
    
    <q-table
      title="Minhas Credenciais"
      :rows="rows"
      :columns="columns"
      row-key="id"
      :filter="filter"
      :loading="loading"
    >
      <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Buscar">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
        
        <q-btn 
          color="primary" 
          icon="vpn_key" 
          label="Nova Credencial" 
          class="q-ml-md" 
          @click="openDialog()"
        />
      </template>

      <template v-slot:body-cell-portal_password="props">
        <q-td :props="props">
          ••••••••
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props" align="right">
          <q-btn flat round color="blue" icon="edit" size="sm" @click="openDialog(props.row)">
            <q-tooltip>Editar</q-tooltip>
          </q-btn>
          <q-btn flat round color="red" icon="delete" size="sm" @click="deleteCredential(props.row)">
            <q-tooltip>Excluir</q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="dialog" persistent>
      <q-card style="width: 500px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">{{ isEditing ? 'Editar Credencial' : 'Nova Credencial' }}</div>
          <div class="text-caption text-grey">Dados de acesso que o robô usará</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-form @submit="saveCredential" class="q-gutter-md">
            
            <q-select
              filled
              v-model="form.portal"
              :options="portalOptions"
              label="Selecione o Portal *"
              option-value="id"
              option-label="name"
              emit-value
              map-options
              :rules="[val => !!val || 'Obrigatório']"
            >
              <template v-slot:option="scope">
                <q-item v-bind="scope.itemProps">
                  <q-item-section avatar v-if="scope.opt.logo">
                    <q-avatar size="sm">
                      <img :src="scope.opt.logo">
                    </q-avatar>
                  </q-item-section>
                  <q-item-section>
                    <q-item-label>{{ scope.opt.name }}</q-item-label>
                    
                    <q-item-label caption v-if="scope.opt.disable" class="text-positive text-weight-bold">
                      <q-icon name="lock" size="xs" />
                      Login Único
                    </q-item-label>
                    </q-item-section>
                </q-item>
              </template>
            </q-select>

            <q-input 
              filled v-model="form.portal_username" label="Login no Portal *" 
              :rules="[val => !!val || 'Obrigatório']"
            />
            
            <q-input 
              filled v-model="form.portal_password" type="text" label="Senha no Portal *" 
              :rules="[val => !!val || 'Obrigatório']"
            />

            <div align="right" class="q-mt-md">
              <q-btn flat label="Cancelar" color="primary" v-close-popup />
              <q-btn flat label="Salvar" type="submit" color="primary" :loading="saving" />
            </div>

          </q-form>
        </q-card-section>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<script>
import { ref, onMounted, reactive } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

export default {
  setup () {
    const $q = useQuasar()
    const rows = ref([])
    const portalOptions = ref([]) 
    const loading = ref(false)
    const filter = ref('')
    
    const dialog = ref(false)
    const saving = ref(false)
    const isEditing = ref(false)
    const editingId = ref(null)

    const form = reactive({
      portal: null,
      portal_username: '',
      portal_password: ''
    })

    const columns = [
      { name: 'portal_name', label: 'Portal', field: 'portal_name', align: 'left', sortable: true },
      { name: 'portal_username', label: 'Login Utilizado', field: 'portal_username', align: 'left' },
      { name: 'portal_password', label: 'Senha', field: 'portal_password', align: 'left' },
      { name: 'updated_at', label: 'Última Alteração', field: 'updated_at', format: val => new Date(val).toLocaleDateString(), align: 'right' },
      { name: 'actions', label: 'Ações', field: 'actions', align: 'right' }
    ]

    const fetchCredentials = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/credenciais/')
        rows.value = response.data
      } catch {
        $q.notify({ type: 'negative', message: 'Erro ao carregar credenciais' })
      } finally {
        loading.value = false
      }
    }

    // --- AQUI ESTÁ A LÓGICA DE BLOQUEIO ---
    const fetchPortals = async () => {
      try {
        const response = await api.get('/api/portais/')
        // Mapeamos os portais e adicionamos 'disable: true' se for login compartilhado
        portalOptions.value = response.data.map(portal => ({
          ...portal,
          disable: portal.is_shared_login // O Quasar lê essa propriedade automaticamente
        }))
      } catch {
        console.error("Erro ao carregar opções de portais")
      }
    }
    // --------------------------------------

    const openDialog = (row = null) => {
      if (row) {
        isEditing.value = true
        editingId.value = row.id
        form.portal = row.portal
        form.portal_username = row.portal_username
        form.portal_password = row.portal_password 
      } else {
        isEditing.value = false
        editingId.value = null
        form.portal = null
        form.portal_username = ''
        form.portal_password = ''
      }
      dialog.value = true
    }

    const saveCredential = async () => {
      saving.value = true
      try {
        if (isEditing.value) {
          await api.patch(`/api/credenciais/${editingId.value}/`, form)
          $q.notify({ type: 'positive', message: 'Credencial atualizada!' })
        } else {
          await api.post('/api/credenciais/', form)
          $q.notify({ type: 'positive', message: 'Credencial salva!' })
        }

        dialog.value = false
        fetchCredentials()

      } catch (error) {
        if (error.response?.data?.non_field_errors) {
            $q.notify({ type: 'negative', message: 'Você já tem uma credencial para este portal.' })
        } else {
            $q.notify({ type: 'negative', message: 'Erro ao salvar.' })
        }
      } finally {
        saving.value = false
      }
    }

    const deleteCredential = (row) => {
      $q.dialog({
        title: 'Confirmar',
        message: `Excluir credencial do portal ${row.portal_name}?`,
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await api.delete(`/api/credenciais/${row.id}/`)
          $q.notify({ type: 'positive', message: 'Excluído com sucesso.' })
          fetchCredentials()
        } catch {
          $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
        }
      })
    }

    onMounted(() => {
      fetchCredentials()
      fetchPortals()
    })

    return {
      rows, columns, loading, filter, portalOptions,
      dialog, saving, form, isEditing,
      openDialog, saveCredential, deleteCredential
    }
  }
}
</script>