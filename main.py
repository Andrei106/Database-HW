from datetime import date, datetime

import cx_Oracle
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
with open(app.root_path + '\config.cfg', 'r') as f:
    app.config['ORACLE_URI'] = f.readline()

# conexiunea la baza de date
#con = cx_Oracle.connect("system", "student", "localhost/xe")

# conexiunea la baza de date - facultate
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Andrei\Desktop\Epure_Andrei_Ioan_1309A\instantclient_21_7")
con_tns = cx_Oracle.makedsn('bd-dc.cs.tuiasi.ro', '1539', service_name='orcl')
try:
    con = cx_Oracle.connect('bd096', 'bd096', dsn=con_tns)

except Exception:
    print('Unexpected error')
else:
    print('Conexiune stabilita')

type_category_id = 1

instrument_category_id = 1
instrument_type_id = 1


@app.route('/')
@app.route('/categorie')
def category_fct():
    categories = []
    cur = con.cursor()
    cur.execute('select * from category c  order by c.category_id')
    for result in cur:
        category = {}
        category['id'] = result[0]
        category['nume'] = result[1]
        categories.append(category)

    return render_template('categorie.html', category=categories)


@app.route('/get_category', methods=['POST'])
def get_category_fct():
    id = request.form['id']
    cur = con.cursor()
    cur.execute('select * from category where category_id=' + id)
    c = cur.fetchone()
    nume = c[1]

    cur.close()
    return render_template('/edit_categorie.html', id=id, nume=nume)


@app.route('/add_category', methods=['POST'])
def add_category_fct():
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['nume'] + "'")

        query = 'insert into category values(NULL,' + ', '.join(values) + ')'

        cur.execute(query)

        cur.execute('commit')
        cur.close()
        return redirect('/categorie')


@app.route('/edit_category', methods=['POST'])
def edit_category_fct():
    id = "'" + request.form['id'] + "'"
    nume = "'" + request.form['nume'] + "'"

    cur = con.cursor()
    query = "update category set category_name=%s where category_id=%s" % (nume, id)
    cur.execute(query)
    cur.execute('commit')
    cur.close()
    return redirect('/categorie')


@app.route('/del_category', methods=['POST'])
def del_category_fct():
    cur = con.cursor()
    cur.execute('delete from category where category_id=' + request.form['id'])
    cur.execute('commit')
    cur.close()
    return redirect('/categorie')


@app.route('/tip')
def type_fct():
    categories = []
    cur = con.cursor()
    cur.execute('select * from category c  order by c.category_id')
    for result in cur:
        category = {}
        category['id'] = result[0]
        category['nume'] = result[1]
        categories.append(category)

    return render_template('tip.html', category=categories)


@app.route('/get_type', methods=['POST'])
def get_type_fct():
    id = "'" + request.form['id'] + "'"
    global type_category_id
    type_category_id = id[1:-1]

    types = []
    cur = con.cursor()
    c2 = con.cursor()
    cur.execute('select * from type t where t.category_id=%s ' % id)
    for result in cur:
        type = {}
        type['id'] = result[0]
        type['nume'] = result[1]
        type['category_id'] = result[2]
        c2.execute(
            'select c.category_name from category c,type t where t.category_id=c.category_id and t.category_id=%s ' %
            result[2])
        for result2 in c2:
            type['category_name'] = result2[0]
        types.append(type)

    return render_template('get_tip.html', type=types)


@app.route('/get_type_type', methods=['POST'])
def get_type_type_fct():
    id = request.form['id']
    cur = con.cursor()
    cur.execute('select * from type where type_id=' + id)
    c = cur.fetchone()
    nume = c[1]
    category_id = c[2]
    global type_category_id
    type_category_id = c[2]

    cur.close()
    return render_template('/edit_tip.html', id=id, nume=nume, category_id=category_id)


@app.route('/add_type', methods=['POST'])
def add_type_fct():
    if request.method == 'POST':
        cur = con.cursor()
        global type_category_id
        values = ["'" + request.form['nume'] + "'", "'" + str(type_category_id) + "'"]
        query = 'insert into type values(NULL,' + ', '.join(values) + ')'
        cur.execute(query)
        cur.execute('commit')
        cur.close()
        return redirect('/tip')


