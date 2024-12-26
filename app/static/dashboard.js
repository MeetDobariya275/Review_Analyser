// Data passed from Flask
const sentimentDataFromBackend = JSON.parse(document.getElementById('sentimentData').textContent);
const recentReviewsFromBackend = JSON.parse(document.getElementById('recentReviews').textContent);

// Prepare data for Chart.js
const sentimentData = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [{
        label: 'Sentiment Analysis',
        data: [
            sentimentDataFromBackend.positive,
            sentimentDataFromBackend.neutral,
            sentimentDataFromBackend.negative
        ],
        backgroundColor: ['#4CAF50', '#FFC107', '#F44336'],
    }]
};

// Configure and render the sentiment chart
const ctx = document.getElementById('sentimentChart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: sentimentData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
        }
    }
});

// Display recent reviews
const reviewList = document.getElementById('reviewList');
recentReviewsFromBackend.forEach(review => {
    const listItem = document.createElement('li');
    listItem.textContent = `${review[0]} (${review[2]}): ${review[1]}`;
    reviewList.appendChild(listItem);
});
