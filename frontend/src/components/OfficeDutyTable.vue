<template>
  <div class="space-y-4">
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th
              v-for="day in weekdays"
              :key="day"
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              {{ day }}
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(weekDates, weekIndex) in monthDates" :key="'week-'+weekIndex">
            <td
              v-for="(dateStr, dayIndex) in weekDates"
              :key="dateStr"
              class="px-2 pt-1 pb-0.5 whitespace-nowrap border h-[60px] align-top"
              :class="getCellClass(dateStr)"
            >
              <div class="flex flex-col space-y-1">
                <span 
                  class="text-sm leading-none"
                  :class="isCurrentMonth(dateStr) ? 'text-gray-900' : 'text-gray-400'"
                >
                  {{ formatDate(dateStr) }}
                </span>
                <span 
                  v-if="getAssignedEmployee(dateStr) && isCurrentMonth(dateStr)" 
                  class="text-green-600 font-medium leading-tight"
                >
                  {{ getAssignedEmployee(dateStr) }}
                </span>
                <span 
                  v-else-if="isCurrentMonth(dateStr)" 
                  class="text-gray-500 leading-tight"
                >
                  No one available
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, watchEffect } from 'vue'

export default {
  name: 'OfficeDutyTable',
  props: {
    schedule: {
      type: Object,
      required: true
    },
    currentMonth: {
      type: Number,
      required: true
    },
    currentYear: {
      type: Number,
      required: true
    }
  },
  setup(props) {
    const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

    // Get the current month's dates including padding days
    const getCurrentMonthDates = () => {
      const firstDay = new Date(props.currentYear, props.currentMonth, 1)
      const lastDay = new Date(props.currentYear, props.currentMonth + 1, 0)
      
      // Find the first Sunday
      let startDate = new Date(firstDay)
      while (startDate.getDay() !== 0) {
        startDate.setDate(startDate.getDate() - 1)
      }

      // Generate all dates including padding
      const dates = []
      let currentDate = new Date(startDate)
      
      // Continue until we've covered all weeks that include current month dates
      while (currentDate <= lastDay || currentDate.getDay() !== 0) {
        const weekDates = []
        // Only add Sunday through Thursday
        for (let i = 0; i < 5; i++) {
          weekDates.push(formatDateForAvailability(new Date(currentDate)))
          currentDate.setDate(currentDate.getDate() + 1)
        }
        // Skip Friday and Saturday
        currentDate.setDate(currentDate.getDate() + 2)
        dates.push(weekDates)
      }
      
      return dates
    }

    const formatDateForAvailability = (date) => {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      const [year, month, day] = dateStr.split('-')
      return day // Just show the day number
    }

    const isCurrentMonth = (dateStr) => {
      if (!dateStr) return false
      const [year, month] = dateStr.split('-')
      return parseInt(month) === props.currentMonth + 1 && parseInt(year) === props.currentYear
    }

    const monthDates = ref(getCurrentMonthDates())

    // Update monthDates when month or year changes
    watchEffect(() => {
      monthDates.value = getCurrentMonthDates()
    })

    const getAssignedEmployee = (dateStr) => {
      // Find which employee is assigned to this date
      for (const [employee, dates] of Object.entries(props.schedule)) {
        if (dates.includes(dateStr)) {
          return employee
        }
      }
      return null
    }

    const getCellClass = (dateStr) => {
      const isAssigned = getAssignedEmployee(dateStr)
      const isThisMonth = isCurrentMonth(dateStr)
      
      return {
        'bg-green-50': isAssigned && isThisMonth,
        'bg-gray-50': !isThisMonth,
        'bg-white': isThisMonth && !isAssigned
      }
    }

    return {
      weekdays,
      monthDates,
      formatDate,
      getAssignedEmployee,
      getCellClass,
      isCurrentMonth
    }
  }
}
</script>

<style scoped>
td.h-[60px] {
  height: 60px;
}
</style> 