import json
from collections import defaultdict

from blueprints.forms import *
from decorators import *
from model import *

bp = Blueprint('charts', __name__, url_prefix='/charts')


def get_buildings():
    result_dict = defaultdict(int)
    res = []
    residents = ResidentModel.query.order_by(ResidentModel.id).all()
    for r in residents:
        result_dict[r.building] += 1
    result_dict = dict(result_dict)
    print(result_dict)
    for k, v in result_dict.items():
        res.append({'name': k, 'value': v})
    return jsonify(({'data': res}))


@bp.route('/total_view')
@login_required
def total_view():
    get_buildings()
    return render_template('g_total_view.html')
