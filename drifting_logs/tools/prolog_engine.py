"""
Prolog Engine (Declarative Relational Resolution Engine)
Supports multi-hop unification, negation-as-failure, recursive reachability, and complex constraint queries.
"""

from typing import List, Dict, Any, Union

class Term:
    def __init__(self, name: str, args: List[Any] = None):
        self.name = str(name)
        self.args = args if args is not None else []

    def is_var(self):
        return isinstance(self.name, str) and (self.name.startswith("?") or (len(self.name) > 0 and self.name[0].isupper()))

    def __repr__(self):
        if not self.args:
            return str(self.name)
        return f"{self.name}({', '.join(map(str, self.args))})"

    def __eq__(self, other):
        return isinstance(other, Term) and self.name == other.name and self.args == other.args

    def __hash__(self):
        return hash((self.name, tuple(self.args)))

class Rule:
    def __init__(self, head: Term, body: List[Term] = None):
        self.head = head
        self.body = body if body is not None else []

    def __repr__(self):
        if not self.body:
            return f"{self.head}."
        return f"{self.head} :- {', '.join(map(str, self.body))}."

class KnowledgeBase:
    def __init__(self):
        self.rules: List[Rule] = []

    def assertz(self, head_or_rule: Union[Term, Rule], body: List[Term] = None):
        if isinstance(head_or_rule, Rule):
            self.rules.append(head_or_rule)
        else:
            self.rules.append(Rule(head_or_rule, body))

    def query(self, goal: Term) -> List[Dict[str, str]]:
        results = []
        self._solve([goal], {}, results, depth=0)
        query_vars = get_vars(goal)
        filtered = []
        for subst in results:
            clean_subst = {}
            for v in query_vars:
                val = deref(Term(v), subst)
                clean_subst[v] = str(val)
            if clean_subst not in filtered:
                filtered.append(clean_subst)
        return filtered

    def _solve(self, goals: List[Term], env: Dict[str, Any], results: List[Dict[str, Any]], depth: int = 0):
        if depth > 25: # Prevent infinite stack overflow on recursive loops
            return
        if not goals:
            results.append(env)
            return

        current_goal = goals[0]

        # Handle negation-as-failure: not(Goal)
        if current_goal.name == "not" and len(current_goal.args) == 1:
            sub_goal = current_goal.args[0]
            sub_results = []
            self._solve([sub_goal], env, sub_results, depth + 1)
            if not sub_results:
                self._solve(goals[1:], env, results, depth + 1)
            return

        for rule in self.rules:
            renamed_rule = rename_vars(rule)
            new_env = env.copy()
            if unify(current_goal, renamed_rule.head, new_env):
                self._solve(renamed_rule.body + goals[1:], new_env, results, depth + 1)

_var_counter = 0
def rename_vars(rule: Rule) -> Rule:
    global _var_counter
    _var_counter += 1
    suffix = f"_{_var_counter}"

    def rename_term(t: Any) -> Any:
        if not isinstance(t, Term):
            return t
        if t.is_var():
            return Term(t.name + suffix)
        return Term(t.name, [rename_term(a) for a in t.args])

    return Rule(rename_term(rule.head), [rename_term(b) for b in rule.body])

def get_vars(t: Term) -> List[str]:
    vars_found = []
    if t.is_var():
        vars_found.append(t.name)
    for arg in t.args:
        if isinstance(arg, Term):
            vars_found.extend(get_vars(arg))
    return list(dict.fromkeys(vars_found))

def deref(t: Any, env: Dict[str, Any]) -> Any:
    if not isinstance(t, Term):
        return t
    if t.is_var():
        if t.name in env:
            return deref(env[t.name], env)
        return t
    if t.args:
        return Term(t.name, [deref(a, env) for a in t.args])
    return t

