# AI Search Agent

A fundamental pillar of AI is the Agent.

Agents are aware of the state of a problem space & take actions on them toward a goal.
For well defined problem spaces such as games like the 15 puzzle or maze path finder the state and actions taken are represented as a graph of nodes.
With this data structure we can use a DFS or BFS algorithm amongst others to come to a solution.

However, in taking actions toward a goal there can be one or more solutions found toward the path of our goal. At this point we must consider how we might optimize our solution. Thus at each node we must ascertain the path cost & evaluate whether or not we've reached our goal state.

This project demonstrates these foundational AI concepts with a few games.

## Deployment

```sh
./deploy.sh
```
