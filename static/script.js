let genderChart;

function initChart() {
  const ctx = document.getElementById('genderChart').getContext('2d');
  genderChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Erkek', 'Kadın'],
      datasets: [{
        data: [0, 0],
        backgroundColor: ['#2196F3', '#E91E63'],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' }
      }
    }
  });
}

async function fetchUsers() {
  try {
    const res = await fetch('/users');
    if (!res.ok) throw new Error(res.status);
    const users = await res.json();
    document.getElementById('userCount').textContent = users.length;

    const list = document.getElementById('userList');
    list.innerHTML = '';
    users.forEach(u => {
      const li = document.createElement('li');
      li.textContent = u.fullname;
      list.appendChild(li);
    });
    // Otomatik aşağı kaydır
    const container = document.querySelector('.list-container');
    container.scrollTop = container.scrollHeight;
  } catch (err) {
    console.error('fetchUsers hata:', err);
  }
}

async function fetchLastUser() {
  try {
    const res = await fetch('/last_user');
    if (res.status === 204) return;
    const u = await res.json();
    document.getElementById('lastName').textContent    = u.fullname;
    document.getElementById('lastEmail').textContent   = u.email;
    document.getElementById('lastGender').textContent  = u.gender;
    document.getElementById('lastCountry').textContent = u.country;
    document.getElementById('lastAge').textContent     = u.age;
  } catch (err) {
    console.error('fetchLastUser hata:', err);
  }
}

async function fetchStats() {
  try {
    const res = await fetch('/stats');
    if (!res.ok) throw new Error(res.status);
    const { male, female } = await res.json();
    // Chart güncelle
    genderChart.data.datasets[0].data = [male, female];
    genderChart.update();
  } catch (err) {
    console.error('fetchStats hata:', err);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initChart();
  // İlk yükleme
  fetchUsers();
  fetchLastUser();
  fetchStats();
  // 3 saniyede bir periyodik yenile
  setInterval(fetchUsers,     3000);
  setInterval(fetchLastUser,  3000);
  setInterval(fetchStats,     3000);
});
