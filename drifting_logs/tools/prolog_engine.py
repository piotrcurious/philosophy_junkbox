"""
Prolog Engine (Declarative Relational Resolution Engine & Executable Prolog Axioms)
Supports multi-hop unification, negation-as-failure, recursive reachability, built-in arithmetic evaluation (`is`, `less_than`, `greater_than`),
list membership (`member`), compound goal string parsing, infix operator syntax (`is`, `<`, `>`),
dynamic fact/rule retract/update, and transitive relation composition rules for complex epistemological axioms.
"""

import re
import ast
import operator
from typing import List, Dict, Any, Union, Optional, Tuple
import cmath

class Term:
    def __init__(self, name: Any, args: List[Any] = None):
        self.name = str(name)
        self.args = args if args is not None else []

    def is_var(self):
        if not isinstance(self.name, str) or not self.name:
            return False
        if self.name.startswith("?"):
            return True
        if self.name in ("STRONGLY_ATTRACTIVE", "ATTRACTIVE", "NEUTRAL", "REPULSIVE", "BARRIER"):
            return False
        # Enum constants are uppercase with non-digit suffixes like STRONGLY_ATTRACTIVE
        if re.match(r'^[A-Z]+_[A-Z]+', self.name):
            return False
        return self.name[0].isupper()

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

    def retract(self, head_name: str, head_args: Optional[List[str]] = None) -> int:
        """Removes rules or facts matching head_name and optionally head_args."""
        initial_count = len(self.rules)
        new_rules = []
        for r in self.rules:
            if r.head.name == head_name:
                if head_args is not None:
                    str_args = [str(a) for a in r.head.args]
                    if str_args == head_args:
                        continue
                else:
                    continue
            new_rules.append(r)
        self.rules = new_rules
        return initial_count - len(self.rules)

    def query(self, goals: Union[Term, List[Term]]) -> List[Dict[str, str]]:
        if isinstance(goals, Term):
            goals = [goals]

        results = []
        self._solve(goals, {}, results, depth=0)

        # Extract all query variables across goals
        query_vars = []
        for g in goals:
            for v in get_vars(g):
                if v not in query_vars:
                    query_vars.append(v)

        filtered = []
        for subst in results:
            clean_subst = {}
            for v in query_vars:
                val = deref(Term(v), subst)
                clean_subst[v] = str(val)
            if clean_subst not in filtered:
                filtered.append(clean_subst)
        return filtered

    def get_all_rules_repr(self) -> List[str]:
        return [str(r) for r in self.rules]

    def _eval_arithmetic(self, expr_str: str, env: Dict[str, Any]) -> Optional[float]:
        try:
            # Replace variables in expr_str with values from env
            for var_name, var_val in list(env.items()):
                val_deref = deref(Term(var_name), env)
                expr_str = expr_str.replace(str(var_name), str(val_deref))

            allowed_operators = {
                ast.Add: operator.add, ast.Sub: operator.sub,
                ast.Mult: operator.mul, ast.Div: operator.truediv,
                ast.Pow: operator.pow, ast.USub: operator.neg,
                ast.UAdd: operator.pos
            }
            def _eval_node(node):
                if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                    return float(node.value)
                elif isinstance(node, ast.BinOp):
                    return allowed_operators[type(node.op)](_eval_node(node.left), _eval_node(node.right))
                elif isinstance(node, ast.UnaryOp):
                    return allowed_operators[type(node.op)](_eval_node(node.operand))
                raise ValueError("Unsupported AST node")

            tree = ast.parse(expr_str, mode='eval')
            return float(_eval_node(tree.body))
        except Exception:
            return None

    def _solve(self, goals: List[Term], env: Dict[str, Any], results: List[Dict[str, Any]], depth: int = 0):
        if depth > 35: # Prevent stack overflow on recursive loops
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

        # Built-in Predicate: is(Var, Expression)
        if current_goal.name == "is" and len(current_goal.args) == 2:
            target_var = current_goal.args[0]
            expr_term = current_goal.args[1]
            eval_val = self._eval_arithmetic(str(expr_term), env)
            if eval_val is not None:
                new_env = env.copy()
                if unify(target_var, Term(str(round(eval_val, 4))), new_env):
                    self._solve(goals[1:], new_env, results, depth + 1)
            return

        # Built-in Predicate: less_than(A, B)
        if current_goal.name == "less_than" and len(current_goal.args) == 2:
            val_a = self._eval_arithmetic(str(current_goal.args[0]), env)
            val_b = self._eval_arithmetic(str(current_goal.args[1]), env)
            if val_a is not None and val_b is not None and val_a < val_b:
                self._solve(goals[1:], env, results, depth + 1)
            return

        # Built-in Predicate: greater_than(A, B)
        if current_goal.name == "greater_than" and len(current_goal.args) == 2:
            val_a = self._eval_arithmetic(str(current_goal.args[0]), env)
            val_b = self._eval_arithmetic(str(current_goal.args[1]), env)
            if val_a is not None and val_b is not None and val_a > val_b:
                self._solve(goals[1:], env, results, depth + 1)
            return

        # Built-in Predicate: member(Elem, ListTerm)
        if current_goal.name == "member" and len(current_goal.args) == 2:
            elem = current_goal.args[0]
            list_arg = current_goal.args[1]
            items = [Term(a.strip()) for a in str(list_arg.name).split(',') if a.strip()] if not list_arg.args else list_arg.args
            for item in items:
                new_env = env.copy()
                if unify(elem, item, new_env):
                    self._solve(goals[1:], new_env, results, depth + 1)
            return

        # Standard Rule Matching
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