@app.route('/edit_type', methods=['POST'])
def edit_type_fct():
    id = "'" + request.form['id'] + "'"
    nume = "'" + request.form['nume'] + "'"

    cur = con.cursor()
    query = "update type set type_name=%s where type_id=%s" % (nume, id)
    cur.execute(query)
    cur.execute('commit')
    cur.close()
    return redirect('/tip')


@app.route('/del_type', methods=['POST'])
def del_type_fct():
    cur = con.cursor()
    cur.execute('delete from type where type_id=' + request.form['id'])
    cur.execute('commit')
    cur.close()
    return redirect('/tip')


@app.route('/producator')
def manufacturer_fct():
    manufacturers = []
    cur = con.cursor()
    cur.execute('select * from manufacturer  order by manufacturer_id')
    for result in cur:
        manufacturer = {}
        manufacturer['id'] = result[0]
        manufacturer['nume'] = result[1]
        manufacturer['tara'] = result[2]
        manufacturers.append(manufacturer)

    return render_template('producator.html', manufacturer=manufacturers)


@app.route('/get_manufacturer', methods=['POST'])
def get_manufacturer_fct():
    id = request.form['id']
    cur = con.cursor()
    cur.execute('select * from manufacturer where manufacturer_id=' + id)
    c = cur.fetchone()
    nume = c[1]
    tara = c[2]

    cur.close()
    return render_template('/edit_producator.html', id=id, nume=nume, tara=tara)


@app.route('/add_manufacturer', methods=['POST'])
def add_manufacturer_fct():
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['nume'] + "'")
        values.append("'" + request.form['tara'] + "'")

        query = 'insert into manufacturer values(NULL,' + ', '.join(values) + ')'

        cur.execute(query)

        cur.execute('commit')
        cur.close()
        return redirect('/producator')


@app.route('/edit_manufacturer', methods=['POST'])
def edit_manufacturer_fct():
    id = "'" + request.form['id'] + "'"
    nume = "'" + request.form['nume'] + "'"
    tara = "'" + request.form['tara'] + "'"

    cur = con.cursor()
    query = "update manufacturer set manufacturer_name=%s ,country =%s where manufacturer_id=%s" % (nume, tara, id)
    cur.execute(query)
    cur.execute('commit')
    cur.close()
    return redirect('/producator')


@app.route('/del_manufacturer', methods=['POST'])
def del_manufacturer_fct():
    cur = con.cursor()
    cur.execute('delete from manufacturer where manufacturer_id=' + request.form['id'])
    cur.execute('commit')
    cur.close()
    return redirect('/producator')


@app.route('/client')
def client_fct():
    clients = []
    cur = con.cursor()
    cur.execute('select * from client  order by client_id')
    for result in cur:
        client = {}
        client['id'] = result[0]
        client['first_name'] = result[1]
        client['last_name'] = result[2]
        client['email'] = result[3]
        client['country'] = result[4]
        client['phone_number'] = result[5]
        client['city'] = result[6]
        clients.append(client)

    return render_template('client.html', client=clients)


@app.route('/get_client', methods=['POST'])
def get_client_fct():
    id = request.form['id']
    cur = con.cursor()
    cur.execute('select * from client where client_id=' + id)
    c = cur.fetchone()
    first_name = c[1]
    last_name = c[2]
    email = c[3]
    country = c[4]
    phone_number = c[5]
    city = c[6]
    cur.close()
    return render_template('/edit_client.html', id=id, first_name=first_name, last_name=last_name, email=email,
                           country=country, phone_number=phone_number, city=city)


@app.route('/add_client', methods=['POST'])
def add_client_fct():
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        values.append("'" + request.form['first_name'] + "'")
        values.append("'" + request.form['last_name'] + "'")
        values.append("'" + request.form['email'] + "'")
        values.append("'" + request.form['country'] + "'")
        values.append("'" + request.form['phone_number'] + "'")
        values.append("'" + request.form['city'] + "'")

        query = 'insert into client values(NULL,' + ', '.join(values) + ')'

        cur.execute(query)

        cur.execute('commit')
        cur.close()
        return redirect('/client')


