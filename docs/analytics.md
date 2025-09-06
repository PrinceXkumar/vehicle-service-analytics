# Analytics & Reporting System

## Overview
The Vehicle Service Analytics system provides comprehensive data visualization and reporting capabilities for different user roles. This makes the project CV-worthy by demonstrating Data Analysis + Visualization skills.

## Features

### 1. Manager Analytics Dashboard
**URL:** `/analytics/manager/`

**Features:**
- **Key Metrics Cards:** Total services, completed, pending, this month's services
- **Monthly Services Chart:** Bar chart showing services per month over the last 12 months
- **Status Distribution:** Pie chart showing pending vs completed vs in-progress services
- **Service Types Chart:** Doughnut chart showing distribution of service types
- **Top Performers Table:** Shows busiest mechanics with job counts
- **Most Popular Service Types:** Cards showing top 3 service types
- **Export Functionality:** Download reports as CSV or Excel

**Charts Used:**
- Bar Chart (Chart.js) for monthly trends
- Pie Chart for status distribution
- Doughnut Chart for service types
- Progress bars for mechanic performance

### 2. Customer Analytics Dashboard
**URL:** `/analytics/customer/`

**Features:**
- **Personal Metrics:** Total services, completed, pending, this year's services
- **Service History Chart:** Line chart showing personal service history by year
- **Service Status Overview:** Visual breakdown of personal service statuses
- **Quick Actions:** Links to book new services and view dashboard

**Charts Used:**
- Line Chart (Chart.js) for service history trends

### 3. Mechanic Analytics Dashboard
**URL:** `/analytics/mechanic/`

**Features:**
- **Performance Metrics:** Total assigned, completed, pending, this month's completed
- **Job Status Distribution:** Doughnut chart showing personal job statuses
- **Completion Rate:** Progress bar showing completion percentage
- **Performance Insights:** Alerts showing monthly performance and overall stats
- **Quick Actions:** Links to manage jobs and view dashboard

**Charts Used:**
- Doughnut Chart for job status distribution
- Progress bars for completion rates

### 4. Exportable Reports
**URL:** `/analytics/export/`

**Features:**
- **CSV Export:** Download service data as CSV file
- **Excel Export:** Download service data as Excel file (requires openpyxl)
- **Filtering:** Export by status (all, pending, completed, in_progress)

**Parameters:**
- `format`: csv or excel
- `status`: all, pending, completed, in_progress

## Technical Implementation

### Analytics Engine (`services/analytics.py`)
- **ServiceAnalytics Class:** Core analytics functions
  - `get_monthly_service_counts()`: Monthly service trends
  - `get_service_status_distribution()`: Status breakdown
  - `get_service_type_distribution()`: Service type breakdown
  - `get_mechanic_performance()`: Mechanic performance metrics
  - `get_customer_service_history()`: Personal service history
  - `get_manager_insights()`: Comprehensive manager dashboard data
  - `get_mechanic_insights()`: Personal mechanic performance
  - `get_customer_insights()`: Personal customer analytics

- **ReportGenerator Class:** Export functionality
  - `generate_csv_report()`: CSV export
  - `generate_excel_report()`: Excel export with fallback to CSV

### Views (`services/views.py`)
- **analytics_dashboard():** Manager analytics view
- **customer_analytics():** Customer analytics view
- **mechanic_analytics():** Mechanic analytics view
- **analytics_data_api():** AJAX API for dynamic data
- **export_report():** Report export functionality
- **analytics_redirect():** Role-based analytics routing

### Templates
- **manager_analytics.html:** Manager dashboard with multiple charts
- **customer_analytics.html:** Customer personal analytics
- **mechanic_analytics.html:** Mechanic performance analytics

### Chart.js Integration
- **CDN Integration:** Charts loaded from CDN
- **Interactive Charts:** Bar, pie, doughnut, and line charts
- **Responsive Design:** Charts adapt to container size
- **Color Schemes:** Professional color palettes for different data types

## Data Flow

1. **User Access:** User clicks Analytics link in navigation
2. **Role Routing:** `analytics_redirect()` routes to appropriate dashboard
3. **Data Aggregation:** Analytics functions query database and aggregate data
4. **Template Rendering:** Data passed to templates with JSON for charts
5. **Chart Rendering:** Chart.js renders interactive visualizations
6. **Export Options:** Users can export data in various formats

## Sample Data
A management command `populate_sample_data` creates realistic test data:
- Sample users (manager, customers, mechanics)
- Sample vehicles for customers
- Sample services with realistic dates and statuses
- Random assignments and distributions

## Usage Examples

### Manager Alice
1. Logs in as manager
2. Clicks "Analytics Dashboard"
3. Sees pie chart: 70% Completed, 30% Pending
4. Sees bar chart: Jan (20 services), Feb (35), Mar (42)...
5. Clicks "Export Excel" to download report

### Customer John
1. Logs in as customer
2. Clicks "My Analytics"
3. Sees personal history: "You booked 5 services this year (3 completed, 2 pending)"
4. Views line chart of services per year

### Mechanic Bob
1. Logs in as mechanic
2. Clicks "My Performance"
3. Sees "You completed 12 jobs this month"
4. Views completion rate and job distribution

## CV-Worthy Features

This analytics system demonstrates:
- **Data Analysis:** Complex aggregations and insights
- **Data Visualization:** Interactive charts and graphs
- **Role-Based Access:** Different views for different user types
- **Export Functionality:** CSV/Excel report generation
- **Real-time Data:** Dynamic charts with live data
- **Professional UI:** Clean, modern dashboard design
- **Full-Stack Skills:** Backend analytics + frontend visualization

## Future Enhancements
- PDF report generation
- Email report scheduling
- Advanced filtering options
- Real-time notifications
- Performance benchmarking
- Cost analysis and revenue tracking
