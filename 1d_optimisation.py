#!/usr/bin/env python3
import time
import argparse
import json
import copy
import pickle
import os
import shutil
import numpy as np
from skopt.space.space import Integer, Space, Real
from sklearn.ensemble import GradientBoostingRegressor
from skopt import Optimizer
from skopt.learning import GaussianProcessRegressor, RandomForestRegressor, GradientBoostingQuantileRegressor

from commons import FCN

from opt_config import (RUN, RANDOM_STARTS, MIN, METADATA_TEMPLATE)
from run_kub import run_batch

POINTS_IN_BATCH = 10
SLEEP_TIME = 60

DEFAULT_POINT = [70.0, 170.0, 208.0, 207.0, 281.0, 248.0, 305.0, 242.0, 
40.0, 40.0, 150.0, 150.0, 2.0, 2.0, 
80.0, 80.0, 150.0, 150.0, 2.0, 2.0,
72.0, 51.0, 29.0, 46.0, 10.0, 7.0, 
54.0, 38.0, 46.0, 192.0, 14.0, 9.0,
10.0, 31.0, 35.0, 31.0, 51.0, 11.0, 
40.0, 32.0, 54.0, 24.0, 8.0, 8.0,
22.0, 32.0, 209.0, 35.0, 8.0, 13.0, 
33.0, 77.0, 85.0, 241.0, 9.0, 26.0]

one_d_index = 38
def StripFixedParams(point):
    #removes absober data from the point
    stripped_point = [point[one_d_index]]
    return stripped_point

def CreateSpace(nMagnets=8):
    
    dimensions = [Integer(3, 100)]
    return Space(dimensions)

def ParseParams(params_string):
    return [float(x) for x in params_string.strip('[]').split(',')]

def AddFixedParams(point):
    point_out = copy.deepcopy(DEFAULT_POINT)
    point_out[one_d_index] = point[0]
    return point_out

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def StripFixedParams_multipoint(points):
    return [StripFixedParams(p) for p in points]

def ExtractParams(metadata):
    params = json.loads(metadata)['user']['params']
    return ParseParams(params)

def get_result(jobs):
    results = []
    weights = np.array([])
    for i in range(len(jobs['jobs'])):
        with open(os.path.join(jobs['path'], str(i), 'optimise_input.json')) as result_file:
          result = json.load(result_file)
          rWeights = np.array(result['kinematics'])
          weights = np.concatenate((weights,rWeights))
          results.append(result)
          print('result is: ', jobs['path'])
    # Only one job per machine calculates the weight and the length
    # -> take first we find
    weight = float(results[0]['w'])
    if weight < 3e6:
        muons_w = np.sum(weights)
    else:
        muons_w =  0
    return weight, 0, muons_w

def get_result_old(jobs):
    results = []
    weights = []
    #print(jobs)
    for i in range(len(jobs['jobs'])):
        with open(os.path.join(jobs['path'], str(i), 'optimise_input.json')) as result_file:
          result = json.load(result_file)
          rWeights = [k[7] for k in result['kinematics']]
          weights = weights + rWeights
          results.append(result)
          print('result is: ', jobs['path'])
    # Only one job per machine calculates the weight and the length
    # -> take first we find
    weight = float(results[0]['w'])
    if weight < 3e6:
        muons_w = sum(np.array(weights, dtype=float))
    else:
        muons_w =  0
    return weight, 0, muons_w


def ProcessPoint(jobs):
    print("process Point: ", jobs)
    try:
        weight, _, muons_w = get_result(jobs)
        #print('obtained weights: ', weight, length, muons_w)
        y = FCN(weight, muons_w, 0)
        #print('Y: ', y)
        X = ExtractParams(jobs['metadata'])
        # print('X: ', X)
        # print(X, y)
        return X, y
    except Exception as e:
        print(e)


def ProcessJobs(jobs, tag, space):
    print('[{}] Processing jobs...'.format(time.time()))
    results = [ProcessPoint(point) for point in jobs]
    print(f'Got results {results}')
    results = [result for result in results if result]
    results = [result for result in results if space.__contains__(StripFixedParams(result[0]))]

    return zip(*results) if results else ([], [])


def CreateMetaData(point, tag):
    metadata = copy.deepcopy(METADATA_TEMPLATE)
    metadata['user'].update([
        ('tag', tag),
        ('params', str(point)),
    ])
    return json.dumps(metadata)

def SubmitKubJobs(point, tag):
    return run_batch(CreateMetaData(point, tag))

def WaitCompleteness(mpoints):
    uncompleted_jobs = mpoints
    work_time = 0
    restart_counts = 0
    while True:
        time.sleep(SLEEP_TIME)
        print(uncompleted_jobs)
        uncompleted_jobs = [any([job.is_alive() for job in jobs['jobs']]) for jobs in mpoints]

        if not any(uncompleted_jobs):
            return mpoints

        print('[{}] Waiting...'.format(time.time()))
        work_time += 60

        if work_time > 60 * 30 * 1:
            restart_counts+=1
            if restart_counts>=3:
                print("Too many restarts")
                raise SystemExit(1)
            print("Job failed!")
            #raise SystemExit(1)
            for jobs in mpoints:
                if any([job.is_alive() for job in jobs['jobs']]):
                    jobs = run_batch(jobs['metadata'])
            #for job in [[for job in jobs['jobs']] for jobs in mpoints]]:
            #    job = run_batch(job['metadata'])
            work_time = 0

