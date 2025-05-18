<template>
  <form @submit.prevent="submitForm" class="space-y-4">
    <div class="space-y-2">
      <label class="block text-sm font-medium text-gray-700">Name</label>
      <input v-model="formData.name" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
    </div>

    <div class="space-y-2">
      <label class="block text-sm font-medium text-gray-700">Role</label>
      <select v-model="formData.role" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
        <option value="intern">Intern</option>
        <option value="senior">Senior</option>
      </select>
    </div>

    <div class="space-y-2">
      <label class="block text-sm font-medium text-gray-700">Employment Percentage</label>
      <select v-model="formData.employment" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
        <option :value="100">100%</option>
        <option :value="80">80%</option>
      </select>
    </div>

    <div v-if="formData.role === 'senior'" class="space-y-2">
      <label class="block text-sm font-medium text-gray-700">Room Number (Optional)</label>
      <input 
        v-model="formData.room_number" 
        type="text" 
        @blur="validateRoom"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
        :class="{ 'border-red-500': roomError }">
      <p v-if="roomError" class="text-red-500 text-sm">{{ roomError }}</p>
    </div>

    <!-- Monthly Calendar -->
    <div class="space-y-4">
      <h3 class="text-lg font-medium text-gray-900">Monthly Availability</h3>
      <p class="text-sm text-gray-500">Uncheck the days you are NOT available to work</p>
      <div class="border rounded-lg p-4">
        <!-- Month and Year -->
        <div class="text-center mb-4">
          <h4 class="text-lg font-semibold">{{ currentMonthYear }}</h4>
        </div>
        <!-- Calendar Grid -->
        <div class="grid grid-cols-7 gap-2">
          <div v-for="day in weekdays" :key="day" class="text-center font-medium text-gray-500">
            {{ day }}
          </div>
          <template v-for="(week, weekIndex) in calendarWeeks" :key="'week-' + weekIndex">
            <div v-for="day in week" :key="day.date" class="relative">
              <div 
                class="aspect-square flex flex-col items-center justify-between border rounded-lg p-2"
                :class="{
                  'bg-gray-100 cursor-not-allowed': !isWorkday(day.date),
                  'cursor-pointer hover:bg-gray-50': isWorkday(day.date)
                }"
                @click="isWorkday(day.date) && toggleDate(day.date)"
              >
                <span 
                  :class="{
                    'text-gray-400': !isWorkday(day.date),
                    'text-gray-900': isWorkday(day.date)
                  }"
                >
                  {{ day.dayOfMonth }}
                </span>
                <div v-if="isWorkday(day.date)">
                  <input
                    type="checkbox"
                    :checked="isDateSelected(day.date)"
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                    @click.stop="toggleDate(day.date)"
                  />
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- Weekly Intern Supervision Settings (for seniors) -->
    <div v-if="formData.role === 'senior'" class="space-y-4">
      <h3 class="text-lg font-medium text-gray-900">Weekly Intern Supervision</h3>
      <div class="grid grid-cols-2 gap-4">
        <div v-for="week in 4" :key="week" class="flex items-center space-x-2">
          <input 
            type="checkbox" 
            :id="'week-' + week"
            v-model="formData.works_with_interns_weekly[week]"
            class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
          <label :for="'week-' + week" class="text-sm text-gray-700">Week {{ week }}</label>
        </div>
      </div>
    </div>

    <div class="flex justify-end space-x-3">
      <button type="button" @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50">
        Cancel
      </button>
      <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700">
        Save
      </button>
    </div>
  </form>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