@app.route('/edit_client', methods=['POST'])
def edit_client_fct():
    id = "'" + request.form['id'] + "'"
    first_name = "'" + request.form['first_name'] + "'"
    last_name = "'" + request.form['last_name'] + "'"
    email = "'" + request.form['email'] + "'"
    country = "'" + request.form['country'] + "'"
    phone_number = "'" + request.form['phone_number'] + "'"
    city = "'" + request.form['city'] + "'"

    cur = con.cursor()
    query = "update client set first_name=%s,last_name=%s,email=%s,country=%s,phone_number=%s,city=%s where " \
            "client_id=%s" % (first_name, last_name, email, country, phone_number, city, id)
    cur.execute(query)
    cur.execute('commit')
    cur.close()
    return redirect('/client')


@app.route('/del_client', methods=['POST'])
def del_client_fct():
    cur = con.cursor()
    cur.execute('delete from client where client_id=' + request.form['id'])
    cur.execute('commit')
    cur.close()
    return redirect('/client')


@app.route('/oferta')
def oferta_fct():
    oferte = []
    cur = con.cursor()
    cur.execute('select * from oferta  order by oferta_id')
    for result in cur:
        oferta = {}
        oferta['id'] = result[0]
        oferta['start_date'] = str(result[1])[:10]
        oferta['end_date'] = str(result[2])[:10]
        oferta['discount'] = result[3]
        oferte.append(oferta)

    return render_template('oferta.html', oferta=oferte)


@app.route('/get_oferta', methods=['POST'])
def get_oferta_fct():
    id = request.form['id']
    cur = con.cursor()
    cur.execute('select * from oferta where oferta_id=' + id)
    c = cur.fetchone()
    start_date = c[1]
    end_date = c[2]
    discount = c[3]

    cur.close()

    return render_template('/edit_oferta.html', id=id, start_date=str(start_date)[:10],
                           end_date=str(end_date)[:10], discount=discount)


@app.route('/add_oferta', methods=['POST'])
def add_oferta_fct():
    if request.method == 'POST':
        cur = con.cursor()
        values = []

        months = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
        date_s = request.form['start_date'].split("-")
        Sdate = date_s[2] + "-" + months[int(date_s[1]) - 1] + "-" + date_s[0]
        date_e = request.form['end_date'].split("-")
        Edate = date_e[2] + "-" + months[int(date_e[1]) - 1] + "-" + date_e[0]

        values.append("'" + Sdate + "'")
        values.append("'" + Edate + "'")
        values.append("'" + request.form['discount'] + "'")

        query = 'insert into oferta values(NULL,' + ', '.join(values) + ')'

        cur.execute(query)

        cur.execute('commit')
        cur.close()
        return redirect('/oferta')


@app.route('/edit_oferta', methods=['POST'])
def edit_oferta_fct():
    months = ('JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC')
    date_s = request.form['start_date'].split("-")
    Sdate = date_s[2] + "-" + str(months[int(date_s[1]) - 1]) + "-" + date_s[0]
    date_e = request.form['end_date'].split("-")
    Edate = date_e[2] + "-" + str(months[int(date_e[1]) - 1]) + "-" + date_e[0]

    id = "'" + request.form['id'] + "'"
    start_date = "'" + Sdate + "'"
    end_date = "'" + Edate + "'"
    discount = "'" + request.form['discount'] + "'"

    cur = con.cursor()
    query = "update oferta set start_date=%s,end_date=%s,discount=%swhere " \
            "oferta_id=%s" % (start_date, end_date, discount, id)
    cur.execute(query)
    cur.execute('commit')
    cur.close()
    return redirect('/oferta')


@app.route('/del_oferta', methods=['POST'])
def del_oferta_fct():
    cur = con.cursor()
    cur.execute('delete from oferta where oferta_id=' + request.form['id'])
    cur.execute('commit')
    cur.close()
    return redirect('/oferta')


@app.route('/instrumente')
def instrumente_fct():
    categories = []
    cur = con.cursor()
    cur.execute('select * from category c  order by c.category_id')
    for result in cur:
        category = {}
        category['id'] = result[0]
        category['nume'] = result[1]
        categories.append(category)

    return render_template('instrument_category.html', category=categories)


