import random
import asyncio
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Antiport states
from matplotlib import rcParams

O_IN = 6
P_IN = 1
P_OUT = 2
O_OUT = 3
S_OUT = 4
S_IN = 5

# Symport States
IN = 0
A_IN = 1
B_IN = 2
AB_IN = 3
AB_OUT = 4
A_OUT = 5
B_OUT = 6
OUT = 7

# Antiport individual rates
au_a = 1000
aw_a = 100
au_b = 900
aw_b = 1000
aGAMMA = 1
aX = 2
auap = 100
aubp = 500

antiport_defaults = [au_a, aw_a, au_b, aw_b, aGAMMA, aX, auap, aubp]

# Symport individual rates
su_a = 1000
sw_a = 100
su_b = 1000
sw_b = 100
sGAMMA = 10
sX = 5
suap = 100
swap = 1000
subp = 100
swbp = 1000

symport_defaults = [su_a, sw_a, su_b, sw_b, sGAMMA, sX, suap, swap, subp, swbp]


TOTAL_TIME = 1500


P_FLOW_INCREMENT = 1
S_FLOW_INCREMENT = 1






# times = []
# p_inflows = []
# s_inflows = []
# state_times_antiport = [0, 0, 0, 0, 0, 0]
# state_times_symport = [0, 0, 0, 0, 0, 0, 0, 0]
# cur_row = -1




def run_once(isAntiport, params):
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
    if isAntiport:
        ubp = params[7]
        state = P_OUT
        state_times = [0, 0, 0, 0, 0, 0]

        rates = [[0, u_a, 0, GAMMA, 0, u_b],
                 [w_a, 0, GAMMA * X, 0, 0, 0],
                 [0, GAMMA * X, 0, w_a, 0, 0],
                 [GAMMA, 0, uap, 0, ubp, 0],
                 [0, 0, 0, w_b, 0, GAMMA * X],
                 [w_b, 0, 0, 0, GAMMA * X, 0]]
    else:
        wap = params[7]
        ubp = params[8]
        wbp = params[9]
        rates = [[0, u_a, u_b, 0, 0, 0, 0, GAMMA / X],
                 [w_a, 0, 0, u_b, 0, GAMMA, 0, 0],
                 [w_b, 0, 0, u_a, 0, 0, GAMMA, 0],
                 [0, w_b, w_a, 0, GAMMA * X, 0, 0, 0],
                 [0, 0, 0, GAMMA / X, 0, wbp, wap, 0],
                 [0, GAMMA, 0, 0, ubp, 0, 0, wap],
                 [0, 0, GAMMA, 0, uap, 0, 0, wbp],
                 [GAMMA * X, 0, 0, 0, 0, uap, ubp, 0]]
        state = IN
        state_times = [0, 0, 0, 0, 0, 0, 0, 0]
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
        else:
            if prev_state == AB_IN and state == AB_OUT:
                p_inflow -= P_FLOW_INCREMENT / TOTAL_TIME
                s_inflow -= S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == AB_OUT and state == AB_IN:
                p_inflow += P_FLOW_INCREMENT / TOTAL_TIME
                s_inflow += S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == B_IN and state == B_OUT:
                s_inflow -= S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == B_OUT and state == B_IN:
                s_inflow += S_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == A_IN and state == A_OUT:
                p_inflow -= P_FLOW_INCREMENT / TOTAL_TIME
            elif prev_state == A_OUT and state == A_IN:
                p_inflow += P_FLOW_INCREMENT / TOTAL_TIME
        # times.append(time)
    # p_inflows.append(p_inflow)
    # s_inflows.append(s_inflow)
    # a = sns.heatmap(s_inflows, xticklabels=x_vals, yticklabels=w_s_vals)
    # plt.plot(x_vals, p_inflows, label="Flow rate of Phosphate")
    # plt.plot(x_vals, s_inflows, label="Flow rate of Sugar")
    # plt.legend()
    # plt.show()


    # z = np.polyfit(np.array(x_vals), np.array(s_inflows), 1)
    # print(z)

    return -1 * p_inflow, s_inflow, state_times

def runStateTimes(isAntiport, varToTest):
    run(isAntiport, varToTest, True, False)

def runInflows(isAntiport, varToTest):
    run(isAntiport, varToTest, False, True)


def run(isAntiport, varToTest, graphStateTimes, graphInflows):

    global antiport_defaults
    global symport_defaults
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
    for line in lines:
        dpoint = line.split('{')[1:]
        xval = float(dpoint[0][:-2])
        yvals = dpoint[1][:-4].split(", ")
        model_x.append(xval)
        for i in range(len(yvals)):
            model_y[i].append(float(yvals[i]))
    for line in lines2:
        dpoint = line[2:-3].split(", ")
        sfl_x.append(float(dpoint[0]))
        sfl_a.append(float(dpoint[1]))
        sfl_b.append(float(dpoint[2]))
    if isAntiport:
        par_strings = ["u_a", "w_a", "u_b", "w_b", "gamma", "x", "uap", "ubp"]
        pars = antiport_defaults.copy()
        all_state_times = [[], [], [], [], [], []]
    else:
        par_strings = ["u_a", "w_a", "u_b", "w_b", "gamma", "x", "uap", "wap", "ubp", "wbp"]
        pars = symport_defaults.copy()
        all_state_times = [[], [], [], [], [], [], [], []]
    try:
        my_test = par_strings.index(varToTest.lower())
    except:
        print("Not a valid parameter to test")
        return
    test_start = pars[my_test]
    low = test_start / 25
    test_vals = [low*x for x in range(1, 76)]
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
                plt.scatter(test_vals, all_state_times[st], s=(rcParams['lines.markersize'] / 3) ** 2, label="State " + str(st), color=colors[st])
            else:
                plt.scatter(test_vals, all_state_times[st], s=(rcParams['lines.markersize'] / 3) ** 2, label="State 6", color=colors[st])
            plt.plot(model_x, model_y[st], color=colors[st])
        plt.ylabel("Probability of state")
        plt.title("u_b' = " + str(aubp))
        plt.xlabel(varToTest)
        plt.legend()
        plt.show()
    if (graphInflows):
        plt.scatter(test_vals, all_p_inflows, label="Simulation: Flow Rate of Compound A (driver)", color="red", s=(rcParams['lines.markersize'] / 3) ** 2)
        plt.scatter(test_vals, all_s_inflows, label="Simulation: Flow Rate of Compound B (driven)", color="blue", s=(rcParams['lines.markersize'] / 3) ** 2)
        plt.plot(sfl_x, sfl_a, label="Model: Flow Rate of Compound A (driver)", color="red")
        plt.plot(sfl_x, sfl_b, label="Model: Flow Rate of Compound B (driven)", color="blue")
        plt.xlabel(varToTest)
        plt.ylabel("Flow rates of compounds")
        plt.title("u_b' = " + str(aubp))
        plt.legend()
        plt.show()

run(True, "x", True, True)

