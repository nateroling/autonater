import toggl

def main():
   
    for project, hours in toggl.fetch_unbilled_hours().iteritems():
        print "%s, %s" % (project, hours)

if __name__ == '__main__':
    main()