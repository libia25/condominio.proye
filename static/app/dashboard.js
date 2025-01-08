  // Configuración del gráfico
  const ctx = document.getElementById('paymentsChart').getContext('2d');
  const paymentsChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
          labels: ['Total Pagado', 'Total Pendiente'],
          datasets: [{
              label: 'Pagos',
              data: [{{ total_pagado|escapejs }}, {{ total_pendiente|escapejs }}],
              backgroundColor: ['#4caf50', '#ff5252'],
              hoverOffset: 4
          }]
      },
      options: {
          responsive: true,
          plugins: {
              legend: {
                  position: 'top',
              }
          }
      }
  });