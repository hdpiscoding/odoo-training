import odoo
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.http import request
import datetime
import json
import logging
_logger = logging.getLogger(__name__)

def convert_datetime(d):
  if d:
    return d.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if isinstance(d, datetime.datetime) else d.strftime(DEFAULT_SERVER_DATE_FORMAT)
  else:
    return False

class ZooAPI(odoo.http.Controller):
  @odoo.http.route('/api/v1/zoo/animal/<id>', type='http', auth='none', cors="*", csrf=False)
  def get_animal_by_id(self, id, **kw):
    env = request.env
    id = int(id)
    model = 'zoo.animal'
    record = env[model].sudo().search([('id', '=', id)], limit=1)
    if record:
      res = {
        "name": record.name,
        "dob": convert_datetime(d=record.dob),
        "gender": record.gender,
        "feed_time": convert_datetime(d=record.feed_time),
      }
      _logger.warning(res)
      return request.make_json_response(res, status=200)
    else:
      return request.make_json_response({}, status=200)
  
  @odoo.http.route('/api/v1/zoo/list/animal', type='http', auth='none', cors="*", csrf=False)
  def get_all_animals(self, **kw):
    env = request.env
    model = 'zoo.animal'
    list_animal = env[model].sudo().search([])
    res = []
    if list_animal:
      for animal in list_animal:
        res.append({
          "name": animal.name,
          "dob": convert_datetime(d=animal.dob),
          "gender": animal.gender,
          "feed_time": convert_datetime(d=animal.feed_time),
        })
      _logger.warning(res)
      return request.make_json_response(res, status=200)
    else:
      return request.make_json_response({}, status=200)

  @odoo.http.route('/api/v1/zoo/list/creatures', type='http', auth='user', cors="*", csrf=False)
  def get_creature_list(self, **kw):
    env = request.env
    model = 'zoo.creature'
    list_creature = env[model].sudo().search([])
    res = []
    if list_creature:
      for creature in list_creature:
        res.append({
          "name": creature.name,
          "environment": creature.environment,
          "is_rare": creature.is_rare,
        })
      _logger.warning(res)
      return request.make_json_response(res, status=200)
    else:
      return request.make_json_response({}, status=200)

  @odoo.http.route('/api/html/<val>', type='http', auth='none', cors='*', csrf=False)
  def api_simple_html(self, val, **kw):
      """
      $ curl -X POST -d "a=2" -d "b=3" -d "c=4" localhost:10014/api/html/minh/
      {"result": "{'a': '2', 'b': '3', 'c': '4'} => minh @ 12.00"}
      """
      data = dict(request.params)
      a = int(data.get("a", 1))
      b = int(data.get("b", 2))
      c = int(data.get("c", 3))
      result = a
      for _ in range(abs(b-1)):
          result *= a
      result = result + c
      # Khi type='http' thì "request" sẽ là "odoo.http.HttpRequest" 
      # và ta có thể gọi phương thức "make_response"
      # https://www.odoo.com/documentation/14.0/reference/http.html#request
      return request.make_response(data=json.dumps({"result": "%s => %s @ %.2f" % (str(data), val, result)}), headers=[('Content-Type', 'application/json')])
