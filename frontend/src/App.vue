<template>
  <!-- Main App Container -->
  <div class="relative">
    <!-- Main Content -->
    <div class="min-h-screen bg-gray-100">
      <nav class="bg-white shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between h-16">
            <div class="flex items-center">
              <h1 class="text-2xl font-bold text-gray-900">🧬 GenetiSched</h1>
            </div>
            <div class="flex items-center space-x-4">
              <button
                @click="showManageEmployees = true"
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
              >
                Manage Employees
              </button>
              <button
                @click="showAddEmployee = true"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Add Employee
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div class="px-4 py-6 sm:px-0">
          <!-- Schedule Type Selector -->
          <div class="mb-6 flex justify-between items-center">
            <div class="text-lg font-semibold text-gray-900">
              {{ getCurrentMonthName() }} {{ getCurrentYear() }}
            </div>
            <div class="flex space-x-4">
              <button
                v-for="type in scheduleTypes"
                :key="type.value"
                @click="currentScheduleType = type.value"
                class="px-4 py-2 rounded-md font-medium"
                :class="currentScheduleType === type.value ? 'bg-indigo-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50'"
              >
                {{ type.label }}
              </button>
            </div>
          </div>

          <!-- Schedule Display -->
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-medium text-gray-900">{{ getScheduleTitle }}</h3>
                <div class="flex space-x-2">
                  <button
                    v-if="['intern-senior', 'rooms'].includes(currentScheduleType)"
                    @click="resetCurrentSchedule"
                    class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    :disabled="isGenerating"
                  >
                    Reset Schedule
                  </button>
                  <button
                    @click="generateCurrentSchedule"
                    class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
                    :disabled="isGenerating"
                  >
                    <span v-if="isGenerating" class="mr-2">
                      Generating...
                    </span>
                    <span v-else>
                      Generate {{ getScheduleTitle }}
                    </span>
                  </button>
                </div>
              </div>

              <!-- Schedule Tables -->
              <ScheduleTable 
                :schedule="schedule"
                :rooms="rooms"
                :employees="employees"
                :showType="getShowType"
                @week-changed="handleWeekChange"
                v-if="['intern-senior', 'rooms'].includes(currentScheduleType)"
              />

              <!-- Office Duty Schedule -->
              <OfficeDutyTable
                v-else
                :schedule="officeDuty"
                :current-month="currentMonth"
                :current-year="currentYear"
              />
            </div>
          </div>
        </div>
      </main>
    </div>

    <!-- Modals -->
    <Teleport to="body">
      <!-- Add Employee Modal -->
      <Modal :show="showAddEmployee" @close="showAddEmployee = false">
        <template #title>Add New Employee</template>
        <EmployeeForm @employee-added="handleEmployeeAdded" @close="showAddEmployee = false" />
      </Modal>

      <!-- Manage Employees Modal -->
      <Modal :show="showManageEmployees" @close="showManageEmployees = false">
        <template #title>Manage Employees</template>
        <EmployeeList 
          :employees="employees" 
          @employee-updated="handleEmployeeUpdated"
          @employee-deleted="handleEmployeeDeleted"
        />
      </Modal>
    </Teleport>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import EmployeeForm from './components/EmployeeForm.vue'
