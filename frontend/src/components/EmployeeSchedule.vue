<template>
  <div class="space-y-4">
    <div>
      <label for="employee-select" class="block text-sm font-medium text-gray-700">Select Employee</label>
      <div class="mt-1 flex items-center space-x-2">
        <select
          id="employee-select"
          v-model="selectedEmployee"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        >
          <option value="">Select an employee</option>
          <option v-for="emp in employees" :key="emp.name" :value="emp">
            {{ emp.name }} ({{ emp.role }})
          </option>
        </select>
        <button
          v-if="selectedEmployee"
          @click="deleteEmployee"
          class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
        >
          Delete
        </button>
      </div>
    </div>

    <div v-if="selectedEmployee" class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Day
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Room
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Role
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="day in weekdays" :key="day">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {{ day }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ getRoomForEmployee(day) || '-' }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {{ getRoleForEmployee(day) || '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import axios from 'axios'

export default {
  name: 'EmployeeSchedule',
  props: {
    employees: {
      type: Array,
      required: true
    },
    schedule: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['employee-deleted'],
  setup(props, { emit }) {
    const selectedEmployee = ref(null)
    const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

    const getRoomForEmployee = (day) => {
      if (!selectedEmployee.value || !props.schedule[day]) return null
      
      for (const [room, employees] of Object.entries(props.schedule[day])) {
        if (employees.includes(selectedEmployee.value.name)) {
          return room
        }
      }
      return null
    }

    const getRoleForEmployee = (day) => {
      if (!selectedEmployee.value) return null
      
      const room = getRoomForEmployee(day)
      if (!room) return null

      if (room === 'Office Duty' && props.officeDuty?.[day] === selectedEmployee.value.name) {
        return 'Office Duty'
      }

      return selectedEmployee.value.role
    }

    const deleteEmployee = async () => {
      if (!selectedEmployee.value) return
      
      try {
        await axios.delete(`http://localhost:8000/api/employees/${selectedEmployee.value.name}`)
        emit('employee-deleted')
        selectedEmployee.value = null
      } catch (error) {
        console.error('Error deleting employee:', error)
        alert('Failed to delete employee')
      }
    }

    return {
      selectedEmployee,
      weekdays,
      getRoomForEmployee,
      getRoleForEmployee,
      deleteEmployee
    }
  }
}
</script> 