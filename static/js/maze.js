let maze = []

function renderMazeBoard(maze, path = [], visited = [], stepMap = {}) {
  stepMap = stepMap || {}

  const table = document.getElementById('maze-board')
  table.innerHTML = ''

  const pathSet = new Set(path.map(([i, j]) => `${i}-${j}`))
  const visitedSet = new Set(visited.map(([i, j]) => `${i}-${j}`))

  for (let i = 0; i < maze.length; i++) {
    const row = document.createElement('tr')
    for (let j = 0; j < maze[i].length; j++) {
      const cell = document.createElement('td')
      const val = maze[i][j]
      const key = `${i}-${j}`

      if (val === 1) cell.className = 'wall'
      else if (val === 'S') cell.className = 'start'
      else if (val === 'G') cell.className = 'goal'
      else if (pathSet.has(`${i}-${j}`)) cell.className = 'solution'
      else if (visitedSet.has(`${i}-${j}`)) cell.className = 'visited'
      else cell.className = 'empty'

      if (Object.prototype.hasOwnProperty.call(stepMap, key)) {
        cell.textContent = stepMap[key]
      }

      row.appendChild(cell)
    }
    table.appendChild(row)
  }
}

function fetchMaze() {
  fetch('/api/maze')
    .then((res) => res.json())
    .then((data) => {
      maze = data.maze || data // support both formats
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

  maze = data.maze // make sure we use the current maze
  path = data.path
  visited = data.visited

  renderMazeBoard(maze, path, visited)
}

function renderStepNumbers() {
  if (!visited || visited.length === 0) {
    console.warn('No visited nodes to render steps for.')
    return
  }

  const stepMap = {}
  const queue = []
  const visitedSet = new Set(visited.map(([i, j]) => `${i}-${j}`))

  // Find 'S' (start) cell
  let start = null
  for (let i = 0; i < maze.length; i++) {
    for (let j = 0; j < maze[i].length; j++) {
      if (maze[i][j] === 'S') {
        start = [i, j]
        break
      }
    }
    if (start) break
  }

  if (!start) {
    console.error("Start 'S' not found in maze")
    return
  }

  // Initialize BFS from 'S'
  queue.push({ pos: start, steps: 0 })
  const seen = new Set()
  seen.add(`${start[0]}-${start[1]}`)

  const directions = [
    [0, 1],
    [1, 0],
    [0, -1],
    [-1, 0],
  ]

  while (queue.length > 0) {
    const { pos, steps } = queue.shift()
    const [i, j] = pos
    const key = `${i}-${j}`

    if (visitedSet.has(key)) {
      stepMap[key] = steps
    }

    for (const [di, dj] of directions) {
      const ni = i + di
      const nj = j + dj
      const nextKey = `${ni}-${nj}`

      if (
        ni >= 0 &&
        ni < maze.length &&
        nj >= 0 &&
        nj < maze[0].length &&
        maze[ni][nj] !== 1 &&
        !seen.has(nextKey)
      ) {
        seen.add(nextKey)
        queue.push({ pos: [ni, nj], steps: steps + 1 })
      }
    }
  }

  renderMazeBoard(maze, path, visited, stepMap)
}
