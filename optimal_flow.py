import numpy as np
from scipy import optimize
from Model.BipartiteNetworkGraph import BipartiteNetworkGraph
from Model.Payment import Payment


def solve_optimal(payments_list):
    """
    Takes in a list of Payments and finds the optimal flow values
    from country to country.
    :param payments_list: list of Payments given from the Backend
    :return:              total cost
    """
    cost_graph, capacity_graph = initialize(payments_list)
    min_weights, constraint_matrix, constraint_res, constraint_matrix_ineq, constraint_res_ineq = formulate_simplex(
            capacity_graph, cost_graph)
    flow_val = run_simplex(min_weights, constraint_matrix, constraint_res, constraint_matrix_ineq, constraint_res_ineq)
    transactions = get_transcations(payments_list, flow_val)
    return transactions


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
    gainers = [(net_amount, currency) for net_amount, currency in net_payments if net_amount > 0]
    L, R = len(losers), len(gainers)
    V = len(net_payments)
    cost_graph, capacity_graph = BipartiteNetworkGraph(L, R), BipartiteNetworkGraph(L, R)

    for index, (net_amount, currency) in enumerate(net_payments):
        v = index + 1
        if (net_amount < 0):
            capacity_graph.add_edge((capacity_graph.s, v), abs(net_amount))
            cost_graph.add_edge((cost_graph.s, v), 0)
        elif (net_amount > 0):
            capacity_graph.add_edge((v, capacity_graph.t), abs(net_amount))
            cost_graph.add_edge((v, cost_graph.t), 0)

        cost_graph.set_currency(v, currency)
        capacity_graph.set_currency(v, currency)

    for u in range(1, L + 1):
        for v in range(L, R + L):
            send_currency, receive_currency = cost_graph.get_currency(u), cost_graph.get_currency(v)
            fee_rate = send_currency.get_fee_rate(receive_currency)
            capacity_graph.add_edge((u, v), float('inf'))
            cost_graph.add_edge((u, v), fee_rate)

    return cost_graph, capacity_graph


def calculate_net_payments(payment_list):
    """
        Takes in a list of Payments and constructs a sorted list of
        tuples of the form (net_amount, currency)
        :param payments_list: list of Payments given from the Backend
        :return:              list of tuples
        """
    net_payments = {}
    currency_name_map = {}
    for payment in payment_list:
        sender, receiver = payment.sender, payment.receiver
        currency_name_map[sender.currency.country] = sender.currency
        if sender.currency.country not in net_payments:
            net_payments[sender.currency.country] = - payment.amount
        else:
            net_payments[sender.currency.country] -= int(payment.amount)

        currency_name_map[receiver.currency.country] = receiver.currency
        if receiver.currency.country not in net_payments:
            net_payments[receiver.currency.country] = payment.amount
        else:
            net_payments[sender.currency.country] += int(payment.amount)
    return sorted([(net_payments[currency], currency_name_map[currency]) for currency in net_payments], key=lambda x: x[0])


def get_currency_to_payment_hash(payment_list):
    payments = {}
    for payment in payment_list:
        sender, receiver = payment.sender, payment.receiver
        if sender.currency not in payments:
            payments[sender.currency.country] = payment
        else:
            payments[sender.currency.country] = payment

    return payments


def get_currency_name_to_object_hash(payment_list):
    currencies = {}
    for payment in payment_list:
        sender, receiver = payment.sender, payment.receiver
        if sender.currency not in currencies:
            currencies[sender.currency.country] = sender.currency
        if receiver.currency not in currencies:
            currencies[receiver.currency.country] = receiver.currency

    return currencies

def get_total_amount_sent(payment_list):
    return sum([int(payment.amount) for payment in payment_list])


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
    for lr_edge_index in range(L):
        mat_row = [0] * total_dim
        for ones_index in range(L + lr_edge_index * R, L + (lr_edge_index + 1) * R):
            mat_row[ones_index] = 1
        constraint_matrix = np.vstack((constraint_matrix, np.array(mat_row)))

    for lr_edge_index in range(R):
        mat_row = [0] * total_dim
        for ones_index in range(L):
            mat_row[L + lr_edge_index + R * ones_index] = 1
        constraint_matrix = np.vstack((constraint_matrix, np.array(mat_row)))

    constraint_matrix = np.vstack((constraint_matrix, np.array([0] * (L * R + L) + [1] * R)))
    constraint_matrix_ineq = np.eye(total_dim)

    protruding_edges = capacity_graph.get_out_edges(capacity_graph.s)
    terminal_edges = capacity_graph.get_in_edges(capacity_graph.t)

    constraint_res = np.array([sum(protruding_edges)])
    constraint_res = np.append(constraint_res, protruding_edges)
    constraint_res = np.append(constraint_res, terminal_edges)
    constraint_res = np.append(constraint_res, np.array([sum(terminal_edges)]))

    constraint_res_ineq = protruding_edges
    constraint_res_ineq = np.append(constraint_res_ineq, capacity_graph.flatten_matrix())
    constraint_res_ineq = np.append(constraint_res_ineq, terminal_edges)

    print('minimum constraints', min_weights)
    print('A', constraint_matrix)
    print('b', constraint_res)
    print('A_ineq', constraint_matrix_ineq)
    print('b_ineq', constraint_res_ineq)
    return min_weights, constraint_matrix, constraint_res, constraint_matrix_ineq, constraint_res_ineq


def run_simplex(c, A_equality, b_equality, A_inequality, b_inequality):
    """
    Run simplex with the given parameters.
    :param c:          the weights for the minimization function.
    :param A_equality: the weights for the constraint equations.
    :param b_equality: the values for the constraint equations.
    :return:           the result of calling simplex.
    """
    opt = optimize.linprog(c, A_eq=A_equality, b_eq=b_equality, A_ub=A_inequality, b_ub=b_inequality, method='simplex')
    print(opt)  # TODO DELETE
    return opt.fun


def get_transcations(payment_list, total_fees):

    currency_to_payment = get_currency_to_payment_hash(payment_list)
    currency_name_to_object = get_currency_name_to_object_hash(payment_list)
    total_amount_sent = get_total_amount_sent(payment_list
                                              )
    transactions = []
    for currency_name in currency_to_payment:
        payment = currency_to_payment[currency_name]
        currency_account = currency_name_to_object[currency_name]
        payment_amount = payment.amount
        sender, receiver = payment.sender, payment.receiver
        transactions += [Payment(sender, currency_account, payment_amount)]
        transactions += [Payment(currency_account, receiver, payment_amount - ((total_fees) * (1.0 * payment_amount / total_amount_sent)))]
    return transactions
