
class Knapsack:
    def __init__(self, c: int, w: list[int], v: list[int]):
        self.capacity = c
        self.weights = w
        self.values = v

    # If the programmer tends to get the length, it will return the length of weights/values
    def __len__(self):
        return len(self.weights) if len(self.weights) == len(self.values) else -1

    def rcapacity(self) -> int:
        return self.capacity

    # This is the main knapsack function
    def knapsack(self) -> object:
        W, V = self.weights, self.values
        capacity = self.capacity

        if len(W) == 0 or len(V) == 0 or len(W) != len(V) or capacity < 0:
            raise Exception("Invalid input")

        N = len(W)
        # Initialize a table where individual rows represent items
        # and columns represent the weight of the knapsack
        DP = [[0] * (capacity + 1) for _ in range(N + 1)]  # [[0] * (capacity+1)] * (N+1)

        i = 1
        while i <= N:
            # Get the value and weight of the item
            w = W[i - 1]
            v = V[i - 1]
            sz = 1
            while sz <= capacity:
                # Consider not picking this element
                DP[i][sz] = DP[i - 1][sz]
                # Consider including the current element and
                # see if this would be more profitable
                if sz >= w and DP[i - 1][sz - w] + v > DP[i][sz]:
                    DP[i][sz] = DP[i - 1][sz - w] + v
                sz += 1
            i += 1

        sz = capacity
        itemsSelected = []
        # Using the information inside the table we can backtrack and determine
        # which items were selected during the dynamic programming phase. The idea
        # is that if DP[i][sz] != DP[i-1][sz] then the item was selected
        i = N
        while i > 0:
            if DP[i][sz] != DP[i - 1][sz]:
                itemIndex = i - 1
                itemsSelected.append(itemIndex)
                sz -= W[itemIndex]
            i -= 1

        return {
            "maxVal": DP[N][capacity],
            "selected": itemsSelected[::-1]
        }

    # Function that returns a list of objects with their corresponding weights, values, and frequencies
    #
    def frequencies(self, amount) -> list[object]:
        arr = []
        for i in range(len(self.weights)):
            obj1 = {"index": i, "freq": amount, "value": self.values[i], "weight": self.weights[i]}
            arr.append(obj1)
        return arr

    # main function
    # returns an object
    def get_value(self) -> object:
        loopNum, sumWeight = 0, 0
        sw = sum(self.weights)

        # iterates if capacity - (loopNum * sw) is greater or equal to zero
        while loopNum * sw <= self.capacity:
            sumWeight += sw
            self.capacity -= sw
            loopNum += 1

        # this 2 if statements just double checks if the values are correct
        while self.capacity - sw >= 0:
            loopNum += 1
            sumWeight += sw
            self.capacity -= sw

        if self.capacity - sw >= 0:
            loopNum += 1
            sumWeight += sw
            self.capacity -= sw

        if self.capacity < 0:
            self.capacity += sum(self.weights)
            sumWeight -= sw
            loopNum -= 1

        # print the values before being validated
        print(f"Loop num: {loopNum}")
        print(f"Capacity {self.capacity}")
        print(f"Weight sum: {sum(self.weights)}")

        # gets the maximum value and selected value from the remaining capacity
        val1 = self.knapsack()  # { "maxVal": int, selected: int[] }

        # assigns the proper frequency to the values and weights
        arrVal = self.frequencies(loopNum)  # [{ "index": int, "freq": int,  }]

        print(val1)
        w1 = 0

        # adds the remaining frequencies to the selected items in the knapsack
        for elem in val1["selected"]:
            arrVal[elem]['freq'] += 1
            w1 += self.weights[elem]
            self.capacity -= self.weights[arrVal[elem]['index']]

        return {
            "maxWeight": sumWeight + w1,
            "maxValue": (loopNum * sum(self.values)) + val1["maxVal"],
            "selectedVal": arrVal
        }

    def get_selected(self, arrIdx: list[int]) -> object:
        obj2 = {"weights": [], "values": []}
        for elem in arrIdx:
            obj2["weights"].append(self.weights[elem])
            obj2["values"].append(self.values[elem])
        return obj2


def main():

    v = [500, 100, 250, 250, 300, 350, 100, 150, 250, 200]  # values
    w = [500, 300, 250, 400, 300, 350, 150, 500, 100, 400]  # weights
    c = 8000  # capacity

    # creates an instance of the Knapsack class then calls the get value method
    valC = Knapsack(c, w, v)
    val = valC.get_value()

    # prints the elements of v(values) and w(weights)
    print(f"Values {v}")
    print(f"Weights {w}")

    # true value and weight, variables to check whether the returned values are correct
    tv = 0
    tw = 0

    # prints the values returned by the method call
    for i in range(len(val['selectedVal'])):
        print(f"Index {val['selectedVal'][i]['index']+1} - Frequency {val['selectedVal'][i]['freq']} - "
              f"Value {val['selectedVal'][i]['value']} - Weight {val['selectedVal'][i]['weight']}")

        # get the total sum of values v(values) and w(weights) array
        tv += val['selectedVal'][i]['freq'] * v[i]
        tw += val['selectedVal'][i]['freq'] * w[i]
    # print the input capacity
    print("Input capacity:", c)
    # print whether the returned value and the true v and w is the same
    print("Test case: ", val['maxWeight'] == tw and val['maxValue'] == tv)
    # print the true value and weight
    print(f"True value: {tv} - True weight: {tw}")
    # print the returned value
    print("Remaining capacity: " + str(valC.rcapacity()))

main()
