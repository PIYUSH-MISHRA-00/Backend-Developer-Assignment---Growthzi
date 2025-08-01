from flask import Blueprint, request, jsonify

pricing_bp = Blueprint('pricing', __name__)

CURRENCY_RATES = {
    "US": {"currency": "USD", "rate": 1},
    "IN": {"currency": "INR", "rate": 83},
    "FR": {"currency": "EUR", "rate": 0.91}
}

BASE_PRICE_USD = 100

@pricing_bp.route('/price', methods=['GET'])
def get_price():
    country = request.args.get('country', 'US').upper()
    if country not in CURRENCY_RATES:
        return jsonify({"error": "Unsupported country code"}), 400

    currency_info = CURRENCY_RATES[country]
    converted_price = BASE_PRICE_USD * currency_info['rate']

    return jsonify({
        "currency": currency_info['currency'],
        "price": converted_price
    }), 200
