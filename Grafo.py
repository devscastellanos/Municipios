import networkx as nx
import folium

def shortest_paths_to_destino(G,municipio_origen, municipio_destino):
    shortest_paths_dijkstra = {}
    shortest_paths_astar = {}

    # Calcular el camino más corto usando Dijkstra desde cada municipio hasta el destino
    shortest_path = nx.shortest_path(G, source=municipio_origen, target=municipio_destino, weight='weight')
    shortest_distance = nx.shortest_path_length(G, source=municipio_origen, target=municipio_destino, weight='weight')
    shortest_paths_dijkstra[municipio_origen] = {"path": shortest_path, "distance": shortest_distance}

    # Calcular el camino más corto usando A* desde cada municipio hasta el destino
    shortest_path = nx.astar_path(G, source=municipio_origen, target=municipio_destino, weight='weight')
    shortest_distance = nx.astar_path_length(G, source=municipio_origen, target=municipio_destino, weight='weight')
    shortest_paths_astar[municipio_origen] = {"path": shortest_path, "distance": shortest_distance}

    return shortest_paths_dijkstra, shortest_paths_astar

def main():
    # Definir el grafo y los municipios
    G = nx.MultiDiGraph()

    municipios = [
        ("armenia",5.120730670623553, -75.52729707759781), ("bogota",4.718053568114313, -74.06658286745144), ("cali",3.5789827143414126, -76.58929061461298), 
        ("cartagena",10.496444164668606, -75.45901276372226),("cucuta",7.9047253501007, -72.5696086268443),("ibague",4.549441498536578, -75.29567685960617), 
        ("manizales",5.140580712416249, -75.42751278908962), ("medellin",6.342991090657202, -75.56484188230154), ("monteria",8.798617353870156, -75.83950008275438), 
        ("neiva",2.993669310618653, -75.28749978065257),("pasto",1.2070625462429003, -77.28623500589828), ("pereira",4.807347684510505, -75.69173445872742), 
        ("popayan",2.445550522724912, -76.61177957088165), ("quibdo",5.695461820855649, -76.65121550139872), ("sincelejo",9.305349792815962, -75.39328315093385),
        ("tunja",5.545101781863523, -73.3576152272728), ("villavo",4.14975368862445, -73.62931702804678), ("arauca",7.0903,-70.7617), ("mocoa",1.1478352782174623, -76.64783640817116), 
        ("yopal",5.349069797742737, -72.40121322204848)
    ]

    conexiones = [
        ("armenia", "bogota", 286), ("armenia", "cali", 194),
        ("bogota", "cartagena", 1178), ("bogota", "cucuta", 649),
        ("cali", "ibague", 279), ("cali", "manizales", 275),
        ("yopal", "manizales", 609), ("cartagena", "monteria", 300),
        ("cucuta", "neiva", 951), ("cucuta", "tunja", 502),
        ("ibague", "pereira", 125), ("ibague", "popayan", 428),
        ("manizales", "quibdo", 501), ("medellin", "sincelejo", 441),
        ("manizales", "tunja", 446), ("manizales", "villavo", 415),
        ("monteria", "arauca", 1141), ("villavo", "mocoa", 715),
        ("mocoa", "cali", 487), 
        ("yopal", "arauca", 422), ("cartagena", "yopal", 1128),
        ("manizales", "pasto", 675), ("manizales", "cartagena", 879),
        ("neiva", "cucuta", 9510),
        ("pasto", "mocoa", 103), ("pereira", "armenia", 44),
        ("popayan", "pereira", 373), 
        ("sincelejo", "manizales", 694), ("tunja", "medellin", 699),
        ("villavo", "medellin", 668), ("arauca", "cucuta", 346),
        ("mocoa", "monteria", 1319), ("mocoa", "neiva", 327)
    ]

    for municipio in municipios:
        G.add_node(municipio)

    for conexion in conexiones:
        G.add_edge(conexion[0], conexion[1], weight=conexion[2])

    # Pedir al usuario que ingrese el municipio de destino
    municipio_origen = input("Ingrese el nombre del municipio de origen: ")

    municipio_destino = input("Ingrese el nombre del municipio de destino: ")

    def get_lat_lng(municipios, conexiones):
        # Crear un mapa centrado en Colombia
        mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

        # Agregar marcadores para cada municipio
        for municipio in municipios:
            folium.Marker(
                location=[municipio[1], municipio[2]],
                popup= f"{municipio[0]}<br>Latitud: {municipio[1]}<br>Longitud: {municipio[2]}",
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(mapa)
            
        for conexion in conexiones:
            ciudad_origen = conexion[0]
            ciudad_destino = conexion[1]
            distancia = conexion[2]
            # Obtener las coordenadas de las ciudades
            origen_coords = [m[1:3] for m in municipios if m[0] == ciudad_origen][0]
            destino_coords = [m[1:3] for m in municipios if m[0] == ciudad_destino][0]
            # Crear una línea entre las ciudades
            folium.PolyLine([origen_coords, destino_coords], color="red", weight=2, opacity=1).add_to(mapa)

        # Guardar el mapa como un archivo HTML
        mapa.save("mapa_municipios.html")

        # Mostrar el mapa
        mapa


    # Calcular los caminos más cortos usando Dijkstra y A*
    shortest_paths_dijkstra, shortest_paths_astar = shortest_paths_to_destino(G,municipio_origen, municipio_destino)

    # Mostrar los resultados
    print("Resultados usando Dijkstra:")
    for municipio_origen, data in shortest_paths_dijkstra.items():
        print(f"Camino más corto desde {municipio_origen} hasta {municipio_destino}:")
        print(data["path"])
        print(f"Distancia: {data['distance']} km")

    print("\nResultados usando A*:")
    for municipio_origen, data in shortest_paths_astar.items():
        print(f"Camino más corto desde {municipio_origen} hasta {municipio_destino}:")
        print(data["path"])
        print(f"Distancia: {data['distance']} km")

    get_lat_lng(municipios, conexiones)

if __name__ == "__main__":
    main()