def parse_term_string(term_str: str) -> Term:
    term_str = term_str.strip()

    # Infix operator parsing: X is Expr
    if ' is ' in term_str:
        left, right = term_str.split(' is ', 1)
        return Term("is", [parse_term_string(left), parse_term_string(right)])

    # Infix operator parsing: X < Y or X less_than Y
    if ' less_than ' in term_str:
        left, right = term_str.split(' less_than ', 1)
        return Term("less_than", [parse_term_string(left), parse_term_string(right)])
    elif '<' in term_str and not '(' in term_str:
        left, right = term_str.split('<', 1)
        return Term("less_than", [parse_term_string(left), parse_term_string(right)])

    # Infix operator parsing: X > Y or X greater_than Y
    if ' greater_than ' in term_str:
        left, right = term_str.split(' greater_than ', 1)
        return Term("greater_than", [parse_term_string(left), parse_term_string(right)])
    elif '>' in term_str and not '(' in term_str:
        left, right = term_str.split('>', 1)
        return Term("greater_than", [parse_term_string(left), parse_term_string(right)])

    m = re.match(r'^\s*(\w+)\s*\((.*)\)\s*$', term_str)
    if not m:
        return Term(term_str)

    pred_name = m.group(1)
    args_raw = m.group(2)

    args = []
    depth = 0
    curr = []
    for char in args_raw:
        if char == '(':
            depth += 1
            curr.append(char)
        elif char == ')':
            depth -= 1
            curr.append(char)
        elif char == ',' and depth == 0:
            args.append(''.join(curr).strip())
            curr = []
        else:
            curr.append(char)
    if curr:
        args.append(''.join(curr).strip())

    return Term(pred_name, [parse_term_string(a) for a in args if a])


def parse_goals_string(goals_str: str) -> List[Term]:
    goals_str = goals_str.strip().rstrip('.')
    if not goals_str:
        return []

    goal_strs = []
    depth = 0
    curr = []
    for char in goals_str:
        if char == '(':
            depth += 1
            curr.append(char)
        elif char == ')':
            depth -= 1
            curr.append(char)
        elif char == ',' and depth == 0:
            goal_strs.append(''.join(curr).strip())
            curr = []
        else:
            curr.append(char)
    if curr:
        goal_strs.append(''.join(curr).strip())

    return [parse_term_string(g) for g in goal_strs if g]


