function transform_stock_data(line) {
    var values = line.split(',');
    var obj = new Object();
    obj.ticker = values[0]
    obj.current_price = parseFloat(values[1])
    obj.total_revenue = Number(values[2])
    obj.ebitda = Number(values[3])
    obj.free_cash_flow = Number(values[4])
    obj.profit_margins = parseFloat(values[5])
    obj.revenue_growth = parseFloat(values[6])
    obj.debt_to_equity = parseFloat(values[7])
    obj.total_debt = Number(values[8])
    obj.num_analyst_opinions = parseInt(values[9])
    obj.recommendation_key = values[10]
    obj.time_stamp = values[11];

    var jsonString = JSON.stringify(obj);
    return jsonString;
}