@app.route('/get_type_instrumente', methods=['POST'])
def get_type_instrumente_fct():
    types = []
    id = request.form['id']
    global instrument_category_id
    instrument_category_id = id

    cur = con.cursor()
    c2 = con.cursor()
    cur.execute('select * from type where category_id=' + id)
    for result in cur:
        type = {}
        type['id'] = result[0]
        type['nume'] = result[1]
        type['category_id'] = result[2]
        c2.execute(
            'select c.category_name from category c,type t where t.category_id=c.category_id and t.category_id=%s ' %
            result[2])
        for result2 in c2:
            type['category_name'] = result2[0]
        types.append(type)

    cur.close()
    return render_template('/instrumente_type.html', type=types)


@app.route('/get_instrument_instrument', methods=['POST'])
def get_instrument_instrumente_fct():
    instruments = []
    id = request.form['id']
    global instrument_type_id
    instrument_type_id = id

    cur = con.cursor()
    c2 = con.cursor()
    cur.execute('select * from instrument where type_id=' + id)
    for result in cur:
        instrument = {}
        instrument['id'] = result[0]
        instrument['instrument_name'] = result[1]
        instrument['description'] = result[2]
        instrument['price'] = result[3]
        instrument['stock'] = result[4]
        instrument['manufacturer_id'] = result[5]
        c2.execute(
            'select m.manufacturer_name from manufacturer m where m.manufacturer_id =%s ' %
            result[5])
        for result2 in c2:
            instrument['manufacturer_name'] = result2[0]

        instrument['type_id'] = result[6]
        c2.execute(
            'select t.type_name from type t where t.type_id =%s ' %
            result[6])
        for result2 in c2:
            instrument['type_name'] = result2[0]

        if result[7] is None:
            instrument['oferta_id'] = 0
            instrument['oferta_discount'] = 0
            instrument['final_price'] = result[3]
        else:
            instrument['oferta_id'] = result[7]
            c2.execute(
                'select discount from oferta  where oferta_id =%s ' %
                result[7])
            for result2 in c2:
                instrument['oferta_discount'] = result2[0]

            c2.execute('select nvl((i.price-(i.price * ofer.discount/100)),i.price)  from instrument i,oferta ofer'
                       ' where i.instrument_id = %s and '
                       ' ofer.oferta_id = %s' % (instrument['id'], instrument['oferta_id']))
            for result2 in c2:
                instrument['final_price'] = result2[0]

        instruments.append(instrument)

    manufacturers = []
    cur.execute('select * from manufacturer')
    for result in cur:
        manufacturer = {}
        manufacturer['id'] = result[0]
        manufacturer['name'] = result[1]
        manufacturers.append(manufacturer)

    cur.execute('select o.oferta_id ,o.discount from oferta o,instrument i where i.oferta_id=o.oferta_id')
    used_oferte = []
    for result in cur:
        used_oferta = {}
        used_oferta['id'] = result[0]
        used_oferta['discount'] = result[1]
        used_oferte.append(used_oferta)

    # initial cur.execute('select o.oferta_id from oferta o,instrument i where i.oferta_id!=o.oferta_id')
    all_oferte = []
    cur.execute('select * from oferta ')
    for result in cur:
        oferta = {}
        oferta['id'] = result[0]
        oferta['discount'] = result[3]
        all_oferte.append(oferta)

    oferte = []
    oferte.append({'id': None, 'discount': 0})

    for i in all_oferte:
        ok = 1
        for j in used_oferte:
            if i == j:
                ok = 0
        if ok == 1:
            oferte.append(i)

    cur.close()
    return render_template('/instrumente_instrumente.html', instrument=instruments, oferta=oferte,
                           manufacturer=manufacturers)


