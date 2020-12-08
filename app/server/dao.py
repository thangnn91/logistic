from app.vndb import DBHelper
from app.model import user_model
from app.server.helper import get_user_role
import pymysql.cursors
import time
from datetime import datetime
__author__ = 'oneconduck'


class DatabaseProcess(object):

    def __init__(self, _db_conf):
        self._db_conf = _db_conf
        
    def login(self, user_name, password):
        sql = 'SELECT id, type, status FROM dbo_user WHERE email=%s AND password=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql, [user_name, password])
        if len(result):
            if result[0]["status"] != 1:
                return -104
            role = get_user_role(result[0]["type"])  
            user_object = user_model.User(str(result[0]["id"]), user_name, role)
            return user_object
        return -105
    
    def register(self, user_name, password, type=0, mobile=""):
        sql = 'SELECT 1 FROM dbo_user WHERE email=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.get_values(sql, [user_name])
        if len(result):  
            return -100;
        
        sql = 'insert into dbo_user(email, password, status, type, mobile) values (%s,%s,%s,%s,%s)'
        with DBHelper(**self._db_conf) as db:
            result = db.insert_batch(sql, [[user_name, password, 1, type, mobile]])           
        return result

    def get_user_info(self, id):
        sql = 'SELECT id,email,fullname,address,mobile, balance from dbo_user WHERE id=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql, [id])
        if len(result):
            return result[0]
        return None
    
    def get_user_info_by_email(self, email):
        sql = 'SELECT id, email, fullname, address, mobile, status, balance from dbo_user WHERE email=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql, [email])
        if len(result):
            return result[0]
        return None
    
    def update_user_info(self, kwargs):
        sql = 'UPDATE dbo_user SET fullname=%s, address=%s, mobile=%s WHERE id=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.update_batch(sql, [[kwargs.fullname, kwargs.address, kwargs.mobile, kwargs.id]])
        return result
    
    def user_change_pass(self, kwargs):
        # check old pass
        sql = 'SELECT 1 FROM dbo_user WHERE password=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.get_values(sql, [kwargs.old_pass])
        if not len(result):  
            return -101;
        
        sql = 'UPDATE dbo_user SET password=%s WHERE id=%s'
        with DBHelper(**self._db_conf) as db:
            result = db.update_batch(sql, [[kwargs.new_pass, kwargs.id]])
        return result  
    
    def admin_insert_update_fee(self, kwargs):
        is_update = getattr(kwargs, 'is_update', None)
        if is_update is not None:
            sql1 = 'DELETE FROM dbo_fee_config WHERE type = %s';
            sql2 = 'INSERT INTO dbo_fee_config(from_value, to_value, fee, type) VALUES (%s,%s,%s,%s)'
            param1 = [kwargs.type]
            array_param = [];
            for item in kwargs.data:
                item.insert(len(item), kwargs.type)
                array_param.append(item)
            
            item1 = type('Dummy', (object,), { "is_many": False,
                                           "param": param1, "query": sql1})
            item2 = type('Dummy', (object,), { "is_many": True,
                                           "param": array_param, "query": sql2})
            sql_object = type('Dummy', (object,), { "length": 2,
                                           "item": [item1, item2]})
            with DBHelper(**self._db_conf) as db:
                result = db.execute_multiple_batch(sql_object)
            return result
        else:
            sql = 'INSERT INTO dbo_fee_config(from_value, to_value, fee, type) VALUES (%s,%s,%s,%s)'      
            array_param = [];
            for item in kwargs.data:
                item.insert(len(item), kwargs.type)
                array_param.append(item)
            
            with DBHelper(**self._db_conf) as db:
                result = db.execute_batch(sql, array_param)
            return result
    
    def admin_get_list_fee(self):
        sql = 'SELECT * FROM dbo_fee_config'
        
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql)
        return result
    
    def admin_insert_update_currency(self, kwargs):
        print(kwargs)
        if not kwargs.id:
            sql = 'INSERT INTO dbo_currency_rate(source, source_name, destination, destination_name, rate) VALUES (%s,%s,%s,%s,%s)'
            param = [[kwargs.source, kwargs.source_name, kwargs.destination, kwargs.destination_name, kwargs.rate]]
            with DBHelper(**self._db_conf) as db:
                result = db.insert_batch(sql, param)
            return result
        else:
            sql = 'UPDATE dbo_currency_rate SET source=%s, source_name=%s, destination=%s, destination_name=%s, rate=%s WHERE id=%s'
            param = [[kwargs.source, kwargs.source_name, kwargs.destination, kwargs.destination_name, kwargs.rate, kwargs.id]]            
            with DBHelper(**self._db_conf) as db:
                result = db.update_batch(sql, param)
            return result
    
    def admin_get_list_currency(self):
        sql = 'SELECT * FROM dbo_currency_rate'
        
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql)
        return result
    
    def admin_insert_update_deposit(self, kwargs):
        print(kwargs)
        if not kwargs.id:
            sql = 'INSERT INTO dbo_deposit(from_price, to_price, deposit_value, customer) VALUES (%s,%s,%s,%s)'
            param = [[kwargs.from_price, kwargs.to_price, kwargs.deposit_value, kwargs.customer]]
            with DBHelper(**self._db_conf) as db:
                result = db.insert_batch(sql, param)
            return result
        else:
            sql = 'UPDATE dbo_deposit SET from_price=%s, to_price=%s, deposit_value=%s, customer=%s WHERE id=%s'
            param = [[kwargs.from_price, kwargs.to_price, kwargs.deposit_value, kwargs.customer, kwargs.id]]        
            with DBHelper(**self._db_conf) as db:
                result = db.update_batch(sql, param)
            return result
        
    def admin_get_list_deposit(self):
        sql = 'SELECT * FROM dbo_deposit'
        
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql)
        return result
    
    def user_create_order(self, kwargs):
        
        connection = pymysql.connect(host=self._db_conf['host'],
                             user=self._db_conf['user'],
                             password=self._db_conf['passwd'],
                             db=self._db_conf['schema'],
                             charset=self._db_conf['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
        detail_id = ''
        result_data = 0
        try:
            with connection.cursor() as cursor:
                # Create a new record
                for item in kwargs.data:
                    sql = "INSERT INTO `dbo_order_detail` (`p_name`, `p_link`, `p_color`, `p_size`, `p_quantity`, `p_price`, `p_image`, `p_vnd_price`, `p_currency`, `p_description`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (item['name'], item['link'], item['color'], item['size'], item['quantity'], item['price'], item['image'], item['price_vnd'], item['currency'], item['item_desc']))
                    detail_id += str(cursor.lastrowid) + ','       
                
                # remove last ,       
                detail_id = detail_id.rstrip(',')
                
                # insert order
                sql = "INSERT INTO `dbo_order` (`order_item`, `order_code`, `price_vnd`, `user_id`, `created_time`) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (detail_id, kwargs.memory_code, kwargs.price_vnd, kwargs.user_id, time.strftime('%Y-%m-%d %H:%M:%S')))
                result_data = cursor.lastrowid
                connection.commit()

        finally:
            connection.close()
        
        return result_data
    
    def admin_update_order_detail(self, kwargs):
        connection = pymysql.connect(host=self._db_conf['host'],
                             user=self._db_conf['user'],
                             password=self._db_conf['passwd'],
                             db=self._db_conf['schema'],
                             charset=self._db_conf['charset'],
                             cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE dbo_order_detail SET p_name=%s, p_link=%s, p_color=%s, p_size=%s, p_quantity=%s, p_price=%s, p_vnd_price=%s WHERE id=%s"
                cursor.execute(sql, (kwargs['p_name'], kwargs['p_link'], kwargs['p_color'], kwargs['p_size'], kwargs['p_quantity'], kwargs['p_price'], kwargs['p_vnd_price'], kwargs['id']))
                sql = "UPDATE dbo_order SET price_vnd=%s WHERE id=%s"
                cursor.execute(sql, (kwargs['price_vnd'], kwargs['order_id']))
                connection.commit()
        finally:
            connection.close()
    
    def admin_update_order(self, kwargs):    
        if hasattr(kwargs, 'final_price'):
            sql = 'UPDATE dbo_order SET status=%s, user_deposit=%s, total_weight=%s, final_price =%s WHERE id=%s'
            param = [[kwargs.status, kwargs.user_deposit, kwargs.total_weight, kwargs.final_price, kwargs.id]]
            with DBHelper(**self._db_conf) as db:
                result = db.update_batch(sql, param)
                print(result)
            return result
        else:
            sql = 'UPDATE dbo_order SET status=%s WHERE id=%s'
            param = [[kwargs.status, kwargs.id]]
            with DBHelper(**self._db_conf) as db:
                result = db.update_batch(sql, param)
            return result
        
    def get_order_info(self, kwargs):
        if hasattr(kwargs, 'user_id'):
            sql = 'SELECT * FROM dbo_order WHERE id=%s AND order_code=%s AND user_id=%s'
            with DBHelper(**self._db_conf) as db:
                result = db.get_dicts(sql, [kwargs.id, kwargs.code, kwargs.user_id])
        else:
            sql = 'SELECT * FROM dbo_order WHERE id=%s AND order_code=%s'
            with DBHelper(**self._db_conf) as db:
                result = db.get_dicts(sql, [kwargs.id, kwargs.code])
        
        if len(result):
            return result[0]
        return None
    
    def get_order_detail(self, params):
        sql = 'SELECT * FROM dbo_order_detail WHERE id IN (%s)' 
        in_p = ', '.join([str(x) for x in params])
        sql = sql % in_p
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql)
        return result
    
    def get_order_from_detail_id(self, detail_id):
        sql = 'SELECT * FROM dbo_order where find_in_set(%s,order_item) <> 0 LIMIT 1'
        
        with DBHelper(**self._db_conf) as db:
            result = db.get_dicts(sql, [detail_id])
            
        if len(result):
            return result[0]
        return None
    
    def get_list_order(self, params):
        if hasattr(params, 'admin'):
            sql = 'SELECT * FROM dbo_order WHERE 1=1 '
        else:
            sql = 'SELECT a.*, b.p_name FROM dbo_order a JOIN dbo_order_detail b ON FIND_IN_SET(b.id, a.order_item) > 0 WHERE 1=1 '
        args = []
        if hasattr(params, 'uid'):
            sql += ' AND user_id = %s'
            args.append(params.uid)
        if hasattr(params, 'status'):
            sql += ' AND status = %s'
            args.append(params.status)
        if hasattr(params, 'order_code'):
            sql += ' AND order_code = %s'
            args.append(params.order_code)
        if hasattr(params, 'from_time'):
            str_to_time = datetime.strptime(params.from_time, '%d/%m/%Y')
            sql_time = str_to_time.strftime('%Y-%m-%d %H:%M:%S')
            sql += ' AND created_time > %s'
            args.append(sql_time)
        if hasattr(params, 'to_time'):
            str_to_time = datetime.strptime(params.to_time, '%d/%m/%Y')
            sql_time = str_to_time.strftime('%Y-%m-%d %H:%M:%S')
            sql += ' AND created_time < %s'
            args.append(sql_time)
        
        if hasattr(params, 'offset'):
            sql += ' LIMIT %s,%s'
            args.append(params.offset)
            args.append(params.limit)
            with DBHelper(**self._db_conf) as db:
                result = db.get_dicts(sql, args)
                total = db.get_values('SELECT FOUND_ROWS() as total')            
            return [result, total[0]]
        else:    
            with DBHelper(**self._db_conf) as db:
                result = db.get_dicts(sql, args)           
            return result
    
    def get_list_user(self, params):
        
        sql = 'SELECT SQL_CALC_FOUND_ROWS * FROM dbo_user WHERE 1=1 '
        args = []
        if hasattr(params, 'email'):
            sql += ' AND email = %s'
            args.append(params.email)
            
        if hasattr(params, 'type'):
            sql += ' AND type = %s'
            args.append(params.type)
            
        if hasattr(params, 'offset'):
            sql += ' LIMIT %s,%s'
            args.append(params.offset)
            args.append(params.limit)

        with DBHelper(**self._db_conf) as db:    
            result = db.get_dicts(sql, args)
            total = db.get_values('SELECT FOUND_ROWS() as total')
            
        return [result, total[0]]
        
    def admin_topup_user(self, params):    
        sql = 'UPDATE dbo_user SET balance = balance + %s WHERE email=%s'
        param = [[params.total, params.email]]            
        with DBHelper(**self._db_conf) as db:
            result = db.update_batch(sql, param)
        return result
        
    def user_deposit_order(self, params): 
        
        sql1 = 'UPDATE dbo_order SET user_deposit = %s, status = 1 WHERE id=%s'
        sql2 = "UPDATE dbo_user SET balance = balance - %s WHERE id=%s"
        with DBHelper(**self._db_conf) as db:
            db.begin()
            db.update_batch(sql1, [[params.deposit_value,params.order_id]])
            db.update_batch(sql2, [[params.deposit_value,params.user_id]])
            db.end()
            
        