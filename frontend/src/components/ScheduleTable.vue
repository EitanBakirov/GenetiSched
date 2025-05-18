<template>
  <div class="space-y-4">
    <!-- Debug Info -->
    <div v-if="Object.keys(filteredRooms).length === 0" class="bg-yellow-50 p-4 rounded-md">
      <p class="text-yellow-700">Debug Info:</p>
      <pre class="text-xs mt-2">{{ JSON.stringify({
        showType,
        hasRooms: !!rooms,
        roomsLength: Object.keys(rooms || {}).length,
        hasSchedule: !!schedule,
        scheduleRooms: !!schedule?.rooms,
        monthDates: monthDates.value,
        currentWeek
      }, null, 2) }}</pre>
    </div>

    <!-- Week Navigation -->
    <div class="flex justify-between items-center px-4 bg-white rounded-lg shadow-sm p-4 mb-4">
      <div class="flex items-center">
        <div class="font-medium text-gray-900">Week {{ currentWeek }} of {{ totalWeeks }}</div>
        <div class="ml-3 px-3 py-1 bg-indigo-50 text-indigo-700 rounded-md font-medium">
          {{ getWeekRange(currentWeek) }}
        </div>
      </div>
      <div class="flex space-x-2">
        <button 
          @click="previousWeek"
          :disabled="currentWeek === 1"
          class="px-4 py-2 text-sm font-medium rounded-md border"
          :class="currentWeek === 1 ? 'bg-gray-50 text-gray-400 border-gray-200' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
        >
          Previous
        </button>
        <button 
          @click="nextWeek"
          :disabled="currentWeek === totalWeeks"
          class="px-4 py-2 text-sm font-medium rounded-md border"
          :class="currentWeek === totalWeeks ? 'bg-gray-50 text-gray-400 border-gray-200' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Schedule Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {{ showType === 'rooms' ? 'Room' : 'Senior Counselor' }}
            </th>
            <th
              v-for="(day, index) in weekDays"
              :key="day"
              scope="col"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
            >
              <div class="flex items-center space-x-2">
                <span>{{ day }}</span>
                <span v-if="monthDates.value && monthDates.value[currentWeek - 1]" class="text-xs font-normal text-gray-400">
                  ({{ monthDates.value[currentWeek - 1][index] }})
                </span>
              </div>
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-if="showType === 'rooms' && Object.keys(filteredRooms).length === 0" class="text-center">
            <td :colspan="weekDays.length + 1" class="px-6 py-4 text-sm text-gray-500">
              No rooms available. Add senior employees with assigned rooms.
            </td>
          </tr>
          <tr v-else-if="showType === 'assignments' && Object.keys(filteredSeniors).length === 0" class="text-center">
            <td :colspan="weekDays.length + 1" class="px-6 py-4 text-sm text-gray-500">
              No seniors available for assignments. Add senior employees who work with interns.
            </td>
          </tr>
          <template v-else>
            <template v-if="showType === 'rooms'">
              <tr v-for="(seniorName, roomKey) in filteredRooms" :key="`room-${roomKey}`">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  Room {{ roomKey }} ({{ seniorName }})
                </td>
                <td
                  v-for="day in weekDays"
                  :key="day"
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="getRoomCellClass(roomKey, day)"
                >
                  {{ getRoomStatus(roomKey, day) }}
                </td>
              </tr>
            </template>
            <template v-else>
              <tr v-for="(seniorName, roomKey) in filteredSeniors" :key="`senior-${roomKey}`">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ seniorName }} (Room {{ roomKey }})
                </td>
                <td
                  v-for="day in weekDays"
                  :key="day"
                  class="px-6 py-4 whitespace-nowrap text-sm"
                  :class="getAssignmentCellClass(roomKey, day)"
                >
                  {{ getAssignmentStatus(roomKey, day) }}
                </td>
              </tr>
            </template>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  schedule: {
    type: Object,
    required: true
  },
  rooms: {
    type: Object,
    required: true
  },
  employees: {
    type: Object,
    required: true
  },
  showType: {
    type: String,
    required: true
  }
})

