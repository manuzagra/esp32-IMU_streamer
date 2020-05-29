def test():
    import os
    from database.btreedb import BtreeDB

    db = BtreeDB('test.db')

    db['one'] = 'one'
    db['two'] = 2
    db[3] = 'three'
    db['four'] = ['foo', 'bar']
    db.put(5,{'first': 1, 'second': 2})

    db.flush()

    db.close()

    db.open('test.db')

    print('####################')
    print('one')
    print('--------------------')
    print(db['one'])
    print('####################')
    print('2')
    print('--------------------')
    print(db['two'])
    print('####################')
    print('three')
    print('--------------------')
    print(db[3])
    print('####################')
    print("['foo', 'bar']")
    print('--------------------')
    print(db['four'])
    print('####################')
    print("{'first': 1, 'second': 2}")
    print('--------------------')
    print(db[5])
    print('####################')


    print('3 in db? (True)')
    print(3 in db)
    print('####################')
    print('deleting (3, "three")')
    del db[3]
    print('####################')
    print('3 in db? (False)')
    print(3 in db)
    print('####################')
    print('get(3,"no three")')
    print(db.get(3,"no three"))
    print('####################')
    print('keys()')
    print(db.keys())
    print('####################')
    print('values()')
    print(db.values())
    print('####################')
    print('items()')
    print(db.items())
    print('####################')

    db.flush()
    db.close()
    os.remove('test.db')
