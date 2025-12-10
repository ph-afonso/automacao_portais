<template>
  <q-page class="q-pa-md">
    
    <q-table
      title="Gerenciar Usuários"
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
          icon="person_add" 
          label="Novo Usuário" 
          class="q-ml-md" 
          @click="openDialog()"
        />
      </template>

      <template v-slot:body-cell-is_active="props">
        <q-td :props="props">
          <q-badge :color="props.value ? 'positive' : 'grey'">
            {{ props.value ? 'Ativo' : 'Inativo' }}
          </q-badge>
        </q-td>
      </template>

      <template v-slot:body-cell-is_staff="props">
        <q-td :props="props">
          <q-icon 
            :name="props.value ? 'verified' : 'person'" 
            :color="props.value ? 'positive' : 'grey'"
            size="sm"
          />
        </q-td>
      </template>

      <template v-slot:body-cell-actions="props">
        <q-td :props="props" align="right">
          <q-btn flat round color="blue" icon="edit" size="sm" @click="openDialog(props.row)">
            <q-tooltip>Editar</q-tooltip>
          </q-btn>
          <q-btn flat round color="red" icon="delete" size="sm" @click="deleteUser(props.row)">
            <q-tooltip>Excluir</q-tooltip>
          </q-btn>
        </q-td>
      </template>
    </q-table>

    <q-dialog v-model="dialog" persistent>
      <q-card style="width: 600px; max-width: 80vw;">
        <q-card-section>
          <div class="text-h6">{{ isEditing ? 'Editar Usuário' : 'Novo Usuário' }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="saveUser" class="q-gutter-md">
            
            <div class="row q-col-gutter-xs q-pt-xs">
              <div class="col-12 col-md-6">
                <q-input 
                  filled v-model="form.first_name" label="Nome" 
                  :rules="[val => !!val || 'Obrigatório']"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input 
                  filled v-model="form.last_name" label="Sobrenome" 
                  :rules="[val => !!val || 'Obrigatório']"
                />
              </div>
            </div>

            <div class="row q-col-gutter-xs q-pt-xs">
              <div class="col-12 col-md-6">
                <q-input 
                  filled v-model="form.username" label="Usuário (Login) *" 
                  :rules="[val => !!val || 'Obrigatório']"
                  :disable="isEditing" 
                  hint="O login não pode ser alterado"
                />
              </div>
              <div class="col-12 col-md-6">
                <q-input 
                  filled v-model="form.email" label="E-mail *" 
                  type="email"
                  :rules="[val => !!val || 'Obrigatório']"
                />
              </div>
            </div>

            <q-input 
              filled 
              v-model="form.password" 
              type="password" 
              label="Senha" 
              :rules="isEditing ? [] : [val => !!val || 'Obrigatório na criação']"
              :hint="isEditing ? 'Deixe em branco para não alterar a senha' : ''"
            />

            <q-separator />

            <div class="q-pa-sm bg-grey-1 rounded-borders row justify-between">
              <q-toggle v-model="form.is_active" label="Ativo?" color="green" />
              <q-toggle v-model="form.is_staff" label="Administrador?" color="blue" />
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
    
    const dialog = ref(false)
    const saving = ref(false)
    const isEditing = ref(false)
    const editingId = ref(null)

    const form = reactive({
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      is_active: true,
      is_staff: false
    })

    const columns = [
      { name: 'username', label: 'Login', field: 'username', align: 'left', sortable: true },
      { name: 'first_name', label: 'Nome', field: 'first_name', align: 'left' },
      { name: 'email', label: 'E-mail', field: 'email', align: 'left' },
      { name: 'is_staff', label: 'Tipo', field: 'is_staff', align: 'center' },
      { name: 'is_active', label: 'Status', field: 'is_active', align: 'center' },
      { name: 'actions', label: 'Ações', field: 'actions', align: 'right' }
    ]

    const fetchUsers = async () => {
      loading.value = true
      try {
        const response = await api.get('/api/usuarios/')
        rows.value = response.data
      } catch {
        $q.notify({ type: 'negative', message: 'Erro ao carregar usuários' })
      } finally {
        loading.value = false
      }
    }

    const openDialog = (row = null) => {
      if (row) {
        isEditing.value = true
        editingId.value = row.id
        form.username = row.username
        form.first_name = row.first_name
        form.last_name = row.last_name
        form.email = row.email
        form.is_active = row.is_active
        form.is_staff = row.is_staff
        form.password = '' // Senha sempre vazia na edição
      } else {
        isEditing.value = false
        editingId.value = null
        form.username = ''
        form.first_name = ''
        form.last_name = ''
        form.email = ''
        form.password = ''
        form.is_active = true
        form.is_staff = false
      }
      dialog.value = true
    }

    const saveUser = async () => {
      saving.value = true
      try {
        // Prepara os dados. Remove senha se estiver vazia na edição
        const data = { ...form }
        if (isEditing.value && !data.password) {
          delete data.password
        }

        if (isEditing.value) {
          await api.patch(`/api/usuarios/${editingId.value}/`, data)
          $q.notify({ type: 'positive', message: 'Usuário atualizado!' })
        } else {
          await api.post('/api/usuarios/', data)
          $q.notify({ type: 'positive', message: 'Usuário criado!' })
        }

        dialog.value = false
        fetchUsers()

      } catch (error) {
        // Se o erro for de validação (ex: username já existe)
        const msg = error.response?.data?.username ? 'Este usuário já existe.' : 'Erro ao salvar.'
        $q.notify({ type: 'negative', message: msg })
      } finally {
        saving.value = false
      }
    }

    const deleteUser = (row) => {
      $q.dialog({
        title: 'Confirmar',
        message: `Excluir o usuário ${row.username}?`,
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await api.delete(`/api/usuarios/${row.id}/`)
          $q.notify({ type: 'positive', message: 'Usuário excluído.' })
          fetchUsers()
        } catch {
          $q.notify({ type: 'negative', message: 'Erro ao excluir.' })
        }
      })
    }

    onMounted(() => {
      fetchUsers()
    })

    return {
      rows, columns, loading, filter,
      dialog, saving, form, isEditing,
      openDialog, saveUser, deleteUser
    }
  }
}
</script>