def CalculatePoints(points, tag, cache, space):
    tags = {json.dumps(points[i], cls=NpEncoder):str(tag)+'-'+str(i) for i in range(len(points))}
    print(points)
    shield_jobs = [
        SubmitKubJobs(point, tags[json.dumps(point, cls=NpEncoder)])
        for point in points if json.dumps(point, cls=NpEncoder) not in cache.keys()
    ]
    print("submitted: \n", points)

    if shield_jobs:
        shield_jobs = WaitCompleteness(shield_jobs)
        X_new, y_new = ProcessJobs(shield_jobs, tag, space)
        return X_new, y_new
    else:
        print("Where are my mf jobs?")
        return 0

def load_points_from_dir(db_name='db.pkl'):
    with open (db_name, 'rb') as f:
        return pickle.load(f)

def CreateOptimizer(clf_type, space, random_state=None):
    if clf_type == 'rf':
        clf = Optimizer(
            space,
            RandomForestRegressor(n_estimators=500, max_depth=7, n_jobs=-1),
            random_state=random_state)
    elif clf_type == 'gb':
        clf = Optimizer(
            space,
            GradientBoostingQuantileRegressor(
                base_estimator=GradientBoostingRegressor(
                    n_estimators=100, max_depth=4, loss='quantile')),
            random_state=random_state)
    elif clf_type == 'gp':
        clf = Optimizer(
            space,
            GaussianProcessRegressor(
                alpha=1e-7, normalize_y=True, noise='gaussian'),
            random_state=random_state)
    else:
        clf = Optimizer(
            space, base_estimator='dummy', random_state=random_state)

    return clf

def main():
    parser = argparse.ArgumentParser(description='Start optimizer.')
    parser.add_argument('--opt', help='Write an optimizer.', default='gp')
    parser.add_argument('--db', help='Data base file', default='db.pkl')
    parser.add_argument('--state', help='Random state of Optimizer', default=None)
    parser.add_argument('--olddb', help='use existing db', action='store_true')

    args = parser.parse_args()
 
    tag = 0#args.tag

    space = CreateSpace()
    clf = CreateOptimizer(args.opt, space, random_state=int(args.state) if args.state else None)
    print(clf)
    if args.olddb:
        cache = load_points_from_dir(args.db)
    else:
        cache = {}

    tag = len(cache.keys())

#Load calculated points from DB
    if len(cache.keys())>0:
        print('Received previous points ', len(cache.keys()))
        try:
            for key in cache.keys():
                loc_x = json.loads(key)
                loc_y = cache[key]
                if space.__contains__(StripFixedParams(loc_x)):
                    print(loc_x, loc_y)
                    clf.tell(StripFixedParams(loc_x), loc_y)
        except ValueError:
            print('None of the previous points are contained in the space.')

#calculate the first point if DB is empty:
    if len(cache.keys())==0:
        X_1, y_1 = CalculatePoints([DEFAULT_POINT], tag, cache, space)
        print("default start point scorring: \n", X_1, y_1)
        cache[json.dumps(X_1[0], cls=NpEncoder)] = y_1[0]
        clf.tell(StripFixedParams(X_1[0]), y_1[0])

        with open(args.db, 'wb') as db:
                 pickle.dump(cache, db, pickle.HIGHEST_PROTOCOL)

    while not (cache and len(cache.keys()) >  RANDOM_STARTS):
        print("start points...")
        tag = tag + 1
        points = [AddFixedParams(p) for p in space.rvs(n_samples=POINTS_IN_BATCH)]
        # points = [transform_forward(p) for p in points]
        # print(points)
        X_new, y_new = CalculatePoints(points, tag, cache, space)
        print('Received new points ', X_new, y_new)
        if X_new and y_new:
            for x, loss in zip(X_new, y_new):
                cache[json.dumps(x,cls=NpEncoder)] = loss
            # X_new = [transform_backward(point) for point in X_new]
            shutil.copy2(args.db, 'old_db.pkl')
            with open(args.db, 'wb') as db:
                 pickle.dump(cache, db, pickle.HIGHEST_PROTOCOL) 
            clf.tell([p for p in StripFixedParams_multipoint(X_new)], y_new)

    while True:
        tag = tag+1
        print("Main cycle, tag is ", tag)
        points = [AddFixedParams(p) for p in clf.ask(n_points=POINTS_IN_BATCH, strategy='cl_mean')]
        repeat_mask = [json.dumps(point, cls=NpEncoder) in cache.keys() for point in points]
        if any(repeat_mask):
            print("Repeating point")
        points = [points[i] for i in range(len(points)) if not repeat_mask[i]]

        if len(points)==0:
            continue
        print("new points to calculate...")
        X_new, y_new = CalculatePoints(
            points, tag, cache, space)

        print('Received new points ', X_new, y_new)
        if X_new and y_new:
                        for x, loss in zip(X_new, y_new):
                            cache[json.dumps(x,cls=NpEncoder)] = loss
                        shutil.copy2(args.db, 'old_db.pkl')
                        with open(args.db, 'wb') as db:
                            pickle.dump(cache, db, pickle.HIGHEST_PROTOCOL)

        result = clf.tell(StripFixedParams_multipoint(X_new), y_new)

        with open('optimiser.pkl', 'wb') as f:
            pickle.dump(clf, f)

        with open('result.pkl', 'wb') as f:
            pickle.dump(result, f)


if __name__ == '__main__':
    main()
