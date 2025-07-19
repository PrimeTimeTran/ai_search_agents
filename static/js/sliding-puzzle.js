let board = []
let solved = false

function fetchBoard() {
  fetch('/api/puzzle')
    .then((res) => res.json())
    .then((data) => {
      board = data.board
      renderBoard()
    })
}

function renderBoard() {
  const table = document.getElementById('board')
  table.innerHTML = ''
  table.style.border = solved ? '3px solid green' : '1px solid #333'
  for (let i = 0; i < 4; i++) {
    const row = document.createElement('tr')
    for (let j = 0; j < 4; j++) {
      const cell = document.createElement('td')
      const val = board[i][j]
      cell.textContent = val === 0 ? '' : val
      if (val === 0) cell.className = 'empty'
      else cell.onclick = () => tryMove(i, j)
      row.appendChild(cell)
    }
    table.appendChild(row)
  }
}

function tryMove(i, j) {
  fetch('/api/move', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ row: i, col: j }),
  })
    .then((res) => res.json())
    .then((data) => {
      board = data.board
      solved = data.solved
      renderBoard()
      if (solved) {
        showToast('Puzzle solved!')
      }
    })
}

function fetchNewBoard() {
  fetch('/api/new_sliding_puzzle', { method: 'POST' })
    .then((res) => res.json())
    .then((data) => {
      // console.log('New board:', data.board)
      board = data.board
      renderBoard()
    })
}

function showToast(message) {
  const toast = document.getElementById('toast')
  toast.textContent = message
  toast.style.visibility = 'visible'
  setTimeout(() => {
    toast.style.visibility = 'hidden'
  }, 2000)
}

showTab('puzzle')
fetchBoard()
