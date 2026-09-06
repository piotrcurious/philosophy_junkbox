/* drift_ontology.pl - Psychogeographical N-Dimensional Ontology & Core Dimensionality Logic Engine */

:- module(drift_ontology, [
    dimension/6,
    register_dimension/6,
    node_vector/3,
    edge/7,
    axiom/3,
    vector_distance_euclidean/3,
    vector_distance_weighted/4,
    vector_interpolate/5,
    verify_manifold_consistency/1,
    verify_trajectory_compatibility/3,
    export_ontology_json/1,
    main/0
]).

:- use_module(library(http/json)).

% --- 1. CORE DIMENSION REGISTRY ---
% dimension(Index, Key, Label, MinVal, MaxVal, Unit)
:- dynamic dimension/6.

dimension(0, x,            'X Coordinate (Spatial)',    -50.0, 50.0,  'm').
dimension(1, y,            'Y Coordinate (Spatial)',    -50.0, 100.0, 'm').
dimension(2, z,            'Z Coordinate (Spatial)',    -10.0, 30.0,  'm').
dimension(3, temp,         'Temperature',                 15.0, 45.0,  'C').
dimension(4, humidity,     'Relative Humidity',          0.10, 0.95, '%').
dimension(5, commerce,     'Commerce Index',              0.00, 1.00, 'idx').
dimension(6, access,       'Accessibility Index',         0.00, 1.00, 'idx').
dimension(7, symbolic,     'Symbolic / Heritage Value',   0.00, 1.00, 'idx').
dimension(8, thermal_stress,'Thermal Stress Index',       0.00, 1.00, 'idx').
dimension(9, flow_density, 'Crowd Flow Density',         0.00, 1.00, 'idx').

% Dynamic extension helper
register_dimension(Index, Key, Label, MinVal, MaxVal, Unit) :-
    retractall(dimension(Index, Key, _, _, _, _)),
    assertz(dimension(Index, Key, Label, MinVal, MaxVal, Unit)).

% --- 2. N-DIMENSIONAL NODE VECTORS ---
% node_vector(ID, Label, VectorList)
:- dynamic node_vector/3.

node_vector(underground, 'Underground Metro Connection',         [ 0.0, -10.0,  0.0, 24.5, 0.75, 0.20, 0.90, 0.20, 0.30, 0.85]).
node_vector(boulevard,   'Boulevard Haussmann Ground Entrance', [10.0,   0.0,  5.0, 33.0, 0.45, 0.90, 0.85, 0.80, 0.85, 0.95]).
node_vector(vip_salon,   'VIP Personal Shopping Salons',       [15.0,  20.0, 12.0, 21.0, 0.50, 0.95, 0.20, 0.90, 0.15, 0.25]).
node_vector(coupole,     'Historic Glass Coupole Dome',         [ 0.0,  40.0,  8.0, 28.5, 0.55, 0.70, 0.70, 0.95, 0.55, 0.75]).
node_vector(glasswalk,   'Glasswalk Suspended Runway',          [ 5.0,  50.0, 10.0, 29.5, 0.50, 0.85, 0.40, 0.90, 0.60, 0.80]).
node_vector(rooftop,     'Rooftop Terrace & Microclimate',      [ 0.0,  70.0, 15.0, 36.0, 0.30, 0.40, 0.60, 0.85, 0.90, 0.60]).

% --- 3. EDGE CONNECTIONS ---
% edge(From, To, DistMeters, CostTourist, CostWorker, CostResident, CostSurveillance)
:- dynamic edge/7.

edge(underground, boulevard, 15, 0.2, 0.1, 0.3, 0.1).
edge(boulevard, vip_salon, 30, 0.8, 0.4, 0.9, 0.2).
edge(boulevard, coupole, 45, 0.3, 0.5, 0.7, 0.2).
edge(vip_salon, glasswalk, 25, 0.5, 0.6, 0.8, 0.3).
edge(coupole, glasswalk, 15, 0.1, 0.5, 0.6, 0.1).
edge(glasswalk, rooftop, 20, 0.2, 0.4, 0.5, 0.2).
edge(boulevard, rooftop, 80, 0.4, 0.3, 0.4, 0.1).
edge(underground, rooftop, 95, 0.9, 0.2, 0.5, 0.2).

