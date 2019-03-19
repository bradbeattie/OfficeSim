#!/usr/bin/env python3
from collections import deque
from constants import Desires
from msp import MinimumSpanningTree
from pathfinding.core.diagonal_movement import DiagonalMovement
import math
import random


PATHING_MSP = MinimumSpanningTree(diagonal_movement=DiagonalMovement.always)


class Agent():
    def __init__(self, name, all_agents, grid, scheduler):
        self.name = name
        self.grid = grid
        self.desires = {
            desire: 0.0 if desire == Desires.EXIT else 1.0
            for desire in Desires
        }
        self.active_desire = None
        self.all_agents = all_agents
        self.scheduler = scheduler

        self.current_position = None

    def step_to(self, node):
        if node == self.current_position:
            return
        if self.current_position:
            self.current_position.agents.remove(self)
            self.current_position.weight -= 10
        self.current_position = node
        self.current_position.agents.add(self)
        self.current_position.weight += 10

    def perform_action(self):
        if not self.current_position:
            self.step_to(random.choice(list(self.grid.spawns)))

        elif not self.active_desire or self.desires[self.active_desire] <= 0:
            self.gen_desire()

        elif self.active_desire in self.current_position.satisfies:
            self.satisfy_desire()

        else:
            self.move_towards_desire()

        self.increment_desires()
        self.schedule_action()

    def gen_desire(self):
        assert self.desires, "Agent has no desires"
        try:
            self.active_desire = random.choices(
                list(self.desires.keys()),
                list(self.desires.values()),
            )[0]
        except Exception:
            self.active_desire = Desires.WORK

    def satisfy_desire(self):
        self.desires[self.active_desire] *= 0.8
        self.desires[self.active_desire] -= 2

        if len(self.current_position.agents) > 1:
            self.move_towards_desire()

        elif random.uniform(0, 1) < 0.05: 
            nodes = [
                node
                for node in PATHING_MSP.find_neighbors(self.grid, self.current_position)
                if all((
                    not node.closed,
                    not node.agents,
                    self.active_desire in node.satisfies,
                ))
            ]
            if nodes:
                self.step_to(random.choice(nodes))

    def move_towards_desire(self):
        path, runs = PATHING_MSP.find_path(
            self.current_position,
            lambda node: self.active_desire in node.satisfies and not node.agents,
            self.grid
        )
        self.grid.cleanup()
        if path:
            self.step_to(path[1])  # TODO: Probably worth optimizing. We generate a path, and then throw all but the first step out. Maybe remember a few steps to cut back on this?
        else:
            # Couldn't find an available location to satisfy the active
            # desire. Let's generate a new desire and try again.
            self.gen_desire()

    def increment_desires(self):
        for desire in Desires:
            self.desires[desire] += 0.0 if desire == Desires.EXIT else 1.0

    def schedule_action(self):
        self.scheduler.enter(
            random.uniform(0.1, 0.5 if self.current_position else 10),
            1,
            self.perform_action,
        )

#print("PATH FROM 6,6 TO NEAREST BATHROOM NODE (CONSIDER WEIGHT, USE DIAGONALS)")
#msp = MinimumSpanningTree(diagonal_movement=DiagonalMovement.always)
#path, runs = msp.find_path(grid.node(6, 6), lambda node: Desires.BATHROOM in node.satisfies, grid)
#print(grid.grid_str(
#    path=path,
#    start=path[0],
#    end=path[-1],
#))
