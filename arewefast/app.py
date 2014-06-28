import json
import os
from collections import defaultdict

from flask import Flask, jsonify, request as req
from flask.ext.sqlalchemy import SQLAlchemy

import requests


if not os.environ.get('APP_SETTINGS'):
    os.environ['APP_SETTINGS'] = 'config.DevelopmentConfig'

if not os.environ.get('DATABASE_URI'):
    os.environ['DATABASE_URI'] = 'postgresql://localhost/arewefast'


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


VALID_DB_FIELDS = ('id', 'url', 'har', 'ref', 'created')
VALID_FIELDS = VALID_DB_FIELDS + ('stats',)
DEFAULT_SORT_ORDERS = {
    'id': 'asc',
    'url': 'asc',
    'ref': 'asc',
    'created': 'desc'
}
RESOURCE_TYPES = [
    'audio',
    'css',
    'cssimage',
    'doc',
    'flash',
    'font',
    'inlinecssimage',
    'inlineimage',
    'js',
    'json',
    'other',
    'total',
    'video'
]


@app.route('/')
def root():
    return 'OK'


def fetch(url, data=None):
    # TODO: Catch request errors.
    print url
    res = requests.get(url, data=data)
    try:
        har = json.loads(res.content)
    except (ValueError, TypeError):
        har = '{}'
        print 'Error parsing JSON: %s' % res.content
    return har


def generate_har(url):
    """Generate a HAR for a given URL by making a call to an external API."""
    # TODO: Do validation checks on the URL.
    # TODO: Pass options: delay, screen size, user-agent override, etc.
    return fetch('http://localhost:3000/demo.har', data={url: url})


def generate_report(report):
    """Generate a breakdown of the sizes and times in the record."""
    # TODO: Consider persisting this instead of generating this on the fly.
    data = defaultdict(dict)

    for type_ in RESOURCE_TYPES:
        data['sizes'][type_] = 0
        data['times'][type_] = 0
        data['totals'][type_] = 0

    try:
        entries = report.har['log']['entries']
    except KeyError:
        return data

    for entry in entries:
        if 'response' not in entry or 'content' not in entry['response']:
            break

        type_ = entry['response']['content'].get('_type')
        if type_ not in RESOURCE_TYPES:
            type_ = 'other'

        size = entry['response']['bodySize']
        time = entry['timings']['wait'] + entry['timings']['receive']

        data['sizes'][type_] += size
        data['times'][type_] += time
        data['totals'][type_] += 1

        data['sizes']['total'] += size
        data['times']['total'] += time
        data['totals']['total'] +=1

    return data


def public_report(report):
    """
    Return a `dict` that is safe to be returned in the JSON response.

    A comma-delimited list of `fields` in the querystring can be specified,
    which will cause only those fields to be returned.
    """
    # Accepted values: ?field=<valid-field>
    # Accepted values: ?fields=<valid-field>,<valid-field>
    # Ignored values:  ?field=<invalid-field>
    # Ignored values:  ?fields=<invalid-field>
    fields_to_include = VALID_FIELDS
    for arg in ('field', 'fields'):
        if arg in req.args:
            fields_to_include = [x.strip() for x in req.args[arg].split(',')
                                 if x in VALID_FIELDS]
    fields_to_include = fields_to_include or VALID_FIELDS

    data = dict((field, getattr(report, field))
                for field in fields_to_include if field in VALID_DB_FIELDS)
    if 'stats' in fields_to_include:
        data['stats'] = generate_report(report)
    return data


def get_unique_values(field):
    """
    Return a response containing the unique values for a particular field.
    """
    from models import Report
    query = db.session.query(getattr(Report, field).distinct()).all()
    items = [x[0] for x in query if x[0]]
    return jsonify(total_count=len(items), items=items)


@app.route('/api/v1/urls')
def get_urls():
    """Return a unique list of URLs from all the records."""
    return get_unique_values('url')


@app.route('/api/v1/reports', methods=['GET'])
def get_reports():
    """
    Return a list of objects of all reports.

    Results can be filtered by `id`, `url`, `ref`.
    A comma-delimited list of `fields` can be specified,
    which will return only those fields.
    If `sort` is specified, results will be sorted by that field.
    If `order` is specified, results can be sorted by `desc` or `asc` orders.

    TODO: Cache these responses to static JSON files.
    """
    from models import Report

    filters = {}
    # TODO: Allow filtering by `created` timestamp.
    for field in ('id', 'url', 'ref'):
        if field in req.args:
            filters[field] = req.args.get(field)

    query = Report.query.filter_by(**filters).order_by()

    # Default sort is `created` by `desc`.
    sort_field = 'created'
    sort_order = DEFAULT_SORT_ORDERS[sort_field]

    # If the user-supplied `sort` is a valid sort option, sort by that.
    if req.args.get('sort') in DEFAULT_SORT_ORDERS:
        sort_field = req.args['sort']

        # If the user-supplied `order` is a valid sort order, sort by that.
        # Otherwise, sort by that field's default sort order.
        if req.args.get('order') in ('asc', 'desc'):
            sort_order = req.args.get('order')
        else:
            sort_order = DEFAULT_SORT_ORDERS[sort_field]

    # Example: `query.order_by(Report.created.desc())`
    query = query.order_by(
        getattr(getattr(Report, sort_field), sort_order)()
    )

    items = [public_report(report) for report in query.all()]
    return jsonify(total_count=len(items), items=items)


@app.route('/api/v1/report/<id>', methods=['GET'])
def get_report(id):
    """Return a given report."""
    from models import Report
    report = Report.query.filter_by(id=id).first_or_404()
    return jsonify(public_report(report))


@app.route('/api/v1/report', methods=['POST', 'PUT'])
def save_report():
    """Fetch a HAR and save the report."""
    from models import Report

    # TODO: Add a delay (with a simple task queue).
    # TODO: Add `payfload` for GitHub Webhooks.

    url = req.form.get('url', req.args.get('url'))
    ref = req.form.get('ref', req.args.get('ref'))
    har = req.form.get('har', req.args.get('har'))

    if har:
        try:
            # If a HAR was supplied as JSON, then just use that.
            # TODO: Add HAR validation.
            har = json.loads(har)
        except ValueError:
            # If a HAR was supplied as a URL, then fetch it.
            # TODO: Add HAR validation.
            har = fetch(har)
    else:
        # If a HAR was not supplied, then generate a HAR for the given URL.
        har = generate_har(url)

    db.session.add(Report(url=url, har=har, ref=ref))
    db.session.commit()

    return jsonify(success=True)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
