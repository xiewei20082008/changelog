from gooey import Gooey, GooeyParser
import subprocess32 as subprocess
from subprocess32 import PIPE,Popen
import os
import datetime

env = os.environ.copy()

def waitSubprocess(p):
    try:
        out, err = p.communicate(timeout=10)
        return out 
    except TimeoutExpired:
        print 'subprocess time out.'
        p.kill()
        raise SubErr

def exe(cmd,cwd):
    p = subprocess.Popen(cmd, stderr=PIPE, stdout=PIPE, cwd=cwd, env=env, shell=True)
    try:
        out = waitSubprocess(p)
        return out
    except "suberr":
            raise

@Gooey()
def main():
    parser = GooeyParser()
    
    parser.add_argument(
        'repo',
        default='guest-templates-json',
        action='store'
        )
        
    parser.add_argument(
        'tagRange',
        default='v1.2.0..v1.3.0',
        action='store'
        )
        
    args = parser.parse_args()
    
    currentTime = datetime.date.today()
    time = currentTime.strftime('%a %b %d %Y')
    name = 'Wei Xie <wei.xie@citrix.com>'
    aimTag = args.tagRange.split('..')[1]
    tag = '- {tag}-1'.format(tag=aimTag)
    header = ' '.join(['*', time,name,tag])
    print header
    
    exe('git checkout master','G:/src-code/{0}'.format(args.repo))
    t = exe('git log --no-merges --oneline {tagRange}'.format(tagRange=args.tagRange),'G:/src-code/{repo}'.format(repo=args.repo))
    for i in t.split('\n'):
        if i:
            print '- '+' '.join(i.split(' ')[1:])
        
    print ''
    print 'Update {repo} to {tag}'.format(repo=args.repo,tag=aimTag)
    
if __name__ == '__main__':
    main()