const currentWeek = ref(1)
const totalWeeks = 4
const weekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
const monthDates = ref([])

const filteredRooms = computed(() => {
  console.log('ScheduleTable - Current props:', {
    schedule: props.schedule,
    rooms: props.rooms,
    employees: props.employees,
    showType: props.showType
  })
  
  if (!props.rooms || Object.keys(props.rooms).length === 0) {
    console.log('No rooms data')
    return {}
  }

  // Convert room data to include senior names
  const roomsWithNames = Object.entries(props.rooms).reduce((acc, [roomNumber, seniorId]) => {
    const senior = props.employees[seniorId]
    if (senior) {
      acc[roomNumber] = senior.name
    }
    return acc
  }, {})

  console.log('Filtered rooms result:', roomsWithNames)
  return roomsWithNames
})

const filteredSeniors = computed(() => {
  if (!props.rooms || !props.employees) return {}
  
  // Convert room data to include senior names
  return Object.entries(props.rooms).reduce((acc, [roomNumber, seniorId]) => {
    const senior = props.employees[seniorId]
    if (senior) {
      acc[roomNumber] = senior.name
    }
    return acc
  }, {})
})

const getRoomStatus = (roomKey, dayName) => {
  // First find the senior assigned to this room
  const seniorId = props.rooms[roomKey]
  if (!seniorId || !props.employees[seniorId]) {
    console.log('No senior found for room:', roomKey)
    return 'No Data'
  }

  // Get the senior's data
  const senior = props.employees[seniorId]
  console.log('Found senior for room:', roomKey, senior)
  
  // Get the date for this day in the current week
  const weekIndex = currentWeek.value - 1
  if (!monthDates.value || !monthDates.value[weekIndex]) {
    console.log('No dates found for week:', weekIndex)
    return 'No Data'
  }
  
  // Get the date string for this day
  const dayIndex = weekDays.indexOf(dayName)
  const dateStr = monthDates.value[weekIndex][dayIndex]
  if (!dateStr) {
    console.log('No date found for day:', dayName)
    return 'No Data'
  }

  // Convert DD/MM to YYYY-MM-DD format using 2025 as the year
  const [day, month] = dateStr.split('/')
  const formattedDate = `2025-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
  console.log('Checking availability for date:', formattedDate)

  // Check senior's availability for this date
  const isAvailable = senior.availability?.[formattedDate]
  console.log('Senior availability:', isAvailable)
  
  if (isAvailable === undefined) {
    return 'No Data'
  }

  // If senior is available (true), room is not available
  // If senior is not available (false), room is available
  return isAvailable ? 'Not Available' : 'Available'
}

const getAssignmentStatus = (roomKey, dayName) => {
  // First find the senior assigned to this room
  const seniorId = props.rooms[roomKey]
  if (!seniorId || !props.employees[seniorId]) {
    console.log('No senior found for room:', roomKey)
    return 'No Data'
  }

  // Get the senior's data
  const senior = props.employees[seniorId]
  console.log('Found senior for room:', roomKey, senior)
  
  // Get the date for this day in the current week
  const weekIndex = currentWeek.value - 1
  if (!monthDates.value || !monthDates.value[weekIndex]) {
    console.log('No dates found for week:', weekIndex)
    return 'No Data'
  }
  
  // Get the date string for this day
  const dayIndex = weekDays.indexOf(dayName)
  const dateStr = monthDates.value[weekIndex][dayIndex]
  if (!dateStr) {
    console.log('No date found for day:', dayName)
    return 'No Data'
  }

  // Convert DD/MM to YYYY-MM-DD format using 2025 as the year
  const [day, month] = dateStr.split('/')
  const formattedDate = `2025-${month.padStart(2, '0')}-${day.padStart(2, '0')}`
  console.log('Checking availability for date:', formattedDate)

  // First check if senior works with interns this week
  const weekNumber = getWeekNumber(dayIndex)
  const worksWithInterns = senior.works_with_interns_weekly?.[weekNumber]
  
  // If they don't work with interns this week, they're not available regardless of availability
  if (!worksWithInterns) {
    console.log('Senior does not work with interns this week:', weekNumber)
    return 'Not Available'
  }

  // If they do work with interns this week, check their availability for this day
  const isWorking = senior.availability?.[formattedDate]
  
  console.log('Senior status:', {
    isWorking,
    weekNumber,
    worksWithInterns,
    dayIndex,
    dayName
  })

  if (isWorking === undefined) {
    return 'No Data'
  }

  // They are only available if they both work with interns this week AND are working this day
  return isWorking ? 'Available' : 'Not Available'
}

const getRoomCellClass = (roomKey, dayName) => {
  const status = getRoomStatus(roomKey, dayName)
  if (status === 'Not Available') return 'bg-red-100 text-red-800'
  if (status === 'Available') return 'bg-green-100 text-green-800'
  return 'bg-gray-100 text-gray-800'
}

const getAssignmentCellClass = (roomKey, dayName) => {
  const status = getAssignmentStatus(roomKey, dayName)
  if (status === 'Available') return 'bg-green-100 text-green-800'
  if (status === 'Not Available') return 'bg-red-100 text-red-800'
  return 'bg-gray-100 text-gray-800'
}

const previousWeek = () => {
  if (currentWeek.value > 1) currentWeek.value--
}

const nextWeek = () => {
  if (currentWeek.value < totalWeeks) currentWeek.value++
}

const formatDate = (date) => {
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  return `${day}/${month}`
}

const initializeMonthDates = () => {
  // Use March 2025 as it matches the data in employees.json
  const year = 2025
  const month = 2  // 2 for March (0-based)
  const firstDay = new Date(year, month, 1)
  
  // Find the first Sunday of March 2025
  const startDate = new Date(firstDay)
  while (startDate.getDay() !== 0) {  // 0 is Sunday
    startDate.setDate(startDate.getDate() + 1)
  }
  
  const dates = []
  const currentDate = new Date(startDate)
  
  for (let week = 0; week < 4; week++) {
    const weekDates = []
    // Generate dates for the full week (0-6) but only store Sunday(0) to Thursday(4)
    for (let i = 0; i < 7; i++) {
      if (i <= 4) {  // Only store Sunday to Thursday
        weekDates.push(formatDate(currentDate))
      }
      currentDate.setDate(currentDate.getDate() + 1)  // Still increment for the full week
    }
    dates.push(weekDates)
  }
  
  monthDates.value = dates
}

const getWeekRange = (week) => {
  if (!monthDates.value || !monthDates.value[week - 1]) return ''
  
  // Get the first date (Sunday)
  const [startDay, startMonth] = monthDates.value[week - 1][0].split('/')
  
  // Calculate the end of week (Saturday) by adding 2 days to Thursday's date
  const thursdayDate = new Date(2025, parseInt(startMonth) - 1, parseInt(startDay) + 4)
  const saturdayDate = new Date(thursdayDate)
  saturdayDate.setDate(saturdayDate.getDate() + 2)
  
  // Format the range
  const endDay = saturdayDate.getDate().toString().padStart(2, '0')
  const endMonth = (saturdayDate.getMonth() + 1).toString().padStart(2, '0')
  
  return `${monthDates.value[week - 1][0]} - ${endDay}/${endMonth}`
}

// Helper function to get week number based on day index
const getWeekNumber = (dayIndex) => {
  const weekMap = {
    0: "1",  // Sunday
    1: "1",  // Monday
    2: "2",  // Tuesday
    3: "3",  // Wednesday
    4: "4",  // Thursday
  }
  return weekMap[dayIndex]
}

// Initialize dates when component is mounted
onMounted(() => {
  initializeMonthDates()
})
</script> 