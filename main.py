from workflow.workflow import pipeline

def main(jwt,day):
    pipeline(day,jwt)
    return 