def unify(t1: Any, t2: Any, env: Dict[str, Any]) -> bool:
    t1 = deref(t1, env)
    t2 = deref(t2, env)

    if t1 == t2:
        return True

    if isinstance(t1, Term) and t1.is_var():
        if isinstance(t2, Term) and t2.is_var() and t1.name == t2.name:
            return True
        env[t1.name] = t2
        return True

    if isinstance(t2, Term) and t2.is_var():
        if isinstance(t1, Term) and t1.is_var() and t1.name == t2.name:
            return True
        env[t2.name] = t1
        return True

    if isinstance(t1, Term) and isinstance(t2, Term):
        if t1.name == t2.name and len(t1.args) == len(t2.args):
            for a1, a2 in zip(t1.args, t2.args):
                if not unify(a1, a2, env):
                    return False
            return True

    return False

def build_psychogeographical_kb() -> KnowledgeBase:
    kb = KnowledgeBase()

    # Facts - Direct Systemic Connections
    kb.assertz(Term("commute_dependency", [Term("saint_saturnin"), Term("a75_corridor")]))
    kb.assertz(Term("platform_lockin", [Term("a75_corridor"), Term("connected_car")]))
    kb.assertz(Term("metabolic_exhaustion", [Term("connected_car"), Term("youth_inertia")]))
    kb.assertz(Term("institutional_desert", [Term("youth_inertia"), Term("medical_desert")]))

    kb.assertz(Term("industrial_memory", [Term("montceau_les_mines"), Term("belfort_lure")]))
    kb.assertz(Term("ecological_anomaly", [Term("aire_de_la_guye"), Term("a75_corridor")]))
    kb.assertz(Term("autonomous_counter_signal", [Term("mond_arverne"), Term("saint_saturnin")]))

    # Direct edge relation
    kb.assertz(Term("linked", [Term("saint_saturnin"), Term("a75_corridor")]))
    kb.assertz(Term("linked", [Term("a75_corridor"), Term("connected_car")]))
    kb.assertz(Term("linked", [Term("connected_car"), Term("youth_inertia")]))
    kb.assertz(Term("linked", [Term("youth_inertia"), Term("medical_desert")]))

    # Rules
    kb.assertz(Rule(
        Term("entropic_corridor", [Term("X"), Term("Z")]),
        [
            Term("commute_dependency", [Term("X"), Term("Y")]),
            Term("platform_lockin", [Term("Y"), Term("Z")])
        ]
    ))

    kb.assertz(Rule(
        Term("feedback_loop", [Term("X"), Term("Z")]),
        [
            Term("entropic_corridor", [Term("X"), Term("Y")]),
            Term("metabolic_exhaustion", [Term("Y"), Term("Z")])
        ]
    ))

    kb.assertz(Rule(
        Term("systemic_trap", [Term("X"), Term("W")]),
        [
            Term("feedback_loop", [Term("X"), Term("Z")]),
            Term("institutional_desert", [Term("Z"), Term("W")])
        ]
    ))

    # Multi-hop Reachability Rule
    kb.assertz(Rule(
        Term("reachable", [Term("X"), Term("Y")]),
        [Term("linked", [Term("X"), Term("Y")])]
    ))
    kb.assertz(Rule(
        Term("reachable", [Term("X"), Term("Y")]),
        [
            Term("linked", [Term("X"), Term("Z")]),
            Term("reachable", [Term("Z"), Term("Y")])
        ]
    ))

    # Unresolved Trap Query using Negation as Failure
    kb.assertz(Rule(
        Term("unresolved_trap", [Term("X"), Term("Y")]),
        [
            Term("systemic_trap", [Term("X"), Term("Y")]),
            Term("not", [Term("autonomous_counter_signal", [Term("X"), Term("Y")])])
        ]
    ))

    return kb

if __name__ == "__main__":
    kb = build_psychogeographical_kb()
    print("Entropic Corridor:", kb.query(Term("entropic_corridor", [Term("X"), Term("Z")])))
    print("Feedback Loop:", kb.query(Term("feedback_loop", [Term("X"), Term("Z")])))
    print("Systemic Trap:", kb.query(Term("systemic_trap", [Term("X"), Term("W")])))
    print("Multi-hop Reachable (saint_saturnin -> ?):", kb.query(Term("reachable", [Term("saint_saturnin"), Term("Y")])))
