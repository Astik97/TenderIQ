// ======================================
// Read JSON from compare.html
// ======================================

const chartData = JSON.parse(
    document.getElementById("chart-data").textContent
);

// ======================================
// Similarity Chart
// ======================================

new Chart(
    document.getElementById("similarityChart"),
    {
        type: "pie",
        data: {
            labels: chartData.similarity_chart.labels,
            datasets: [
                {
                    data: chartData.similarity_chart.values
                }
            ]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false
        }
    }
);

// ======================================
// Risk Chart
// ======================================

new Chart(
    document.getElementById("riskChart"),
    {
        type: "pie",
        data: {
            labels: chartData.risk_chart.labels,
            datasets: [
                {
                    data: chartData.risk_chart.values
                }
            ]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false
        }
    }
);

// ======================================
// Priority Chart
// ======================================

new Chart(
    document.getElementById("priorityChart"),
    {
        type: "bar",
        data: {
            labels: chartData.priority_chart.labels,
            datasets: [
                {
                    label: "Priority",
                    data: chartData.priority_chart.values
                }
            ]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false
        }
    }
);

// ======================================
// Dashboard Chart
// ======================================

new Chart(
    document.getElementById("dashboardChart"),
    {
        type: "bar",
        data: {
            labels:
            chartData.dashboard_chart.labels,
            datasets: [
                {
                    label: "Score",
                    data: chartData.dashboard_chart.values
                }
            ]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false
        }
    }
);