def parse_rule_string(rule_str: str) -> Rule:
    rule_str = rule_str.strip().rstrip('.')
    if ':-' in rule_str:
        head_part, body_part = rule_str.split(':-', 1)
        head_term = parse_term_string(head_part)
        body_terms = parse_goals_string(body_part)
        return Rule(head_term, body_terms)
    else:
        head_term = parse_term_string(rule_str)
        return Rule(head_term, [])


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

    # Quantized Relation Classes and Cost Thresholds
    kb.assertz(Term("relation_class", [Term("saint_saturnin"), Term("a75_corridor"), Term("STRONGLY_ATTRACTIVE")]))
    kb.assertz(Term("relation_class", [Term("a75_corridor"), Term("connected_car"), Term("ATTRACTIVE")]))
    kb.assertz(Term("relation_class", [Term("connected_car"), Term("youth_inertia"), Term("REPULSIVE")]))
    kb.assertz(Term("relation_class", [Term("youth_inertia"), Term("medical_desert"), Term("BARRIER")]))
    kb.assertz(Term("relation_class", [Term("aire_de_la_guye"), Term("a75_corridor"), Term("NEUTRAL")]))

    # Discrete Relation Composition Facts (R1 x R2 -> R3)
    kb.assertz(Term("rel_compose", [Term("STRONGLY_ATTRACTIVE"), Term("STRONGLY_ATTRACTIVE"), Term("STRONGLY_ATTRACTIVE")]))
    kb.assertz(Term("rel_compose", [Term("STRONGLY_ATTRACTIVE"), Term("ATTRACTIVE"), Term("ATTRACTIVE")]))
    kb.assertz(Term("rel_compose", [Term("ATTRACTIVE"), Term("ATTRACTIVE"), Term("ATTRACTIVE")]))
    kb.assertz(Term("rel_compose", [Term("ATTRACTIVE"), Term("REPULSIVE"), Term("REPULSIVE")]))
    kb.assertz(Term("rel_compose", [Term("REPULSIVE"), Term("BARRIER"), Term("BARRIER")]))

    # Transitive Quantized Relation Composition Rules
    kb.assertz(Rule(
        Term("transitive_rel", [Term("X"), Term("Y"), Term("R")]),
        [Term("relation_class", [Term("X"), Term("Y"), Term("R")])]
    ))
    kb.assertz(Rule(
        Term("transitive_rel", [Term("X"), Term("Z"), Term("R3")]),
        [
            Term("relation_class", [Term("X"), Term("Y"), Term("R1")]),
            Term("transitive_rel", [Term("Y"), Term("Z"), Term("R2")]),
            Term("rel_compose", [Term("R1"), Term("R2"), Term("R3")])
        ]
    ))

    # Ontological Domain Mapping Facts
    kb.assertz(Term("ontological_domain", [Term("gdp"), Term("macroeconomic"), Term("country")]))
    kb.assertz(Term("ontological_domain", [Term("temperature"), Term("physical_field"), Term("grid_point")]))
    kb.assertz(Term("ontological_domain", [Term("flow"), Term("directed_pair"), Term("graph_edge")]))

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

    # Psychogeographical Phase Boundary Rule (NEUTRAL or BARRIER relation transition)
    kb.assertz(Rule(
        Term("psychogeographical_boundary", [Term("X"), Term("Y")]),
        [Term("relation_class", [Term("X"), Term("Y"), Term("NEUTRAL")])]
    ))
    kb.assertz(Rule(
        Term("psychogeographical_boundary", [Term("X"), Term("Y")]),
        [Term("relation_class", [Term("X"), Term("Y"), Term("BARRIER")])]
    ))

    return kb


