import odoo
from odoo.http import request, Response
import json

import logging
_logger = logging.getLogger(__name__)

class FooAPI(odoo.http.Controller):
    @odoo.http.route('/api/foo/<val>', type='json', auth='none', cors='*', csrf=False)
    def api_foo(self, val, **kw):
        """
        $ curl -H "Content-Type: application/json" -X POST --data '{"params": {"a": 2, "b": 3, "c": 4}}' localhost:10014/api/foo/calc/
        {"jsonrpc": "2.0", "id": null, "result": {"val": "calc", "result": 12, "data": "{'a': 2, 'b': 3, 'c': 4}", "request_json": "{'params': {'a': 2, 'b': 3, 'c': 4}}", "request_param": "{'a': 2, 'b': 3, 'c': 4}"}}
        """
        request_httprequest_args = request.httprequest.args.to_dict()
        request_params = request.params
        
        # our custom logic
        data = request_params if request_params else request_httprequest_args
        a = data.get("a", 1)
        b = data.get("b", 2)
        c = data.get("c", 3)
        result = a
        for _ in range(abs(b-1)):
            result *= a
        result = result + c
        return {
            "val": val,
            "result": result,
            "data": str(data),
            "request_httprequest_args": str(request_httprequest_args),
            "request_params": str(request_params),
        }