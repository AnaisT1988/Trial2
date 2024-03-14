test_dict_default = {
    "WorkflowId": 20,
    "Experiment": [
        {
            "Id": 1,
            "Nodes": [
                {"NodeId": 1461.0, "TrialNumber": 0, "Articles": [{"ArticleId": 5}]}
            ],
        }
    ],
}
test_dict_default["Experiment"][0]["Nodes"][0]["Articles"][0]
print(test_dict_default)
