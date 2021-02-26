
# from flask import Blueprint, render_template
# from flask_login import login_required, current_user

from flask import render_template, request, redirect, url_for, abort, session, Blueprint
from server import app
from datetime import datetime
from src.ingredient import Ingredient
import sys
from init import bootstrap_system
<<<<<<< HEAD
import pickle
system = bootstrap_system()
=======
>>>>>>> added staff pages on report and menu update

'''
Website Structure:
- Home page '/'
- #Customer '/customer'
    - Menu pages '/customer/menu'
        - Mains '/customer/mains'
            - Creation '/customer/mains/creation'
        - Sides '/customer/sides'
        - Drinks '/customer/drinks'
        - Sundaes '/customer/sundaes'
    - Review order '/customer/review/<order_id>'
    - Order tracking  '/customer/order/<order_id>'
- #Staff '/staff'
    - Login '/staff/login'
    - Logout '/staff/logout'
    - Order '/staff/order'
    - Inventory '/staff/inventory'
-#Admin '/admin'
    - Homepage (redirects to newmenu)'/admin'
    - Create new menu'/admin/newmenu'
    - Modify menu '/admin/modify'
    - Usage reports '/admin/usage'
'''


'''
page for "page not found"
'''
# @app.route('/404')
# @app.errorhandler(404)
# def page_not_found(e=None):
#     return render_template('404.html'), 404

customer = Blueprint('customer', __name__)
staff = Blueprint('staff', __name__)
admin = Blueprint('admin', __name__)
system = bootstrap_system()
print(system.get_menulist())


@customer.route('/customer', methods=["GET", "POST"])
def home_page():
    print(session)
    # if request.method == 'POST':
    #     if request.form["button"] == "make_new_order":
    order_id = system.make_order()
    session['order_ID'] = order_id
    #         return redirect('/customer/menu/Mains')
    #     elif request.form["button"] == "continue_order":
    #         return redirect('/customer/menu/Mains')
    #     elif request.form["button"] == "search_order":
    #         return redirect(url_for('search_order', order_id=request.form['order_id']))
    #     elif request.form["button"] == "staff":
    #         return redirect(url_for('staff_homepage'))

    return render_template('new_order.html', system=system)


'''
Customer pages:
'''

def check_order_in_session():
    # check whether order_id in the session
    if 'order_ID' not in session:
        return render_template("error.html", error="Sorry, you need to create a new order first.")
    # check whether the order_id is in the system
    if not system.get_order(session['order_ID']):
        return render_template("error.html", error="Sorry, your order ID is no longer valid.")


@customer.route('/customer/menu/<menu_name>', methods=["GET", "POST"])
def display_menu(menu_name):
    check_order_in_session()

    if request.method == 'POST':
        if "add_btn" in request.form.keys():
            item = system.get_item(request.form["add_btn"])
            if menu_name == "Mains":
                 system.add_default_main(session['order_ID'], item)
            else:
                system.add_items_in_orders(session['order_ID'], item)
        elif "mod_btn" in request.form.keys():
            item = system.get_item(request.form["mod_btn"])
            return redirect(url_for("customer.modify_mains", item_name=item.name))

    menu = system.get_menu(menu_name)
    if not menu:

        return redirect(url_for('page_not_found'))

    return render_template('customer_menus.html', menu_name=menu_name, menu=menu.display(), inventory=system.inventory)


@customer.route('/customer/creation/<item_name>', methods=["GET", "POST"])
def modify_mains(item_name):
    check_order_in_session()

    item = system.get_item(item_name)
    print(item)
    print(system.inventory.display_unavailable_ingredients())
    if request.method == 'POST':
        if request.form['button'] == 'submit':
            for name, amount in request.form.items():
                if name == 'button':
                    continue
                if amount:
                    price = system.inventory.get_ingredient(name)._additional_price
                    ingredient = Ingredient(name,int(amount),additional_price=price)
                    if 'Bun' in name:       item.modify_buns(system.inventory,ingredient)
                    elif 'Wrap' in name:    item.modify_wraps(system.inventory,ingredient)
                    elif 'Patty' in name:   item.modify_patties(system.inventory,ingredient)
                    else:                   item.modify_other_ingredients(system.inventory,ingredient)
                if item._errors:
                    return render_template("customer_mains_creation.html", item=item, inventory=system.inventory, error=item._errors)
            system.add_items_in_orders(session['order_ID'], item)
            return redirect(url_for('review_order'))

    return render_template("customer_mains_creation.html", item=item, inventory=system.inventory, error=item._errors)


@customer.route('/customer/review', methods=["GET", "POST"])
def review_order():
    check_order_in_session()

    order = system.get_order(session['order_ID'])
    if request.method == 'POST':
        if request.form["button"] == "checkout":
            order_id = session['order_ID']
            error = system.checkout(order_id)
            if error:
                return render_template("error.html", error=error)
            session.pop('order_ID')
            return render_template("customer_order_result.html", order_id=order_id)
        else:
            system.del_items_in_orders(order.order_id, request.form["button"])

    return render_template('customer_review_order.html', order=order)


@customer.route('/customer/order/<order_id>')
def search_order(order_id):
    return render_template('customer_search_order_result.html', order=system.get_order(int(order_id)))


'''
Staff pages:
'''

