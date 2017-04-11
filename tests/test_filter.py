from opv_api_client.filter import Filter, treat_query

def test_filter():
    f1 = Filter("test") == 1
    f2 = Filter().name("test").op("eq").val(1)

    assert f1.get() == f2.get()
    assert f1.get() == {"name": "test", "op": "eq", "val": "1"}

def test_treat_query():
    q = [Filter("test") == -1,
         Filter("T2").op("in").val(5)]

    assert treat_query(q) == [{"name": "test", "op": "eq", "val": "-1"},
                              {"name": "T2", "op": "in", "val": "5"}]
