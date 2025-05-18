<template>
  <div class="space-y-4">
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <ul class="divide-y divide-gray-200">
        <li v-for="employee in employees" :key="employee.id" class="px-4 py-4 flex items-center justify-between">
          <div>
            <h3 class="text-lg font-medium text-gray-900">{{ employee.name }}</h3>
            <div class="mt-1 text-sm text-gray-500">
              <p>Role: {{ employee.role }}</p>
              <p v-if="employee.role === 'senior' && employee.room_number">Room: {{ employee.room_number }}</p>
            </div>
          </div>
          <div class="flex space-x-3">
            <button
              @click="editEmployee(employee)"
              class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Edit
            </button>
            <button
              @click="deleteEmployee(employee)"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              Delete
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- Edit Modal -->
    <Modal :show="showEditModal" @close="closeEditModal">
      <template #title>Edit Employee</template>
      <EmployeeForm 
        :employee="originalEmployee" 
        @employee-added="handleEmployeeUpdated"
        @close="closeEditModal"
      />
    </Modal>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import Modal from './Modal.vue'
import EmployeeForm from './EmployeeForm.vue'

export default {
  name: 'EmployeeList',
  components: {
    Modal,
    EmployeeForm
  },
  props: {
    employees: {
      type: Array,
      required: true
    }
  },
  emits: ['employee-updated', 'employee-deleted'],
  setup(props, { emit }) {
    const showEditModal = ref(false)
    const originalEmployee = ref(null)

    const editEmployee = (employee) => {
      originalEmployee.value = employee
      showEditModal.value = true
    }

    const closeEditModal = () => {
      showEditModal.value = false
      originalEmployee.value = null
    }

    const handleEmployeeUpdated = async () => {
      emit('employee-updated')
      closeEditModal()
    }

    const deleteEmployee = async (employee) => {
      if (!confirm(`Are you sure you want to delete ${employee.name}?`)) return
      
      try {
        await axios.delete(`http://localhost:8000/api/employees/${employee.id}`)
        emit('employee-deleted')
      } catch (error) {
        console.error('Error deleting employee:', error)
        alert('Failed to delete employee')
      }
    }

    return {
      showEditModal,
      originalEmployee,
      editEmployee,
      closeEditModal,
      handleEmployeeUpdated,
      deleteEmployee
    }
  }
}
</script> 