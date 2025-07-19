let maze = []

async function renderMazeBoard(
  maze,
  path = [],
  visited = [],
  stepMap = {},
  optimal = []
) {
  stepMap = stepMap || {}

  const table = document.getElementById('maze-board')
  table.innerHTML = ''

  const visitedSet = new Set(visited.map(([i, j]) => `${i}-${j}`))
  const optimalSet = new Set(optimal.map(([i, j]) => `${i}-${j}`))
  const pathSet = new Set(path.map(([i, j]) => `${i}-${j}`))

  const cellRefs = []

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

  await animateCells(path, 'solution', 15)

  await animateCells(optimal, 'optimal', 15, pathSet)

  async function animateCells(
    cells,
    className,
    delay = 20,
    skipSet = new Set()
  ) {
    for (const [i, j] of cells) {
      const key = `${i}-${j}`
      const cell = cellRefs[i][j]

      if (maze[i][j] === 'S' || maze[i][j] === 'G') continue
      if (skipSet.has(key)) continue

      cell.className = className
      await new Promise((resolve) => setTimeout(resolve, delay))
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

  navigator.clipboard
    .writeText(formatted)
    .then(() => {
      console.log('Maze copied to clipboard!')
    })
    .catch((err) => {
      console.error('Failed to copy maze:', err)
    })
}
