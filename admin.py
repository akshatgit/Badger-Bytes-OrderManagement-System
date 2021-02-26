from flask import render_template, request, redirect, url_for, abort, session, Blueprint
from server import app
from datetime import datetime
from src.ingredient import Ingredient
import sys
from init import bootstrap_system 

'/admin'
'/admin/newmenu'
'/admin/modify'
'/admin/usage'

'''
Admin pages:
'''
admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_homepage():
    if system.is_authenticated:
        return redirect(url_for('admin_base'))
    else:
        return redirect(url_for('admin_login'))
# Admin: Logging into website


# Admin: create a new menu item
@app.route('admin/newMenu', methods=['GET', 'POST'])
def admin_new_item():
    if not system.is_authenticated:
        return redirect(url_for('staff_login')) 
    # if login_session['user_id'] != system.user_id:
        # return "<script>function myFunction() {alert('You are not authorized to add menu items to this restaurant. Please create your own restaurant in order to add items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], image=flask.request.files.get('image', ''), price=request.form[
                               'price'], availability=request.form['availability'], user_id=admin.user_id)
        session.add(newItem)
        session.commit()
        flash('New menu %s item has been successfully added' % (newItem.name))
        return redirect(url_for('admin/showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('admin_new_item.html')
# Admin: Modify an existing menu item
@admin.route('/admin/modify', methods=["GET", "POST"])
def admin_modify_item(menu_id):
    if not system.is_authenticated:
        return redirect(url_for('staff_login')) 
    editedItem = session.query(menu_name).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['image']:
            editedItem.image = flask.request.files.get('image', '')
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['availability']:
            editedItem.course = request.form['availability']
        session.add(editedItem)
        session.commit()
        flash('Menu item has been changed successfully.')
        return redirect(url_for('admin/showMenu'))
    else:
        return render_template('admin_modify_item.html', menu_id=menu_id, item=editedItem)
# Admin: Print usage reports of website activity and purchases
@bull.route('admin/reports')
@login_required
def admin_usage_reports():
    """Run and display various analytics reports."""
    products = Product.query.all()
    purchases = Purchase.query.all()
    purchases_by_day = dict()
    for purchase in purchases:
        purchase_date = purchase.sold_at.date().strftime('%m-%d')
        if purchase_date not in purchases_by_day:
            purchases_by_day[purchase_date] = {'units': 0, 'sales': 0.0}
        purchases_by_day[purchase_date]['units'] += 1
        purchases_by_day[purchase_date]['sales'] += purchase.product.price
    purchase_days = sorted(purchases_by_day.keys())
    units = len(purchases)
    total_sales = sum([p.product.price for p in purchases])

    return render_template(
        'admin_usage_reports.html',
        products=products,
        purchase_days=purchase_days,
        purchases=purchases,
        purchases_by_day=purchases_by_day,
        units=units,
        total_sales=total_sales)