import EmployeeList from './components/EmployeeList.vue'
import ScheduleTable from './components/ScheduleTable.vue'
import OfficeDutyTable from './components/OfficeDutyTable.vue'
import Modal from './components/Modal.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    EmployeeForm,
    EmployeeList,
    ScheduleTable,
    OfficeDutyTable,
    Modal
  },
  setup() {
    const showAddEmployee = ref(false)
    const showManageEmployees = ref(false)
    const employees = ref({})
    const schedule = ref({
      rooms: {},
      assignments: {},
      officeDuty: {}
    })
    const officeDuty = ref({})
    const rooms = ref({})
    const currentScheduleType = ref('rooms')
    const isGenerating = ref(false)
    const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    const currentMonth = new Date().getMonth()
    const currentYear = new Date().getFullYear()

    // Track last selected week for each view
    const lastSelectedWeek = ref({
      'intern-senior': 1,
      'rooms': 1,
      'office-duty': 1
    })

    const scheduleTypes = [
      { value: 'intern-senior', label: 'Intern-Senior Schedule' },
      { value: 'rooms', label: 'Room Schedule' },
      { value: 'office-duty', label: 'Office Duty Schedule' }
    ]

    const getCurrentMonthName = () => {
      return new Date(currentYear, currentMonth).toLocaleString('default', { month: 'long' })
    }

    const getCurrentYear = () => {
      return currentYear
    }

    const getScheduleTitle = computed(() => {
      const type = scheduleTypes.find(t => t.value === currentScheduleType.value)
      return type ? type.label : 'Schedule'
    })

    const getShowType = computed(() => {
      return currentScheduleType.value === 'rooms' ? 'rooms' : 'assignments'
    })

    // Handle week changes from schedule table
    const handleWeekChange = ({ type, week }) => {
      lastSelectedWeek.value[type] = week
    }

    const fetchEmployees = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/employees')
        employees.value = response.data
      } catch (error) {
        console.error('Error fetching employees:', error)
      }
    }

    // Generate schedule based on current type
    const generateCurrentSchedule = async () => {
      console.log('Generating schedule for type:', currentScheduleType.value)
      try {
        isGenerating.value = true
        
        if (currentScheduleType.value === 'intern-senior') {
          const response = await axios.post('http://localhost:8000/api/schedule/intern-senior')
          schedule.value = {
            ...schedule.value,
            assignments: response.data.schedule
          }
        } else if (currentScheduleType.value === 'rooms') {
          const response = await axios.post('http://localhost:8000/api/schedule/rooms')
          rooms.value = response.data.rooms
          schedule.value = {
            ...schedule.value,
            rooms: response.data.schedule
          }
        } else if (currentScheduleType.value === 'office-duty') {
          const response = await axios.post('http://localhost:8000/api/schedule/office-duty')
          officeDuty.value = response.data.office_duty
          schedule.value = {
            ...schedule.value,
            officeDuty: response.data.schedule
          }
        }
        console.log('Updated schedule:', schedule.value)
        console.log('Updated rooms:', rooms.value)
      } catch (error) {
        console.error('Error generating schedule:', error)
      } finally {
        isGenerating.value = false
      }
    }

    const handleEmployeeAdded = () => {
      showAddEmployee.value = false
      fetchEmployees()
      generateCurrentSchedule()
    }

    const handleEmployeeUpdated = () => {
      fetchEmployees()
      generateCurrentSchedule()
    }

    const handleEmployeeDeleted = () => {
      fetchEmployees()
      generateCurrentSchedule()
    }

    // Reset schedule based on current type
    const resetCurrentSchedule = async () => {
      console.log('Resetting schedule for type:', currentScheduleType.value)
      try {
        if (currentScheduleType.value === 'intern-senior') {
          const response = await fetch('/api/schedule/intern-senior/reset', {
            method: 'POST'
          })
          const data = await response.json()
          console.log('Intern-senior reset response:', data)
          if (data.success) {
            schedule.value = {
              ...schedule.value,
              assignments: data.schedule
            }
          }
        } else if (currentScheduleType.value === 'rooms') {
          const response = await fetch('/api/schedule/rooms/reset', {
            method: 'POST'
          })
          const data = await response.json()
          console.log('Room reset response:', data)
          if (data.success) {
            rooms.value = data.rooms || {}
            schedule.value = {
              ...schedule.value,
              rooms: data.schedule || {}
            }
          }
          console.log('Updated rooms:', rooms.value)
          console.log('Updated schedule:', schedule.value)
        }
      } catch (error) {
        console.error('Error resetting schedule:', error)
      }
    }

    // Fetch initial data
    const fetchInitialData = async () => {
      try {
        console.log('Fetching initial data...')
        const response = await fetch('http://localhost:8000/api/employees')
        const data = await response.json()
        console.log('Employees data:', data)
        
        // Convert employees array to object with ID as key
        employees.value = data.reduce((acc, emp) => {
          acc[emp.id] = emp
          return acc
        }, {})
        console.log('Processed employees:', employees.value)

        // Reset schedule after fetching employees
        const scheduleResponse = await fetch('http://localhost:8000/api/reset_room_schedule', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        const scheduleData = await scheduleResponse.json()
        console.log('Schedule reset response:', scheduleData)
        
        if (scheduleData.success) {
          schedule.value = {
            rooms: scheduleData.schedule || {},
            assignments: scheduleData.assignments || {}
          }
          rooms.value = scheduleData.rooms || {}
          console.log('Updated state:', {
            schedule: schedule.value,
            rooms: rooms.value,
            employees: employees.value
          })
        }
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    }

    // Call fetchInitialData when component is mounted
    onMounted(() => {
      fetchInitialData()
    })

    return {
      showAddEmployee,
      showManageEmployees,
      employees,
      schedule,
      officeDuty,
      rooms,
      currentScheduleType,
      isGenerating,
      scheduleTypes,
      weekdays,
      getScheduleTitle,
      getShowType,
      generateCurrentSchedule,
      handleEmployeeAdded,
      handleEmployeeUpdated,
      handleEmployeeDeleted,
      handleWeekChange,
      lastSelectedWeek,
      getCurrentMonthName,
      getCurrentYear,
      currentMonth,
      currentYear,
      resetCurrentSchedule
    }
  }
}
</script> 