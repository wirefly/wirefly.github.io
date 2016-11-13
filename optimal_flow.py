import numpy as np
from scipy import optimize
from Model.BipartiteNetworkGraph import BipartiteNetworkGraph


def solve_optimal(payments_list):
    """
    Takes in a list of Payments and finds the optimal flow values
    from country to country.
    :param payments_list: list of Payments given from the Backend
    :return:              a list of flow values for each edge from country to country
    """
    capacity_graph, cost_graph = initialize(payments_list)
    min_weights, constraint_matrix, constraint_res = formulate_simplex(capacity_graph, cost_graph)
    flow_vals = run_simplex(min_weights, constraint_matrix, constraint_res)
    return flow_vals


def initialize(payments_list):
    """
    Takes in a list of Payments and constructs two NetworkGraph objects
    that represent a graph whose edge weights are capacities and another
    graph whose edge weights are cut percentages.
    :param payments_list: list of Payments given from the Backend
    :return:              two Graph objects
    """
    net_payments = calculate_net_payments(payments_list)
    losers = [(net_amount, currency) for net_amount, currency in net_payments if net_amount < 0]
    gainers = [(net_amount, currency) for net_amount, currency in net_payments if net_amount > 0]   # TODO: Handle == 0 case
    L, R = len(losers), len(gainers)
    V = len(net_payments)
    cost_graph, capacity_graph = BipartiteNetworkGraph(V), BipartiteNetworkGraph(V)

    for index, (net_amount, currency) in enumerate(net_payments):
        v = index + 1
        if(net_amount < 0):
            capacity_graph.add_edge((capacity_graph.s, v), abs(net_amount))
            cost_graph.add_edge((cost_graph.s, v), 0)
        elif(net_amount > 0):
            capacity_graph.add_edge((v, capacity_graph.t), abs(net_amount))
            cost_graph.add_edge((v, cost_graph.t), 0)

        cost_graph.set_currency(v, currency)
        capacity_graph.set_currency(v, currency)

    for u in range(L):
        for v in range(R):
            send_currency, receive_currency = cost_graph.get_currency(u), cost_graph.get_currency(v)
            exchange_rate = send_currency.get_exchange_rate(receive_currency)
            capacity_graph.add_edge((u,v), float('inf'))
            cost_graph.add_edge((u,v), exchange_rate)

    return cost_graph, capacity_graph


def calculate_net_payments(payment_list):
    """
        Takes in a list of Payments and constructs a sorted list of
        tuples of the form (net_amount, currency)
        :param payments_list: list of Payments given from the Backend
        :return:              list of tuples
        """
    net_payments = {}
    for payment in payment_list:
        sender, receiver = payment.get_sender(), payment.get_receiver()
        if sender.get_currency() not in net_payments:
            net_payments[sender.get_currency()] = - payment.get_amount()
        else:
            net_payments[sender.get_currency()] -= payment.get_amount()

        if receiver.get_currency() not in net_payments:
            net_payments[receiver.get_currency()] = payment.get_amount()
        else:
            net_payments[sender.get_currency()] += payment.get_amount()
    return sorted([(net_payments[currency], currency) for currency in net_payments])


def formulate_simplex(capacity_graph, cost_graph):
    """
    Takes in a capacity graph and cost graph in order to output
    c, A, b such that we form inputs readable by Simplex.
    :param capacity_graph: the graph holding edge weights as capacities.
    :param cost_graph:     the graph holding edge weights as cut percentages.
    :return:               parameters for simplex to function.
    """
    L, R = capacity_graph.get_L(), capacity_graph.get_R()
    total_dim = L * R + R + L
    min_weights = np.append(cost_graph.s_to_L, cost_graph.flatten_matrix())
    min_weights = np.append(min_weights, cost_graph.R_to_T)

    constraint_matrix = np.array([1] * L + [0] * (L * R + R))
    constraint_matrix = np.vstack((constraint_matrix, np.ones(shape=(L, total_dim))))
    constraint_matrix = np.vstack((constraint_matrix, np.ones(shape=(R, total_dim))))

    protruding_edges = capacity_graph.get_out_edges(capacity_graph.s)
    terminal_edges = capacity_graph.get_in_edges(capacity_graph.t)

    constraint_res = np.array([sum(protruding_edges)])
    constraint_res = np.append(constraint_res, protruding_edges)
    constraint_res = np.append(constraint_res, terminal_edges)
    return min_weights, constraint_matrix, constraint_res


def run_simplex(c, A_equality, b_equality):
    """
    Run simplex with the given parameters.
    :param c:          the weights for the minimization function.
    :param A_equality: the weights for the constraint equations.
    :param b_equality: the values for the constraint equations.
    :return:           the result of calling simplex.
    """
    return optimize.linprog(c, A_eq=A_equality, b_eq=b_equality, method='simplex')


# TODO: Actually implement
def get_currency_account(currency):
    return 'fake bank'


class Payment():
    def __init__(self, a, b, c):
        return


def get_transcations_for_currency(currency, total_fees, total_amount_sent):
    transactions = []
    currency_bank = get_currency_account(currency)
    for payment in currency_bank.get_out_payments():
        payment_amount = payment.get_amount()
        sender, receiver = payment.get_sender(), payment.get_receiver()
        transactions += [Payment(sender, currency_bank, payment_amount)]
        transactions += [Payment(currency_bank, receiver - (total_fees)*(payment_amount/total_amount_sent), payment_amount)]
    return transactions