class PrologAxiomProgram:
    """
    Executable Prolog Program representing Epistemological Axioms as Logical Rules.
    Allows runtime extension, rule injection, dynamic retraction, compound goal queries,
    and logical deduction of Axiom Parameters.
    """
    def __init__(self, kb: Optional[KnowledgeBase] = None):
        self.kb = kb if kb is not None else build_psychogeographical_kb()
        self._init_axiom_rules()

    def _init_axiom_rules(self):
        """Define default Prolog rule sets for complex field axioms."""
        # Kępiński Metabolic Axiom Program
        self.kb.assertz(Term("kepinski_metabolic_state", [Term("high_entropy"), Term("1.8"), Term("0.9")]))
        self.kb.assertz(Term("kepinski_metabolic_state", [Term("homeostatic"), Term("1.2"), Term("0.3")]))

        self.kb.assertz(Rule(
            Term("derive_m_axiom", [Term("Real"), Term("Imag"), Term("State")]),
            [Term("kepinski_metabolic_state", [Term("State"), Term("Real"), Term("Imag")])]
        ))

        # Ashby Requisite Variety Axiom Program
        self.kb.assertz(Term("ashby_variety_state", [Term("hyper_variable"), Term("2.5"), Term("-0.8")]))
        self.kb.assertz(Term("ashby_variety_state", [Term("constrained"), Term("1.1"), Term("-0.2")]))

        self.kb.assertz(Rule(
            Term("derive_v_axiom", [Term("Real"), Term("Imag"), Term("State")]),
            [Term("ashby_variety_state", [Term("State"), Term("Real"), Term("Imag")])]
        ))

        # Girard Mimetic Axiom Program
        self.kb.assertz(Term("girard_mimetic_state", [Term("resonant"), Term("0.8"), Term("1.2")]))
        self.kb.assertz(Term("girard_mimetic_state", [Term("isolated"), Term("0.2"), Term("0.1")]))

        self.kb.assertz(Rule(
            Term("derive_mu_axiom", [Term("Real"), Term("Imag"), Term("State")]),
            [Term("girard_mimetic_state", [Term("State"), Term("Real"), Term("Imag")])]
        ))

        # Debord Spectacle Axiom Program
        self.kb.assertz(Term("debord_spectacle_state", [Term("alienated"), Term("1.5"), Term("0.6")]))
        self.kb.assertz(Term("debord_spectacle_state", [Term("authentic"), Term("0.4"), Term("0.05")]))

        self.kb.assertz(Rule(
            Term("derive_sigma_axiom", [Term("Real"), Term("Imag"), Term("State")]),
            [Term("debord_spectacle_state", [Term("State"), Term("Real"), Term("Imag")])]
        ))

    def inject_fact(self, fact_name: str, args: List[str]):
        """Asserts a new relational fact into the Prolog KB."""
        self.kb.assertz(Term(fact_name, [Term(a) for a in args]))

    def retract_relation(self, head_name: str, head_args: Optional[List[str]] = None) -> int:
        """Retracts matching facts or rules from the Prolog KB."""
        return self.kb.retract(head_name, head_args)

    def inject_rule(self, head_str: str, head_args: List[str], body_terms: List[Tuple[str, List[str]]] = None):
        """Allows runtime extensibility by injecting custom user/agent Prolog rules."""
        head = Term(head_str, [Term(a) for a in head_args])
        body = []
        if body_terms:
            for b_name, b_args in body_terms:
                body.append(Term(b_name, [Term(a) for a in b_args]))
        self.kb.assertz(Rule(head, body))

    def inject_rule_string(self, rule_str: str):
        """Parses and injects full Prolog rule string e.g. 'path(X, Y) :- linked(X, Z), path(Z, Y).'"""
        parsed_rule = parse_rule_string(rule_str)
        self.kb.assertz(parsed_rule)

    def parse_and_query_string(self, query_str: str) -> List[Dict[str, str]]:
        """Parses compound query string e.g. 'linked(?X, ?Y), relation_class(?Y, ?Z, STRONGLY_ATTRACTIVE)'"""
        goals = parse_goals_string(query_str)
        return self.kb.query(goals)

    def evaluate_axiom_values(self, m_state: str = "high_entropy", v_state: str = "hyper_variable",
                              mu_state: str = "resonant", sigma_state: str = "alienated") -> Dict[str, complex]:
        """Queries Prolog KB to derive exact complex values for M, V, mu, Sigma."""
        q_m = self.kb.query(Term("derive_m_axiom", [Term("R"), Term("I"), Term(m_state)]))
        m_val = complex(float(q_m[0]["R"]), float(q_m[0]["I"])) if q_m else (1.5 + 0.8j)

        q_v = self.kb.query(Term("derive_v_axiom", [Term("R"), Term("I"), Term(v_state)]))
        v_val = complex(float(q_v[0]["R"]), float(q_v[0]["I"])) if q_v else (2.2 - 0.5j)

        q_mu = self.kb.query(Term("derive_mu_axiom", [Term("R"), Term("I"), Term(mu_state)]))
        mu_val = complex(float(q_mu[0]["R"]), float(q_mu[0]["I"])) if q_mu else (0.7 + 1.1j)

        q_sig = self.kb.query(Term("derive_sigma_axiom", [Term("R"), Term("I"), Term(sigma_state)]))
        sigma_val = complex(float(q_sig[0]["R"]), float(q_sig[0]["I"])) if q_sig else (1.2 + 0.4j)

        return {
            "M": m_val,
            "V": v_val,
            "mu": mu_val,
            "Sigma": sigma_val
        }

if __name__ == "__main__":
    prog = PrologAxiomProgram()
    vals = prog.evaluate_axiom_values()
    print("Derived Axiom Values:", vals)
    print("Transitive Multi-hop Query:", prog.parse_and_query_string("transitive_rel(saint_saturnin, ?Y, ?R)"))
    print("Built-in Arithmetic Query:", prog.kb.query(parse_goals_string("?X is 10 + 5, ?X > 12")))
