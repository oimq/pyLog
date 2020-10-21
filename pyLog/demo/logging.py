from pyLog import Logger

if __name__=="__main__" :
    logger = Logger(isWrite=True)
    logger.set('level', 0)
    log = logger.log

    log("every")
    log("one!", 'd')
    log("hello", 'i')
    log("world", 'w')
    log("nice",  'e')
    log("smile", 'c')

    logger.set("name", "hello")

    log("every")
    log("one!", 'd')
    log("hello", 'i')
    log("world", 'w')
    log("nice",  'e')
    log("smile", 'c')
