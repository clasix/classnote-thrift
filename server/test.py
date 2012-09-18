import os


if __name__ == '__main__':
    config = dict()
    config['dev_mode'] = True
    config['sqlite_path'] = 'test.db'
    #config['shell'] = True

    # create the db session
    import model
    model.db = model.db_factory(config)
    if config.has_key('dev_mode') and config.has_key('bootstrap_db'):
        model.bootstrap(model.db)

    if config.has_key('shell'):
        import code
        code.interact()
    else:
        a_user = model.User(username='Cenny', password='123')
        model.db.add(a_user)
        print a_user.id
        b_user = model.db.query(model.User).filter_by(username='Cenny').first()
        print b_user is a_user
