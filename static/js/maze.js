let maze = []

function renderMazeBoard(
  maze,
  path = [],
  visited = [],
  stepMap = {},
  optimal = []
) {
  stepMap = stepMap || {}

  const table = document.getElementById('maze-board')
  table.innerHTML = ''

  // Convert to sets for faster lookups
  const visitedSet = new Set(visited.map(([i, j]) => `${i}-${j}`))
  const optimalSet = new Set(optimal.map(([i, j]) => `${i}-${j}`))
  const pathSet = new Set(path.map(([i, j]) => `${i}-${j}`))

  // First pass: render everything and mark optimal
  const cellRefs = [] // Cache references so we can overwrite with 'solution' later

  for (let i = 0; i < maze.length; i++) {
    const row = document.createElement('tr')
    const rowRefs = []

    for (let j = 0; j < maze[i].length; j++) {
      const cell = document.createElement('td')
      const val = maze[i][j]
      const key = `${i}-${j}`

      if (val === 1) {
        cell.className = 'wall'
      } else if (val === 'S') {
        cell.className = 'start'
      } else if (val === 'G') {
        cell.className = 'goal'
      } else if (optimalSet.has(key)) {
        cell.className = 'optimal'
      } else if (visitedSet.has(key)) {
        cell.className = 'visited'
      } else {
        cell.className = 'empty'
      }

      if (stepMap[key] !== undefined) {
        cell.textContent = stepMap[key]
      }

      row.appendChild(cell)
      rowRefs.push(cell)
    }

    table.appendChild(row)
    cellRefs.push(rowRefs)
  }

  // Second pass: apply solution (green) over the top
  for (const [i, j] of path) {
    const key = `${i}-${j}`
    const cell = cellRefs[i][j]

    // Don't overwrite start or goal
    if (maze[i][j] !== 'S' && maze[i][j] !== 'G') {
      cell.className = 'solution'
    }
  }
}

function fetchMaze() {
  fetch('/api/maze')
    .then((res) => res.json())
    .then((data) => {
      maze = data.maze || data
      path = []
      visited = []
      renderMazeBoard(maze)
      document.getElementById('maze-tab').style.display = 'block'
    })
}
function fetchMultiPathMaze() {
  fetch('/api/multi_path_maze')
    .then((res) => res.json())
    .then((data) => {
      maze = data.maze || data
      path = []
      visited = []
      renderMazeBoard(maze)
      document.getElementById('maze-tab').style.display = 'block'
    })
}

async function solveMazeAndRender(algorithm) {
  const res = await fetch(`/api/maze/solve?algorithm=${algorithm}`)
  const data = await res.json()

  if (data.error) {
    console.error(data.error)
    return
  }

  maze = data.maze
  path = data.path
  visited = data.visited
  const optimal = data.optimal || []
  renderStepNumbers(optimal)
}

function renderStepNumbers(optimal = []) {
  if (!path || path.length === 0) {
    console.warn('No path to render step numbers for.')
    return
  }

  const stepMap = {}
  path.forEach(([i, j], index) => {
    stepMap[`${i}-${j}`] = index
  })

  document.getElementById('num-steps').textContent = `Steps in path: ${
    path.length - 1
  }`

  renderMazeBoard(maze, path, visited, stepMap, optimal)
}

function copyMazeToClipboard() {
  if (!maze || maze.length === 0) {
    console.warn('Maze is empty or undefined.')
    return
  }

  const formatted = JSON.stringify(maze)

  // Copy to clipboard
  navigator.clipboard
    .writeText(formatted)
    .then(() => {
      console.log('Maze copied to clipboard!')
    })
    .catch((err) => {
      console.error('Failed to copy maze:', err)
    })
}