@app.route('/get_instrument', methods=['POST'])
def get_instrumente_fct():
    id = request.form['id']

    cur = con.cursor()
    cur.execute('select * from instrument where instrument_id=' + id)
    c = cur.fetchone()
    instrument_name = c[1]
    description = c[2]
    price = c[3]
    stock = c[4]
    manufacturer_id = c[5]
    type_id = c[6]
    cur.execute('select category_id from type where type_id=' + str(type_id))
    c1 = cur.fetchone()
    category_id = c1[0]
    if c[7] is not None:
        oferta_id = c[7]
    else:
        oferta_id = 0

    manufacturers = []
    cur.execute('select * from manufacturer')
    for result in cur:
        manufacturer = {}
        manufacturer['id'] = result[0]
        manufacturer['name'] = result[1]
        manufacturers.append(manufacturer)

    cur.execute('select o.oferta_id ,o.discount from oferta o,instrument i where i.oferta_id=o.oferta_id')
    used_oferte = []
    for result in cur:
        used_oferta = {}
        used_oferta['id'] = result[0]
        used_oferta['discount'] = result[1]
        used_oferte.append(used_oferta)

    # initial cur.execute('select o.oferta_id from oferta o,instrument i where i.oferta_id!=o.oferta_id')
    all_oferte = []
    cur.execute('select * from oferta ')
    for result in cur:
        oferta = {}
        oferta['id'] = result[0]
        oferta['discount'] = result[3]
        all_oferte.append(oferta)

    oferte = []
    oferte.append({'id': None, 'discount': 0})
    for i in all_oferte:
        ok = 1
        for j in used_oferte:
            if i == j:
                ok = 0
        if ok == 1:
            oferte.append(i)

    cur.close()
    return render_template('/edit_instrument.html', id=id, instrument_name=instrument_name, description=description,
                           price=price,
                           stock=stock, manufacturer_id=manufacturer_id, type_id=type_id, category_id=category_id,
                           oferta_id=oferta_id, oferta=oferte, manufacturer=manufacturers)


@app.route('/add_instrumente', methods=['POST'])
def add_instrumente_fct():
    if request.method == 'POST':
        global instrument_category_id, instrument_type_id
        cur = con.cursor()
        if request.form['oferta_id'] != 'None':
            values = ["'" + request.form['Nume'] + "'", "'" + request.form['Descriere'] + "'",
                      "'" + request.form['Pret'] + "'", "'" + request.form['Stoc'] + "'",
                      "'" + request.form['manufacturer_id'] + "'", "'" + str(instrument_type_id) + "'",
                      "'" + request.form['oferta_id'] + "'"]
            query = 'insert into instrument values(NULL,' + ', '.join(values) + ')'
        else:
            values = ["'" + request.form['Nume'] + "'", "'" + request.form['Descriere'] + "'",
                      "'" + request.form['Pret'] + "'", "'" + request.form['Stoc'] + "'",
                      "'" + request.form['manufacturer_id'] + "'", "'" + str(instrument_type_id) + "'"]
            query = 'insert into instrument values(NULL,' + ', '.join(values) + ',NULL)'

        cur.execute(query)

        cur.execute('commit')
        cur.close()
        return redirect('/instrumente')


@app.route('/edit_instrument', methods=['POST'])
def edit_instrumente_fct():
    global instrument_category_id, instrument_type_id
    id = "'" + request.form['id'] + "'"
    instrument_name = "'" + request.form['Nume'] + "'"
    description = "'" + request.form['Descriere'] + "'"
    price = "'" + request.form['Pret'] + "'"
    stock = "'" + request.form['Stoc'] + "'"
    manufacturer_id = "'" + request.form['manufacturer_id'] + "'"
    if request.form['oferta_id'] != 'None':
        oferta_id = "'" + request.form['oferta_id'] + "'"
    else:
        oferta_id = 'NULL'

    cur = con.cursor()
    query = "update instrument set instrument_name=%s,description=%s,price=%s,stock=%s,manufacturer_id=%s,type_id=%s " \
            ",oferta_id=%s where " \
            "instrument_id=%s" % (
                instrument_name, description, price, stock, manufacturer_id, instrument_type_id,
                oferta_id, id)
    cur.execute(query)
    cur.execute('commit')
    cur.close()
    return redirect('/instrumente')


@app.route('/del_instrumente', methods=['POST'])
def del_instrumente_fct():
    cur = con.cursor()
    cur.execute('delete from instrument where instrument_id=' + request.form['id'])
    cur.execute('commit')
    cur.close()
    return redirect('/instrumente')