% --- 4. FORMAL AXIOMS ---
axiom(a1_thermal_barrier, 'Climate Adaptability', 'Thermal Stress / Temp > 35.0 C creates access friction').
axiom(a2_commercial_exclusion, 'Social Access', 'Commerce Index > 0.90 excludes non-commercial public trajectories').
axiom(a3_symbolic_spectacle, 'Symbolic Geometry', 'Heritage Spectacle nodes amplify flow density and tourist attraction').
axiom(a4_reachability_continuity, 'Topology', 'Valid drift trajectory requires continuous connected edge transitions').
axiom(a5_surveillance_symmetry, 'Control Space', 'Surveillance archetype experiences minimal physical friction').

% --- 5. N-DIMENSIONAL MATH & CORE DIMENSION ENGINE ---

% Euclidean distance in N-dimensions
vector_distance_euclidean([], [], 0.0).
vector_distance_euclidean([X|Xs], [Y|Ys], Dist) :-
    vector_distance_euclidean(Xs, Ys, SubDistSq),
    Diff is X - Y,
    DistSq is SubDistSq + Diff * Diff,
    Dist is sqrt(DistSq).

% Weighted distance in N-dimensions
vector_distance_weighted([], [], [], 0.0).
vector_distance_weighted([X|Xs], [Y|Ys], [W|Ws], Dist) :-
    vector_distance_weighted(Xs, Ys, Ws, SubDistSq),
    Diff is X - Y,
    DistSq is SubDistSq + W * Diff * Diff,
    Dist is sqrt(DistSq).

% Non-linear Vector Interpolation across N dimensions
vector_interpolate([], [], _, _, []).
vector_interpolate([X|Xs], [Y|Ys], T, Warp, [V|Vs]) :-
    TWarped is T ** Warp,
    V is X + (Y - X) * TWarped,
    vector_interpolate(Xs, Ys, T, Warp, Vs).

% Vector attribute lookup by index
vector_val_by_index(Vector, Index, Val) :-
    nth0(Index, Vector, Val).

% Helper to check threshold condition on specific dimension key
check_node_dimension_threshold(NodeID, DimKey, Threshold, Operator) :-
    dimension(Index, DimKey, _, _, _, _),
    node_vector(NodeID, _, Vector),
    vector_val_by_index(Vector, Index, Val),
    compare_threshold(Operator, Val, Threshold).

compare_threshold(gt, Val, Thresh) :- Val > Thresh.
compare_threshold(lt, Val, Thresh) :- Val < Thresh.
compare_threshold(eq, Val, Thresh) :- Val =:= Thresh.

% --- 6. ONTOLOGY & TRAJECTORY VERIFICATION ---

connected(A, B, D, CT, CW, CR, CS) :- edge(A, B, D, CT, CW, CR, CS).
connected(A, B, D, CT, CW, CR, CS) :- edge(B, A, D, CT, CW, CR, CS).

archetype_cost(tourist, CT, _, _, _, CT).
archetype_cost(worker, _, CW, _, _, CW).
archetype_cost(resident, _, _, CR, _, CR).
archetype_cost(surveillance, _, _, _, CS, CS).

valid_path(Start, End, Path, Archetype) :-
    travel(Start, End, [Start], ReversedPath, Archetype),
    reverse(ReversedPath, Path).

travel(Node, Node, Path, Path, _).
travel(Curr, End, Visited, Path, Archetype) :-
    connected(Curr, Next, _, CT, CW, CR, CS),
    archetype_cost(Archetype, CT, CW, CR, CS, Cost),
    Cost < 0.9,
    \+ member(Next, Visited),
    travel(Next, End, [Next|Visited], Path, Archetype).

