import numpy
import json
import requests


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def new_run(base_URL, token, json_file, label):
    with open("data" + label + ".json", "w", encoding="utf-8") as f:
        json.dump(json_file, f, ensure_ascii=False, indent=4, cls=NpEncoder)

    URL = base_URL + "cst-api/v1/production/experimentation/run/create-run"

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    # Opening JSON file
    f = open("data" + label + ".json")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    resp = requests.post(URL, headers=headersAPI, json=data, verify=True)
    print(resp.json())
    j = resp.json()
    runID = j["result"]["runId"]

    return runID


def put_in_queue(base_URL, token, runID):
    URL = (
        base_URL + "/cst-api/v1/production/experimentation/run/queue-run/" + str(runID)
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    resp = requests.post(URL, headers=headersAPI, verify=True)

    return resp.json()


def status_run(base_URL, token, runID):
    URL = (
        base_URL
        + "/cst-api/v1/production/experimentation/run/get-run-state/"
        + str(runID)
    )

    headersAPI = {
        "accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    resp = requests.post(URL, headers=headersAPI, verify=True)
    status = resp["result"]

    return status
