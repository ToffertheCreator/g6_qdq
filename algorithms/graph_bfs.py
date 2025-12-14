from collections import deque

graph = {

    # ===== LRT-1 =====
    "Fernando Poe Jr.": ["Balintawak"],
    "Balintawak": ["Fernando Poe Jr.", "Monumento"],
    "Monumento": ["Balintawak", "5th Ave"],
    "5th Ave": ["Monumento", "R. Papa"],
    "R. Papa": ["5th Ave", "Abad Santos"],
    "Abad Santos": ["R. Papa", "Blumentritt"],
    "Blumentritt": ["Abad Santos", "Tayuman"],
    "Tayuman": ["Blumentritt", "Bambang"],
    "Bambang": ["Tayuman", "Doroteo Jose"],
    "Doroteo Jose": ["Bambang", "Carriedo", "Recto"],
    "Carriedo": ["Doroteo Jose", "Central Terminal"],
    "Central Terminal": ["Carriedo", "United Nations"],
    "United Nations": ["Central Terminal", "Pedro Gil"],
    "Pedro Gil": ["United Nations", "Quirino Ave"],
    "Quirino Ave": ["Pedro Gil", "Vito Cruz"],
    "Vito Cruz": ["Quirino Ave", "Gil Puyat"],
    "Gil Puyat": ["Vito Cruz", "Libertad"],
    "Libertad": ["Gil Puyat", "EDSA"],
    "EDSA": ["Libertad", "Baclaran", "Taft Ave"],
    "Baclaran": ["EDSA"],

    # ===== LRT-2 =====
    "Recto": ["Doroteo Jose", "Legarda"],
    "Legarda": ["Recto", "Pureza"],
    "Pureza": ["Legarda", "V. Mapa"],
    "V. Mapa": ["Pureza", "J. Ruiz"],
    "J. Ruiz": ["V. Mapa", "Gilmore"],
    "Gilmore": ["J. Ruiz", "Betty Go-Belmonte"],
    "Betty Go-Belmonte": ["Gilmore", "Cubao LRT"],
    "Cubao LRT": ["Betty Go-Belmonte", "Anonas", "Cubao MRT"],
    "Anonas": ["Cubao LRT", "Katipunan"],
    "Katipunan": ["Anonas", "Santolan LRT"],
    "Santolan LRT": ["Katipunan"],

    # ===== MRT-3 =====
    "North Ave": ["Quezon Ave"],
    "Quezon Ave": ["North Ave", "Kamuning"],
    "Kamuning": ["Quezon Ave", "Cubao MRT"],
    "Cubao MRT": ["Kamuning", "Santolan MRT", "Cubao LRT"],
    "Santolan MRT": ["Cubao MRT", "Ortigas"],
    "Ortigas": ["Santolan MRT", "Shaw Blvd"],
    "Shaw Blvd": ["Ortigas", "Boni"],
    "Boni": ["Shaw Blvd", "Guadalupe"],
    "Guadalupe": ["Boni", "Buendia"],
    "Buendia": ["Guadalupe", "Ayala"],
    "Ayala": ["Buendia", "Magallanes"],
    "Magallanes": ["Ayala", "Taft Ave"],
    "Taft Ave": ["Magallanes", "EDSA"]
}

def bfs_shortest_path(start, goal, graph=graph):
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        station = path[-1]

        if station==goal:
            return path
        
        if station not in visited:
            visited.add(station)
            for neighbor in graph.get(station, []):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    return None
