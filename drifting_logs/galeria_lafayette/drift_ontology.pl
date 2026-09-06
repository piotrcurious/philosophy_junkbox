/* drift_ontology.pl - Psychogeographical Event-Relational Prolog Ontology */

:- module(drift_ontology, [node/6, edge/7, valid_path/4, export_ontology_json/1, main/0]).
:- use_module(library(http/json)).

% node(ID, Label, Level, TempC, CommerceIdx, SymbolicCategory)
node(underground, 'Underground Metro Connection', -1, 24.5, 0.20, 'Infrastructure').
node(boulevard,   'Boulevard Haussmann Ground Entrance', 0, 33.0, 0.90, 'Commercial Street').
node(vip_salon,   'VIP Personal Shopping Salons', 2, 21.0, 0.95, 'Exclusivity').
node(coupole,     'Historic Glass Coupole Dome', 4, 28.5, 0.70, 'Heritage Spectacle').
node(glasswalk,   'Glasswalk Suspended Runway', 5, 29.5, 0.85, 'Tourist Landmark').
node(rooftop,     'Rooftop Terrace & Microclimate', 7, 36.0, 0.40, 'Viewpoint Oasis').

% edge(From, To, DistMeters, CostTourist, CostWorker, CostResident, CostSurveillance)
edge(underground, boulevard, 15, 0.2, 0.1, 0.3, 0.1).
edge(boulevard, vip_salon, 30, 0.8, 0.4, 0.9, 0.2).
edge(boulevard, coupole, 45, 0.3, 0.5, 0.7, 0.2).
edge(vip_salon, glasswalk, 25, 0.5, 0.6, 0.8, 0.3).
edge(coupole, glasswalk, 15, 0.1, 0.5, 0.6, 0.1).
edge(glasswalk, rooftop, 20, 0.2, 0.4, 0.5, 0.2).
edge(boulevard, rooftop, 80, 0.4, 0.3, 0.4, 0.1).
edge(underground, rooftop, 95, 0.9, 0.2, 0.5, 0.2).

% Symmetric path finding
connected(A, B, D, CT, CW, CR, CS) :- edge(A, B, D, CT, CW, CR, CS).
connected(A, B, D, CT, CW, CR, CS) :- edge(B, A, D, CT, CW, CR, CS).

% Trajectory search
valid_path(Start, End, Path, Archetype) :-
    travel(Start, End, [Start], ReversedPath, Archetype),
    reverse(ReversedPath, Path).

travel(Node, Node, Path, Path, _).
travel(Curr, End, Visited, Path, Archetype) :-
    connected(Curr, Next, _, CT, CW, CR, CS),
    archetype_cost(Archetype, CT, CW, CR, CS, Cost),
    Cost < 0.9, % Cost threshold
    \+ member(Next, Visited),
    travel(Next, End, [Next|Visited], Path, Archetype).

archetype_cost(tourist, CT, _, _, _, CT).
archetype_cost(worker, _, CW, _, _, CW).
archetype_cost(resident, _, _, CR, _, CR).
archetype_cost(surveillance, _, _, _, CS, CS).

% Export ontology data to JSON format
export_ontology_json(Filename) :-
    findall(json{id: ID, label: L, level: Lev, temp: T, commerce: C, symbol: S},
            node(ID, L, Lev, T, C, S), Nodes),
    findall(json{from: F, to: T, dist: D, cost_tourist: CT, cost_worker: CW, cost_resident: CR, cost_surveillance: CS},
            edge(F, T, D, CT, CW, CR, CS), Edges),
    Data = json{nodes: Nodes, edges: Edges},
    open(Filename, write, Stream),
    json_write_dict(Stream, Data),
    close(Stream).

main :-
    export_ontology_json('ontology_output.json'),
    writeln('Successfully generated ontology_output.json').
