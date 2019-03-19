#!/usr/bin/env python3
from pathfinding.core.grid import Grid


class GridPlus(Grid):
    def __init__(self, layout):
        super().__init__(self, matrix=[
            [
                0 if char == "#" else int(char)
                for char in row
            ]
            for row in layout.strip("\n").splitlines()
        ])

        for y_nodes in self.nodes:
            for node in y_nodes:
                node.satisfies = set()
                node.agents = set()

    def grid_str(self, path=None, start=None, end=None,
                 border=True, start_chr='s', end_chr='e',
                 path_chr='x', empty_chr=' ', block_chr='#',
                 show_weight=False):
        """
        create a printable string from the grid using ASCII characters

        :param path: list of nodes that show the path
        :param start: start node
        :param end: end node
        :param border: create a border around the grid
        :param start_chr: character for the start (default "s")
        :param end_chr: character for the destination (default "e")
        :param path_chr: character to show the path (default "x")
        :param empty_chr: character for empty fields (default " ")
        :param block_chr: character for blocking elements (default "#")
        :param show_weight: instead of empty_chr show the cost of each empty
                            field (shows a + if the value of weight is > 10)
        :return:
        """
        data = ''
        if border:
            data = '+{}+'.format('-'*len(self.nodes[0]))
        for y in range(len(self.nodes)):
            line = ''
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                if node == start:
                    line += start_chr
                elif node == end:
                    line += end_chr
                elif path and ((node.x, node.y) in path or node in path):
                    line += path_chr
                elif node.agents:
                    line += list(node.agents)[0].name[0]
                elif node.walkable:
                    # empty field
                    weight = str(node.weight) if node.weight < 10 else '+'
                    line += weight if show_weight else empty_chr
                else:
                    line += block_chr  # blocked field
            if border:
                line = '|'+line+'|'
            if data:
                data += '\n'
            data += line
        if border:
            data += '\n+{}+'.format('-'*len(self.nodes[0]))
        return data
