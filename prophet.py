from sklearn.tree import DecisionTreeClassifier

from getAPI import make_data

def predict_by_decisiontree(X_train,Y_train,X_test,random_state=100,max_depth=10):
    tree = DecisionTreeClassifier(criterion = "gini",random_state = random_state,max_depth=max_depth, min_samples_leaf=5)

    numofsample = len(X_test[0])
    length = len(X_train)
    X_sample = X_train[length-numofsample : length]
    Y_sample = Y_train[length-numofsample : length]
    X_train = X_train[0 : length-numofsample]
    Y_train = Y_train[0 : length-numofsample]


    tree.fit(X_train,Y_train)

    score = tree.score(X_sample,Y_sample)               #?????????????????????????
    predict = tree.predict(X_test)[0]

    return score,predict



class Prophet:
    def __init__(self,id,random_state=None,max_depth=None):
        self.id = id
        self.random_state =random_state
        self.max_depth = max_depth
        self.predict = None
        self.true = 1
        self.false = 1
        self.percent = 0.5
        self.score = 0.5
    
    def check_resutl(self,result):
        if self.predict == None:
            return
        result = string_to_result(result)
        # if self.predict >10:
        #     predict = "BIG"
        # else:
        #     predict = "SMALL"
        if self.predict == result:  #>>
            self.true+=1
        else:
            self.false+=1
        self.percent = self.true/(self.true+self.false)
    def make_predict(self):
        X_train,Y_train,X_test = make_data(self.id)
        self.score,self.predict = predict_by_decisiontree(X_train,Y_train,X_test,self.random_state,self.max_depth)

def string_to_result(strings):
    if "BIG" in strings:
        return "BIG"
    return "SMALL"

def make_prophet_list():
    prophet_list = []
    for id in range(5,21):
        prophet_list.append(Prophet(id))
    return prophet_list

def check_resutl(result):
    global prophet_list
    for prophet in prophet_list:
        prophet.check_resutl(result)
        # prophet.show()
def make_predict():
    global prophet_list
    big = 0
    small = 0
    for prophet in prophet_list:
        prophet.make_predict()
        print(prophet.predict,prophet.score,prophet.percent)
        if prophet.predict == "BIG":
            big+= prophet.percent* prophet.score
        else:
            small +=prophet.percent* prophet.score

    if big>small:
        return "BIG"
    if small>big:
        return "SMALL"
    return None

    # sampleSpace = [0 for i in range(19)]
    # for prophet in prophet_list:
    #     prophet.make_predict()
    #     # print(prophet.predict, prophet.score,prophet.percent)

    #     sampleSpace[prophet.predict] += prophet.percent* prophet.score #??????????????

    # show_sample_space(sampleSpace)

    # maxresult = max(sampleSpace)

    # for i in range(len(sampleSpace)):
    #     if sampleSpace[i] == maxresult:           #??????????????????????????
    #         if i>10:
    #             return "BIG"
    #         return "SMALL"

def show_percent(big,small):
    big = int(big*50/(big+small))
    small = 50-big
    text = "B"*big + "s"*small
    print(text)
prophet_list = make_prophet_list()

def show_sample_space(sampleSpace):
    for i in range(3,11):
        print(i," : ",round(sampleSpace[i],3), "\t\t\t", i+8," : ", round(sampleSpace[i+8],3))