#!/usr/bin/env python3
from agent import Agent
from config import LAYOUT, DESIRES, SPAWNS, NAMES
from constants import Desires
from gridplus import GridPlus
from msp import MinimumSpanningTree
from pathfinding.core.diagonal_movement import DiagonalMovement
import itertools
import random
import sched


def paint_desire(grid, origin, max_distance, desire):
    msp = MinimumSpanningTree(
        diagonal_movement=DiagonalMovement.always,
        weighted=True,
    )
    display = set()
    for node in itertools.takewhile(
        lambda node: node.f < max_distance,
        msp.itertree(grid, origin),
    ):
        node.satisfies.add(desire)
        display.add(node)
    grid.cleanup()


def run_sim():
    agents = {}
    scheduler = sched.scheduler()
    grid = GridPlus(LAYOUT)

    grid.spawns = set([grid.node(*spawn) for spawn in SPAWNS])
    for desire in DESIRES:
        paint_desire(grid, grid.node(*desire[0]), *desire[1:])


    def show_status():
        for agent in agents.values():
            print(agent.name, agent.active_desire)
        print(grid.grid_str())
        scheduler.enter(0.2, 1, show_status)
    scheduler.enter(0.5, 1, show_status)

    for k in NAMES:
        agent = Agent(k, agents, grid, scheduler)
        agent.schedule_action()
        agents[k] = agent
    scheduler.run()

if __name__ == "__main__":
    run_sim()