@app.route('/comenzi')
def comenzi_fct():
    orders = []
    orders_i = []
    cur = con.cursor()
    cur.execute('select * from orders ')
    cur2 = con.cursor()
    cur2.execute('select * from order_instrument ')
    for result in cur:
        order = {}
        order['client_id'] = result[0]
        order['id'] = result[1]
        order['status'] = result[2]
        # order['quantity'] = result[3]
        orders.append(order)

    for result in cur:
        order_i = {}
        # order_i['orders_client_id'] = result[0]
        order_i['orders_order_id'] = result[0]
        order_i['instrument_instrument_id'] = result[1]
        #   order_i['instrument_type_id'] = result[3]
        # order_i['instrument_category_id'] = result[4]
        order_i['quantity'] = result[2]
        orders_i.append(order_i)

    clients = []
    cur.execute('select * from client')
    for result in cur:
        client = {}
        client['id'] = result[0]
        client['id_name'] = str(result[0]) + " - " + str(result[2]) + "  " + str(result[1])
        clients.append(client)

    types = []
    cur.execute('select * from type')
    for result in cur:
        type = {}
        type['id'] = result[0]
        types.append(type)

    categories = []
    cur.execute('select * from category')
    for result in cur:
        categorie = {}
        categorie['id'] = result[0]
        categories.append(categorie)

    instruments = []
    cur.execute('select * from instrument')
    for result in cur:
        instrument = {}
        instrument['id'] = result[0]
        instrument['name'] = result[1]
        instruments.append(instrument)

    cur.execute('select c.first_name,c.last_name, i.instrument_name ,ord.status,o.quantity ,o.orders_order_id from '
                'client c, '
                'order_instrument o , '
                'orders ord,instrument i where c.client_id=ord.client_id and  '
                'o.instrument_instrument_id=i.instrument_id and ord.order_id=o.orders_order_id order by c.first_name '
                'asc')
    comenzi = []
    for result in cur:
        comanda = {}
        comanda['first_name'] = result[0]
        comanda['last_name'] = result[1]
        comanda['instrument_name'] = result[2]
        comanda['status'] = result[3]
        comanda['quantity'] = result[4]
        comanda['orders_order_id'] = result[5]
        comenzi.append(comanda)

    return render_template('comenzi.html', comanda=comenzi, order=orders, order_i=orders_i, client=clients, type=types,
                           categorie=categories, instrument=instruments)


@app.route('/add_comenzi', methods=['POST'])
def add_comenzi_fct():
    if request.method == 'POST':
        cur = con.cursor()
        values = []
        cl = "'" + request.form['client_id'] + "'"
        ii = "'" + request.form['instrument_id'] + "'"
        global comenzi_instrument_id
        comenzi_instrument_id = ii
        values.append("'" + request.form['status'] + "'")

        query = 'insert into orders values(' + cl + ',NULL, ' + ', '.join(values) + ')'
        cur.execute(query)
        cur.execute('commit')

        cur.execute('select * from orders ')

        order = None

        for result in cur:
            order = result[1]

        values = []
        order = "'" + str(order) + "'"
        values.append(ii)
        values.append("'" + request.form['cantitate'] + "'")
        query = 'insert into order_instrument values(' + order + ',' + ' , '.join(values) + ')'
        cur.execute(query)

        query = 'update instrument set stock = ' \
                '(select i.stock - ord.quantity from instrument i,order_instrument ord where ' \
                'i.instrument_id=ord.instrument_instrument_id and ' \
                'ord.orders_order_id =  ' + order + ' and ord.instrument_instrument_id = ' + ii+')' \
                                                    'where instrument_id = ' + ii
        cur.execute(query)

        cur.execute('commit work')
        cur.close()
        return redirect('/comenzi')


@app.route('/del_comenzi', methods=['POST'])
def del_comenzi_fct():
    cur = con.cursor()
    cur.execute('select * from order_instrument where orders_order_id = ' + request.form['orders_order_id'])

    comenzi_instrument_id = None

    for result in cur:
        comenzi_instrument_id = result[1]

    query = 'update instrument set stock = ' \
            '(select i.stock + ord.quantity from instrument i,order_instrument ord where ' \
            'i.instrument_id=ord.instrument_instrument_id and ' \
            'ord.orders_order_id =  ' + request.form['orders_order_id'] + ')' \
                                                                          'where instrument_id = ' + str(
        comenzi_instrument_id)
    cur.execute(query)

    cur.execute('delete from order_instrument where orders_order_id=' + request.form['orders_order_id'])
    cur.execute('commit work')
    cur.execute('delete from orders where order_id=' + request.form['orders_order_id'])
    cur.execute('commit work')
    cur.close()
    return redirect('/comenzi')


if __name__ == '__main__':
    app.run(debug=True)
    con.close()