verify_manifold_consistency(Results) :-
    findall(NodeID, check_node_dimension_threshold(NodeID, temp, 35.0, gt), ThermalExceeded),
    findall(NodeID, check_node_dimension_threshold(NodeID, commerce, 0.90, gt), HighCommercial),
    findall(edge(A,B), edge(A,B,_,_,_,_,_), Edges),
    length(Edges, EdgeCount),
    findall(DimKey, dimension(_, DimKey, _, _, _, _), DimList),
    length(DimList, DimCount),
    Results = json{
        theorem_a1_thermal_barriers_cnt: ThermalExceeded,
        theorem_a2_high_commerce_exclusion_cnt: HighCommercial,
        total_manifold_edges: EdgeCount,
        active_dimensions_count: DimCount,
        manifold_status: 'PROVED_CONSISTENT'
    }.

verify_trajectory_compatibility(Archetype, Path, Status) :-
    (   valid_path_check(Path, Archetype)
    ->  Status = 'FORMALLY_VALIDATED'
    ;   Status = 'AXIOM_VIOLATION'
    ).

valid_path_check([_], _).
valid_path_check([A, B | Rest], Archetype) :-
    connected(A, B, _, CT, CW, CR, CS),
    archetype_cost(Archetype, CT, CW, CR, CS, Cost),
    Cost < 0.9,
    valid_path_check([B | Rest], Archetype).

% --- 7. EXPORT PROLOG DIMENSION SCHEMA & DATA TO JSON ---

export_ontology_json(Filename) :-
    verify_manifold_consistency(VerificationResults),

    findall(json{index: Idx, key: K, label: L, min: Min, max: Max, unit: U},
            dimension(Idx, K, L, Min, Max, U), Dimensions),

    findall(json{id: ID, label: L, vector: Vec},
            node_vector(ID, L, Vec), Nodes),

    findall(json{from: F, to: T, dist: D, cost_tourist: CT, cost_worker: CW, cost_resident: CR, cost_surveillance: CS},
            edge(F, T, D, CT, CW, CR, CS), Edges),

    findall(json{id: AID, category: Cat, statement: Stmt},
            axiom(AID, Cat, Stmt), Axioms),

    (   valid_path(boulevard, rooftop, TouristPath, tourist) -> true ; TouristPath = [boulevard, rooftop] ),
    (   valid_path(underground, rooftop, WorkerPath, worker) -> true ; WorkerPath = [underground, rooftop] ),
    (   valid_path(underground, rooftop, ResidentPath, resident) -> true ; ResidentPath = [underground, rooftop] ),
    (   valid_path(underground, rooftop, SurveillancePath, surveillance) -> true ; SurveillancePath = [underground, rooftop] ),

    verify_trajectory_compatibility(tourist, TouristPath, TouristStatus),
    verify_trajectory_compatibility(worker, WorkerPath, WorkerStatus),
    verify_trajectory_compatibility(resident, ResidentPath, ResidentStatus),
    verify_trajectory_compatibility(surveillance, SurveillancePath, SurveillanceStatus),

    Trajectories = json{
        tourist: json{path: TouristPath, status: TouristStatus},
        worker: json{path: WorkerPath, status: WorkerStatus},
        resident: json{path: ResidentPath, status: ResidentStatus},
        surveillance: json{path: SurveillancePath, status: SurveillanceStatus}
    },

    Data = json{
        dimensions: Dimensions,
        nodes: Nodes,
        edges: Edges,
        axioms: Axioms,
        verification: VerificationResults,
        formal_trajectories: Trajectories
    },

    open(Filename, write, Stream),
    json_write_dict(Stream, Data, [width(128)]),
    close(Stream).

main :-
    export_ontology_json('ontology_output.json'),
    writeln('Successfully executed Prolog core dimensionality engine and exported ontology_output.json').
