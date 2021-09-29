import random
import asyncio
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import graph_things
import matplotlib
from matplotlib import rcParams

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

# Antiport states


O_IN = 0
P_IN = 1
P_OUT = 2
O_OUT = 3
S_OUT = 4
S_IN = 5

# Symport States
A_IN = 0
IN = 1
OUT = 2
A_OUT = 3
AB_OUT = 4
AB_IN = 5


# Antiport individual rates
au_a = 1000
aw_a = 100
au_b = 1000
aw_b = 100
aGAMMA = 1
aX = 2
auap = 100
aubp = 120

antiport_defaults = [au_a, aw_a, au_b, aw_b, aGAMMA, aX, auap, aubp]

# Symport individual rates
su_a = 1000
sw_a = 1000
su_b = 100
sw_b = 1000
sGAMMA = 1
sX = 2
suap = 100
subp = 500



symport_defaults = [su_a, sw_a, su_b, sw_b, sGAMMA, sX, suap, subp]


TOTAL_TIME = 500


P_FLOW_INCREMENT = 1
S_FLOW_INCREMENT = 1






# times = []
# p_inflows = []
# s_inflows = []
# state_times_antiport = [0, 0, 0, 0, 0, 0]
# state_times_symport = [0, 0, 0, 0, 0, 0, 0, 0]
# cur_row = -1

def run_once(isAntiport, params):
    return run_once_graph(isAntiport, params, False)


def run_once_graph(isAntiport, params, graph):
    time = 0
    p_inflow = 0
    s_inflow = 0
    u_a = params[0]
    w_a = params[1]
    u_b = params[2]
    w_b = params[3]
    GAMMA = params[4]
    X = params[5]
    uap = params[6]
    ubp = params[7]
    state_times = [0, 0, 0, 0, 0, 0]

    if graph:
        prev_inflow_time = 0
        prev_outflow_time = 0
        prev_flow_time = 0
        p_inflow_times = []
        p_outflow_times = []
        p_flow_times = []
    if isAntiport:
        state = O_IN
        rates = [[0, u_a, 0, GAMMA, 0, u_b],
                 [w_a, 0, GAMMA * X, 0, 0, 0],
                 [0, GAMMA * X, 0, w_a, 0, 0],
                 [GAMMA, 0, uap, 0, ubp, 0],
                 [0, 0, 0, w_b, 0, GAMMA * X],
                 [w_b, 0, 0, 0, GAMMA * X, 0]]
    else:
        state = IN
        rates = [[0, w_a, 0, GAMMA * X, 0, u_b],
                 [u_a, 0, GAMMA, 0, 0, 0],
                 [0, GAMMA, 0, uap, 0, 0],
                 [GAMMA * X, 0, w_a, 0, ubp, 0],
                 [0, 0, 0, w_b, 0, GAMMA],
                 [w_b, 0, 0, 0, GAMMA, 0]]
    while time < TOTAL_TIME:
        reaction_rate = sum(rates[state])

        rand_t = random.random()
        rand_r = random.random()

        rxn_time = (1 / reaction_rate) * np.log(1 / rand_t)
        time += rxn_time
        state_times[state] += rxn_time / TOTAL_TIME

        prob = 0
        prev_state = state
        for i in range(len(rates)):
            prob += (rates[state][i] / reaction_rate)
            if (prob > rand_r):
                state = i
                break
        if isAntiport:
            if prev_state == P_IN and state == P_OUT:
                p_inflow -= P_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == P_OUT and state == P_IN:
                p_inflow += P_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == S_IN and state == S_OUT:
                s_inflow -= S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == S_OUT and state == S_IN:
                s_inflow += S_FLOW_INCREMENT / TOTAL_TIME
            if graph:
                if prev_state == P_IN and state == P_OUT:
                    p_inflow -= P_FLOW_INCREMENT / TOTAL_TIME
                    p_outflow_times.append(time - prev_outflow_time)
                    p_flow_times.append(time - prev_flow_time)
                    prev_outflow_time = time
                    prev_flow_time = time
                elif prev_state == P_OUT and state == P_IN:
                    p_inflow += P_FLOW_INCREMENT / TOTAL_TIME
                    p_inflow_times.append(time - prev_inflow_time)
                    p_flow_times.append(time - prev_flow_time)
                    prev_inflow_time = time
                    prev_flow_time = time
        else:
            if prev_state == AB_IN and state == AB_OUT:
                p_inflow += P_FLOW_INCREMENT / TOTAL_TIME
                s_inflow += S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == AB_OUT and state == AB_IN:
                p_inflow -= P_FLOW_INCREMENT / TOTAL_TIME
                s_inflow -= S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == A_IN and state == A_OUT:
                p_inflow += P_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == A_OUT and state == A_IN:
                p_inflow -= P_FLOW_INCREMENT / TOTAL_TIME
    if graph:
        plt.hist(p_flow_times, 250)
        plt.title("Flow Times, x = " + str(params[5]) + ", ubp = " + str(params[7]))
        plt.xlim([0, max(p_flow_times)/2])
        plt.show()
        plt.hist(p_outflow_times, 250)
        plt.xlim([0, max(p_outflow_times)/2])
        plt.title("Inflow Times, x = " + str(params[5]) + ", ubp = " + str(params[7]))
        plt.show()
        plt.hist(p_inflow_times, 250)
        plt.xlim([0, max(p_outflow_times)/1.25])
        plt.title("Outflow Times, x = " + str(params[5]) + ", ubp = " + str(params[7]))
        plt.show()


    return p_inflow, s_inflow, state_times

