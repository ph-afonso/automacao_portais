<template>
  <q-page class="q-pa-md">
    
    <q-table
      title="Portais Cadastrados"
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
          icon="add" 
          label="Novo Portal" 
          class="q-ml-md" 
          @click="openDialog()"
        />
      </template>

      <template v-slot:body-cell-logo="props">
        <q-td :props="props">
          <q-avatar rounded size="40px" v-if="props.value">
            <img :src="props.value">
          </q-avatar>
          <q-icon name="image_not_supported" size="30px" color="grey" v-else />
        </q-td>
      </template>

      <template v-slot:body-cell-is_shared_login="props">
        <q-td :props="props">
          <q-chip 
            :color="props.value ? 'green-2' : 'grey-3'" 
            :text-color="props.value ? 'green-9' : 'grey-8'"
            dense
          >
            {{ props.value ? 'Sim' : 'Não' }}
          </q-chip>
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props" align="right">
          <q-btn flat round color="blue" icon="edit" size="sm" @click="openDialog(props.row)">
            <q-tooltip>Editar</q-tooltip>
          </q-btn>
          <q-btn flat round color="red" icon="delete" size="sm" @click="deletePortal(props.row)">
            <q-tooltip>Excluir</q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="dialog" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        
        <q-card-section>
          <div class="text-h6">{{ isEditing ? 'Editar Portal' : 'Novo Portal' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="savePortal" class="q-gutter-md">
            
            <div class="row q-col-gutter-xs q-pt-xs">
              <div class="col-12 col-md-6">
                <q-input 
                  filled v-model="form.name" label="Nome do Portal *" 
                  :rules="[val => !!val || 'Obrigatório']"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input 
                  filled v-model="form.link" label="Link (URL) *" 
                  :rules="[val => !!val || 'Obrigatório']"
                />
              </div>
            </div>

            <q-file 
              filled bottom-slots v-model="form.logoFile" label="Logotipo" counter
              accept=".jpg, .png, image/*"
            >
              <template v-slot:prepend>
                <q-icon name="cloud_upload" @click.stop />
              </template>
              <template v-slot:hint>
                Deixe vazio para manter a atual
              </template>
            </q-file>

            <q-separator />

            <div class="q-pa-sm bg-grey-1 rounded-borders">
              <q-toggle v-model="form.is_shared_login" label="Este portal usa Login Único (Compartilhado)?" />
              
              <div v-if="form.is_shared_login" class="row q-col-gutter-md q-mt-xs fade-in">
                 <div class="col-12 col-md-6">
                    <q-input filled v-model="form.shared_username" label="Usuário Global" dense />
                 </div>
                 <div class="col-12 col-md-6">
                    <q-input filled v-model="form.shared_password" type="password" label="Senha Global" dense />
                 </div>
              </div>
            </div>

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
    const loading = ref(false)
    const filter = ref('')
    
    // Controle do Modal
    const dialog = ref(false)
    const saving = ref(false)
    const isEditing = ref(false)
    const editingId = ref(null)

    // Formulário
    const form = reactive({
      name: '',
      link: '',
      logoFile: null, // Para o arquivo novo
      is_shared_login: false,
      shared_username: '',
      shared_password: ''
    })

    const columns = [
      { name: 'logo', label: 'Logo', field: 'logo', align: 'left' },
      { name: 'name', label: 'Portal', field: 'name', align: 'left', sortable: true },
      { name: 'link', label: 'Link', field: 'link', align: 'left' },
      { name: 'is_shared_login', label: 'Login Único?', field: 'is_shared_login', align: 'center' },
      { name: 'actions', label: 'Ações', field: 'actions', align: 'right' }
    ]

    // --- AÇÕES ---

    const fetchPortais = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/portais/')
        rows.value = response.data
      } catch {
        $q.notify({ type: 'negative', message: 'Erro ao carregar portais' })
      } finally {
        loading.value = false
      }
    }

    const openDialog = (row = null) => {
      if (row) {
        // Modo Edição
        isEditing.value = true
        editingId.value = row.id
        form.name = row.name
        form.link = row.link
        form.is_shared_login = row.is_shared_login
        form.shared_username = row.shared_username
        form.shared_password = row.shared_password
        form.logoFile = null 
      } else {
        // Modo Criação
        isEditing.value = false
        editingId.value = null
        form.name = ''
        form.link = ''
        form.is_shared_login = false
        form.shared_username = ''
        form.shared_password = ''
        form.logoFile = null
      }
      dialog.value = true
    }

    const savePortal = async () => {
      saving.value = true
      try {
        // TRUQUE: Para enviar arquivos (imagem), precisamos usar FormData
        // Não dá para enviar JSON simples quando tem upload
        const formData = new FormData()
        formData.append('name', form.name)
        formData.append('link', form.link)
        formData.append('is_shared_login', form.is_shared_login ? 'True' : 'False') // Django espera string bool no Formdata
        if (form.shared_username) formData.append('shared_username', form.shared_username)
        if (form.shared_password) formData.append('shared_password', form.shared_password)
        
        // Só anexa a imagem se o usuário selecionou uma nova
        if (form.logoFile) {
          formData.append('logo', form.logoFile)
        }

        if (isEditing.value) {
          // PUT (Atualizar) - Atenção: Para upload de arquivo em PUT, às vezes o Django prefere PATCH
          await api.patch(`/api/portais/${editingId.value}/`, formData, {
             headers: { 'Content-Type': 'multipart/form-data' }
          })
          $q.notify({ type: 'positive', message: 'Portal atualizado!' })
        } else {
          // POST (Criar)
          await api.post('/api/portais/', formData, {
             headers: { 'Content-Type': 'multipart/form-data' }
          })
          $q.notify({ type: 'positive', message: 'Portal criado!' })
        }

        dialog.value = false
        fetchPortais() // Recarrega a tabela

      } catch (error) {
        console.error(error)
        $q.notify({ type: 'negative', message: 'Erro ao salvar. Verifique os dados.' })
      } finally {
        saving.value = false
      }
    }

    const deletePortal = (row) => {
      $q.dialog({
        title: 'Confirmar Exclusão',
        message: `Deseja excluir o portal "${row.name}"?`,
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await api.delete(`/api/portais/${row.id}/`)
          $q.notify({ type: 'positive', message: 'Portal excluído.' })
          fetchPortais()
        } catch {
          $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
        }
      })
    }

    onMounted(() => {
      fetchPortais()
    })

    return {
      rows, columns, loading, filter,
      dialog, saving, form, isEditing,
      openDialog, savePortal, deletePortal
    }
  }
}
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.3s;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>