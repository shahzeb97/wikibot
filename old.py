import wikipedia as wp
import matplotlib.pyplot as plt
import networkx as nx

'''
Makes a network graph from a user-defined wikipedia article
Algorithm for Expansion
1. Initial Node
2. Go through all links on node
3. Find links who's word appears in the summary
4. Make new nodes and connections to all those links
5. Continue for other 

Information to Embed
    Nodes:
1. Word Count of Article (Size)
2. Date Article was created (Transparency)
3. Degrees of Separation from Initial (Colour)
    Edges:
1. Number of cross-references (Thickness)
2. 
'''

def search():
    # Select Starting Page
    topic = input('Initial Article: ')

    # Find matching statement or more specific one if it's ambiguous
    try:
        page = wp.page(title=topic)
    
    except wp.exceptions.DisambiguationError as e:
        print('Which "{}" do you mean?'.format(topic))
        options = [x for x in e.options if '(disambiguation)' not in x]
        for option in options:
            print('{:<5}{}'.format(e.options.index(option),option))
        choice = 'easter egg'
        while (not choice.isdigit()) or (int(choice) >= int(len(options))):
            choice = input('Select option (#): ')
            if int(choice) >= len(options):
                print('Number too high')
            elif choice.isdigit():
                topic = e.options[int(choice)]
            else:
                print('Invalid Option')
                pass
        
        page = wp.page(title=topic)
    
    return page.title

def expand_graph(root_title, nodes=[], edges=[], level=0, max_level=2):
    # Add page to node_set
    nodes += [root_title]

    if level < max_level:
        try:
            # Download the entire page
            root_page = wp.page(title=root_title)
        except wp.exceptions.PageError:
            return nodes, edges

        # Get links from root
        links = root_page.links
        
        # Get summary from root
        summary = root_page.summary

        # Recursively iterate through sub links if they are in summary
        for link in links:
            if link in summary:
                if link not in nodes:
                    edges += [(root_title,link)]
                    new_nodes, new_edges = expand_graph(link, nodes, edges, level+1)
                            
    return nodes, edges

def make_graph(nodes, edges):
    G = nx.Graph()
    fig, ax = plt.subplots()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    nx.draw(G, with_labels=True)
    plt.show()
    return

page = search()
nodes, edges = expand_graph(page)
make_graph(nodes, edges)