def runStateTimes(isAntiport, varToTest):
    run(isAntiport, varToTest, True, False)

def runInflows(isAntiport, varToTest):
    run(isAntiport, varToTest, False, True)



def run(isAntiport, varToTest, graphStateTimes, graphInflows):

    global antiport_defaults
    global symport_defaults
    all_state_times = [[], [], [], [], [], []]
    model_x = []
    if isAntiport:
        model_y = [[], [], [], [], [], []]
    else:
        model_y = [[], [], [], [], [], [], [], []]
    sfl_x = []
    sfl_a = []
    sfl_b = []
    model = open("solutiontext.txt")
    m2 = open("sugar.txt")
    lines = model.readlines()
    lines2 = m2.readlines()
    # for line in lines:
    #     dpoint = line.split('{')[1:]
    #     xval = float(dpoint[0][:-2])
    #     yvals = dpoint[1][:-4].split(", ")
    #     model_x.append(xval)
    #     for i in range(len(yvals)):
    #         model_y[i].append(float(yvals[i]))
    for line in lines2:
        dpoint = line[2:-3].split(", ")
        sfl_x.append(float(dpoint[0]))
        sfl_a.append(float(dpoint[1]))
        sfl_b.append(float(dpoint[2]))
    if isAntiport:
        par_strings = ["u_a", "w_a", "u_b", "w_b", "gamma", "x", "uap", "ubp"]
        pars = antiport_defaults.copy()
    else:
        par_strings = ["u_a", "w_a", "u_b", "w_b", "gamma", "x", "uap", "wap", "ubp", "wbp"]
        pars = symport_defaults.copy()
    try:
        my_test = par_strings.index(varToTest.lower())
    except:
        print("Not a valid parameter to test")
        return
    test_start = pars[my_test]
    low = test_start / 20
    test_vals = [low*x for x in range(1, 100)]
    all_p_inflows = []
    all_s_inflows = []

    for val in test_vals:
        pars[my_test] = val
        data = run_once(isAntiport, pars)
        all_p_inflows.append(data[0])
        all_s_inflows.append(data[1])
        for state in range(len(data[2])):
            all_state_times[state].append(data[2][state])
        print(val)
        print(data[2])
    colors = ["purple", "red", "orange", "yellow", "green", "blue"]
    if (graphStateTimes):
        for st in range(len(all_state_times)):
            if st > 0:
                plt.scatter(test_vals, all_state_times[st], label="State " + str(st), color=colors[st])
            else:
                plt.scatter(test_vals, all_state_times[st], label="State 6", color=colors[st])
            plt.plot(model_x, model_y[st], color=colors[st])
        plt.ylabel("Probability of state")
        plt.title("u_b' = " + str(aubp))
        plt.xlabel(varToTest)
        plt.legend()
        plt.show()
    if (graphInflows):
        plt.plot(test_vals, np.zeros(len(test_vals)), color="0.8", linewidth=3)
        plt.scatter(test_vals, all_p_inflows, label="Simulation: Flow Rate of Compound A (driver)", color="red", s=(rcParams['lines.markersize'] / 3) ** 2)
        plt.scatter(test_vals, all_s_inflows, label="Simulation: Flow Rate of Compound B (driven)", color="blue", s=(rcParams['lines.markersize'] / 3) ** 2)
        plt.plot(sfl_x, sfl_a, label="Model: Flow Rate of Compound A (driver)", color="red")
        plt.plot(sfl_x, sfl_b, label="Model: Flow Rate of Compound B (driven)", color="blue")
        plt.xlabel("$w_B$")
        plt.ylabel("Flow rates of compounds")
        plt.show()