@staff.route('/staff')
def staff_homepage():
    return redirect(url_for('staff.staff_order'))


<<<<<<< HEAD
=======

@staff.route('/staff/updatemenu')
def staff_updatemenu():
    return render_template('staff_updatemenu.html')

@staff.route('/staff/report')
def staff_report():
    return render_template('staff_report.html')

@staff.route('/staff/checkmenu')
def staff_checkmenu():
    return render_template('staff_checkmenu.html')


# @staff.route('/staff/login', methods=["GET", "POST"])
# def staff_login():

#     if request.method == 'POST':
#         if request.form['button'] == "login":
#             if system.staff_login(request.form['username'], request.form['password']):
#                 return redirect(url_for('staff_order'))
#             else:
#                 return render_template('staff_login.html', username=request.form['username'], error=True)

#         elif request.form['button'] == "cancel":
#             return redirect(url_for('home_page'))

#     return render_template('staff_login.html', username=None, error=None)


# @staff.route('/staff/logout')
# def staff_logout():
#     system.staff_logout()
#     return redirect(url_for('home_page'))


>>>>>>> added staff pages on report and menu update
@staff.route('/staff/order', methods=["GET", "POST"])
def staff_order():

    if request.method == 'POST':
        print("button")
        order_id = int(request.form['button'])
        system.update_order(order_id)
        system.save_state()

    return render_template('staff_order.html', system=system)


@staff.route('/staff/inventory', methods=["GET", "POST"])
def staff_inventory():

    if request.method == 'POST':
        for name, amount in request.form.items():
            if amount:
                system.inventory.update_stock(name, float(amount))
        system.save_state()

    return render_template('staff_inventory.html', system=system)


'''
Admin pages:
'''


@admin.route('/admin', methods=["GET"])
def admin_home_page():
    return redirect(url_for('admin.admin_newmenu'))

'''--------------------------------------------------------------------------'''


@admin.route('/admin/showMenu', methods=["GET", "POST"])
def admin_showMenu():
    return redirect(url_for('admin.admin_newmenu'))



@admin.route('/admin/newmenu', methods=["GET", "POST"])
def admin_newmenu():

    if request.method == 'POST':
        print(request.form)
        menutype = request.form('menutype')
        item = request.form('item')
        price = abs(request.form('price'))
        # newItem = MenuItem(name=request.form['name'], image=flask.request.files.get('image', ''), price=request.form[
        #                        'price'], availability=request.form['availability'], user_id=admin.user_id)
        # # session.add(newItem)
        # session.commit()
        # flash('New menu %s item has been successfully added' % (newItem.name))
        return redirect(url_for('admin/admin_showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('admin_newmenu.html')

@admin.route('/admin/modify', methods=["GET", "POST"])
def admin_modify():
    if request.method == 'POST':
        print(request.form)
        # for name, amount in request.form.items():
        #     if amount:
        #         system.inventory.update_stock(name, float(amount))
        # system.save_state()

    return render_template('admin_modify.html', system=system)


@admin.route('/admin/modify/<menu_name>', methods=["GET", "POST"])
def modify_menu(menu_name):
    check_order_in_session()

    if request.method == 'POST':
        if "del_btn" in request.form.keys():
            # TODO
            print("delete button")
        elif "upd_btn" in request.form.keys():
            # TOD
            print("update button")

    menu = system.get_menu(menu_name)
    if not menu:

        return redirect(url_for('page_not_found'))

    return render_template('admin_menu_list.html', menu_name=menu_name, menu=menu.display(), inventory=system.inventory)


    # '''
    # editedItem = session.query(menu_name).filter_by(id=menu_id).one()
    # if request.method == 'POST':
    #     if request.form['name']:
    #         editedItem.name = request.form['name']
    #     if request.form['image']:
    #         editedItem.image = flask.request.files.get('image', '')
    #     if request.form['price']:
    #         editedItem.price = request.form['price']
    #     if request.form['availability']:
    #         editedItem.course = request.form['availability']
    #     session.add(editedItem)
    #     session.commit()
    #     flash('Menu item has been changed successfully.')
    #     return redirect(url_for('admin/admin_showMenu'))
    # else:
    #     return render_template('admin_modify.html', menu_id=menu_id, item=editedItem)
    #     '''



@admin.route('/admin/usage', methods=["GET", "POST"])
def admin_usage():

    # TODO FROM BELOW

    '''
    """Run and display various analytics reports."""

    inputFile = open('system_data.dat', 'rb')
    new_dict = pickle.load(inputFile)
    purchases_by_day = new_dict()
    for purchase in purchases:
        purchase_date = purchase.sold_at.date().strftime('%m-%d')
        if purchase_date not in purchases_by_day:
            purchases_by_day[purchase_date] = {'units': 0, 'sales': 0.0}
        purchases_by_day[purchase_date]['units'] += 1
        purchases_by_day[purchase_date]['sales'] += purchase.product.price
    purchase_days = sorted(purchases_by_day.keys())
    units = len(purchases)
    total_sales = sum([p.product.price for p in purchases])


    return render_template('admin_usage.html',
                            products=products,
                            purchase_days=purchase_days,
                            purchases=purchases,
                            purchases_by_day=purchases_by_day,
                            units=units,
                            total_sales=total_sales)

'''