export default {
  name: 'EmployeeForm',
  props: {
    employee: {
      type: Object,
      default: null
    }
  },
  emits: ['employee-added', 'close'],
  setup(props, { emit }) {
    const formData = ref({
      name: '',
      role: 'intern',
      employment: 100,
      room_number: '',
      availability: {},
      works_with_interns_weekly: {}
    })

    const monthDates = ref([])
    const roomError = ref('')

    const currentMonthYear = computed(() => {
      const date = new Date()
      return new Intl.DateTimeFormat('en-US', { 
        month: 'long', 
        year: 'numeric' 
      }).format(date)
    })

    const weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    const isWorkday = (date) => {
      if (!date) return false
      const dateObj = new Date(date)
      // Force UTC to avoid timezone issues
      const utcDay = dateObj.getUTCDay()
      console.log('Date:', date, 'UTC Day:', utcDay, 'Local Day:', dateObj.getDay())
      return utcDay <= 4  // Sunday (0) through Thursday (4)
    }

    const toggleDate = (date) => {
      if (!isWorkday(date)) return
      formData.value.availability[date] = !formData.value.availability[date]
    }

    const isDateSelected = (date) => {
      if (!isWorkday(date)) return false
      return formData.value.availability[date] || false
    }

    const calendarWeeks = computed(() => {
      const year = new Date().getFullYear()
      const month = new Date().getMonth()
      const firstDay = new Date(Date.UTC(year, month, 1))
      const lastDay = new Date(Date.UTC(year, month + 1, 0))
      const startingDay = firstDay.getUTCDay() // Force Sunday as first day (0)

      const days = []
      // Add empty cells for days before the first day of the month
      for (let i = 0; i < startingDay; i++) {
        days.push({ date: null, dayOfMonth: '' })
      }
      // Add all days of the month
      for (let i = 1; i <= lastDay.getUTCDate(); i++) {
        const currentDate = new Date(Date.UTC(year, month, i))
        const formattedDate = currentDate.toISOString().split('T')[0]
        days.push({
          date: formattedDate,
          dayOfMonth: i
        })
      }

      // Group days into weeks
      const weeks = []
      for (let i = 0; i < days.length; i += 7) {
        weeks.push(days.slice(i, i + 7))
      }

      return weeks
    })

    onMounted(async () => {
      console.log('Component mounted')
      try {
        const response = await fetch('http://localhost:8000/api/current-month-dates')
        if (!response.ok) {
          throw new Error('Failed to fetch dates')
        }
        const dates = await response.json()
        console.log('Received dates:', dates)
        monthDates.value = dates
        
        // Initialize form data
        const baseFormData = {
          name: '',
          role: 'intern',
          employment: 100,
          room_number: '',
          availability: {},
          works_with_interns_weekly: {}
        }

        // Initialize all workdays as available (checked)
        const year = new Date().getFullYear()
        const month = new Date().getMonth()
        
        // Get all days in the current month
        const lastDay = new Date(year, month + 1, 0).getDate()
        for (let i = 1; i <= lastDay; i++) {
          const currentDate = new Date(Date.UTC(year, month, i))
          const formattedDate = currentDate.toISOString().split('T')[0]
          if (isWorkday(formattedDate)) {
            baseFormData.availability[formattedDate] = true
          }
        }

        // Initialize weekly intern supervision settings
        for (let week = 1; week <= 4; week++) {
          baseFormData.works_with_interns_weekly[week] = true
        }

        // If editing existing employee, merge their data with the base form data
        if (props.employee) {
          formData.value = {
            ...baseFormData,
            ...props.employee,
            // Merge availability to keep the calendar structure
            availability: {
              ...baseFormData.availability,
              ...props.employee.availability
            },
            works_with_interns_weekly: {
              ...baseFormData.works_with_interns_weekly,
              ...props.employee.works_with_interns_weekly
            }
          }
        } else {
          formData.value = baseFormData
        }

      } catch (error) {
        console.error('Error fetching month dates:', error)
      }
    })

    const validateRoom = async () => {
      roomError.value = ''
      if (!formData.value.room_number) return true

      // Skip validation if editing and room number hasn't changed
      if (props.employee && props.employee.room_number === formData.value.room_number) {
        return true
      }

      try {
        const response = await fetch(`http://localhost:8000/api/validate-room/${formData.value.room_number}`)
        const data = await response.json()
        
        if (!response.ok) {
          roomError.value = data.detail
          return false
        }
        
        return true
      } catch (error) {
        console.error('Room validation error:', error)
        return true // Allow submission if validation fails for technical reasons
      }
    }

    const submitForm = async () => {
      try {
        if (formData.value.role === 'senior' && formData.value.room_number) {
          const isValid = await validateRoom()
          if (!isValid) return
        }

        // Convert week numbers to strings in works_with_interns_weekly
        const works_with_interns_weekly = {}
        if (formData.value.role === 'senior') {
          Object.entries(formData.value.works_with_interns_weekly).forEach(([week, value]) => {
            works_with_interns_weekly[week.toString()] = value
          })
        }

        const employeeData = {
          name: formData.value.name,
          role: formData.value.role,
          employment: Number(formData.value.employment),
          room_number: formData.value.room_number || null,
          availability: formData.value.availability,
          works_with_interns_weekly: works_with_interns_weekly
        }

        console.log('Sending employee data:', employeeData)
        let response;
        
        if (props.employee) {
          // Update existing employee
          response = await axios.put(`http://localhost:8000/api/employees/${props.employee.id}`, employeeData)
        } else {
          // Create new employee
          response = await axios.post('http://localhost:8000/api/employees', employeeData)
        }
        
        console.log('Response:', response.data)
        emit('employee-added', response.data)
      } catch (error) {
        console.error('Error saving employee:', error.response?.data || error)
        alert(error.response?.data?.detail || 'Failed to save employee. Please try again.')
      }
    }

    return {
      formData,
      weekdays,
      monthDates,
      calendarWeeks,
      currentMonthYear,
      roomError,
      isWorkday,
      toggleDate,
      isDateSelected,
      validateRoom,
      submitForm
    }
  }
}
</script>

<style scoped>
.calendar-day {
  aspect-ratio: 1;
}
</style> 