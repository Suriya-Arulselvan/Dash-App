from SALib.analyze import delta, sobol
import numpy as np
import multiprocessing 
from functools import partial

def DeltaSensitivityAnalysis(dataFrame, independentVarList, dependentVarList):
    indep_min_max = []

    for var in independentVarList:
        min_max = [dataFrame[var].min(), dataFrame[var].max()]
        indep_min_max.append(min_max)

    problem = {
        "num_vars" : len(independentVarList),
        "names" : independentVarList,
        "bounds" : indep_min_max
    }

    dependentVarDataFrame = dataFrame[[c for c in dataFrame.columns if c in dependentVarList]]
    independentVarDataFrame = dataFrame[[c for c in dataFrame.columns if c in independentVarList]]

    independentVarNumpyMatrix = np.asmatrix(independentVarDataFrame.to_numpy())

    pool = multiprocessing.Pool()
    func = partial(DeltaAnalysis, problem, independentVarNumpyMatrix, dependentVarDataFrame)
    ResultList = pool.map(func, dependentVarDataFrame.columns)
    pool.close()
    pool.join()

    return ResultList


def SobolSensitivityAnalysis(dataFrame, independentVarList, dependentVarList):
    indep_min_max = []

    for var in independentVarList:
        min_max = [dataFrame[var].min(), dataFrame[var].max()]
        indep_min_max.append(min_max)

    problem = {
        "num_vars" : len(independentVarList),
        "names" : independentVarList,
        "bounds" : indep_min_max
    }

    dependentVarDataFrame = dataFrame[[c for c in dataFrame.columns if c in dependentVarList]]

    pool = multiprocessing.Pool()
    func = partial(SOBOLAnalysis, problem, dependentVarDataFrame)
    ResultList = pool.map(func, dependentVarDataFrame.columns)
    pool.close()
    pool.join()
    
    return ResultList


def DeltaAnalysis(problem, independentVarNumpyMatrix, dependentVarDataFrame, column):
    analysis = delta.analyze(problem, independentVarNumpyMatrix, dependentVarDataFrame[column].to_numpy())
    return analysis


def SOBOLAnalysis(problem, dependentVarDataFrame, column):
    analysis = sobol.analyze(problem, dependentVarDataFrame[column].to_numpy(), calc_second_order=False)
    return analysis