def simple_plot():
    model = open("solutiontext.txt")
    m2 = open("sugar.txt")
    m3 = open("xmin.txt")
    lines = model.readlines()
    lines2 = m2.readlines()
    lines3 = m3.readlines()
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []
    for line in lines:
        dpoint = line[1:-2].split(", ")
        x1.append(float(dpoint[0]))
        y1.append(float(dpoint[1]))
    for line in lines2:
        dpoint = line[1:-2].split(", ")
        x2.append(float(dpoint[0]))
        y2.append(float(dpoint[1]))
    for line in lines3:
        dpoint = line[1:-2].split(", ")
        x3.append(float(dpoint[0]))
        y3.append(float(dpoint[1]))
    plt.plot(x1, y1, linewidth=5)
    plt.plot(x1, np.zeros(len(x1)), color="0.8")
    plt.xlabel("$\\frac{g_B}{g_A}$")
    plt.ylabel("Efficiency")
    plt.title("x = 0.001")
    plt.show()
    plt.plot(x2, np.zeros(len(x2)), color="0.8")

    plt.plot(x2, y2, linewidth=5)
    plt.xlabel("$\\frac{g_B}{g_A}$")
    plt.ylabel("Efficiency")
    plt.title("x = 1")
    plt.show()
    plt.plot(x3, np.zeros(len(x3)), color="0.8")
    plt.plot(x3, y3, linewidth=5)

    plt.xlabel("$\\frac{g_B}{g_A}$")
    plt.ylabel("Efficiency")
    plt.title("x = 1000")
    plt.show()

def bar_plot():
    model = open("solutiontext.txt")
    m2 = open("sugar.txt")
    lines = model.readlines()
    yy1 = lines[0][2:-3].split(", ")
    yy1.append((yy1.pop(0)))
    y1 = [float(y) for y in yy1]
    yy2 = lines[1][2:-3].split(", ")
    yy2.append((yy2.pop(0)))
    y2 = [float(y) for y in yy2]
    x = [1, 2, 3, 4, 5, 6]
    plt.bar(x, y1)
    plt.xlabel("State")
    plt.ylabel("Probability")
    plt.title("Probability of Antiporter Being in Each State \n $x < x_c$")
    plt.show()
    plt.bar(x, y2)
    plt.xlabel("State")
    plt.ylabel("Probability")
    plt.title("Probability of Antiporter Being in Each State \n $x > x_c$")
    plt.show()

def sp2():
    model = open("solutiontext.txt")
    lines = model.readlines()
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    y5 = []
    for line in lines:
        quint = line[2:-3].split(", ")
        y1.append(float(quint[0]))
        y2.append(float(quint[1]))
        y3.append(float(quint[2]))
        y4.append(float(quint[3]))
        y5.append(float(quint[4]))
    plt.plot(y1, y1, "--", color="red", label="$g_A = g_B$", linewidth=5)

    plt.plot(y1, y3, color="blue", label="x = 50", linewidth=5)
    plt.plot(y1, y4, color="green", label="x = 10", linewidth=5)
    plt.plot(y1, y5, color="black", label="x = 1", linewidth=5)
    plt.ylim([1, 20])
    plt.xlim([1, 20])
    plt.legend()
    plt.show()


runInflows(False, "x")