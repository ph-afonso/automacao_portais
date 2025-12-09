import { boot } from 'quasar/wrappers'
import axios from 'axios'

// Crie uma instância do axios com a URL do seu Backend Django
const api = axios.create({ baseURL: 'http://127.0.0.1:8000' })

export default boot(({ app }) => {
  // Isso permite usar this.$axios e this.$api dentro dos arquivos .vue (Options API)
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }