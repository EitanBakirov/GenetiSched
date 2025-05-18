# GenetiSched Project Brief

## Project Overview
GenetiSched is a web-based scheduling platform designed for genetic counseling departments. It enables managers to efficiently manage room assignments, intern-senior counselor pairings, and office duty rotations based on availability and internal rules.

## Core Requirements

### 1. Employee Management
- Support for two employee types:
  - Senior Counselors
  - Interns
- Employee attributes:
  - Employment percentage
  - Daily availability
  - Weekly intern availability (for seniors)
  - Room assignments (for seniors)

### 2. Scheduling Features
- Room scheduling (Sunday-Thursday)
- Intern-Senior counselor assignments
- Office duty rotations
- Automatic schedule generation based on rules
- Week-based availability tracking
- Cross-month week handling

### 3. Technical Requirements
- FastAPI backend (Python)
- Vue.js frontend with TailwindCSS
- JSON-based data storage (upgradable to SQLite/PostgreSQL)
- REST API communication using Axios

## Project Goals
1. Streamline scheduling process for genetic counseling departments
2. Ensure fair distribution of intern assignments
3. Optimize room utilization
4. Maintain clear visibility of schedules
5. Support flexible availability management

## Success Criteria
1. Successful room assignment and management
2. Proper intern-senior counselor pairing
3. Accurate schedule generation based on rules
4. Intuitive user interface
5. Reliable data persistence 