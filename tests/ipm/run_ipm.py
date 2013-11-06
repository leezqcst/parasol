#! /usr/bin/python

if __name__ == '__main__':
    import json
    from mpi4py import MPI
    from optparse import OptionParser
    from parasol.alg.ipm import ipm
    from parasol.utils.gethostnames import get_hostnames_dict
    comm = MPI.COMM_WORLD

    optpar = OptionParser()
    optpar.add_option('--hostsname', action = 'store', type = 'string', dest = 'hosts_name_st', help = 'hosts name string of parasol servers', metavar = 'dwalin:8888parasolbalin:7777')
    options, args = optpar.parse_args()
    hosts_dict_lst = get_hostnames_dict(options.hosts_name_st)

    cfg_file = '/home/xunzhang/xunzhang/Proj/parasol/config/ipm_cfg.json'
    json_obj = json.loads(open(cfg_file).read())
    nsrv = json_obj['nserver']
    nworker = json_obj['nworker']
    k = json_obj['k']
    input_filename = json_obj['input']
    output = json_obj['output']

    # optional para
    if json_obj.get('alpha'):
        alpha = json_obj['alpha']
    else:
        alpha = 0.001
    if json_obj.get('beta'):
        beta = json_obj['beta']
    else:
        beta = 0.01
    if json_obj.get('rounds'):
        rounds = json_obj['rounds']
    else:
        rounds = 10
    if json_obj.get('limit_s'):
        limit_s = json_obj['limit_s']
    else:
        limit_s = 3
     
    ipm_solver = ipm(comm, hosts_dict_lst, nworker, k, input_filename, output, alpha, beta, rounds, limit_s)

    ipm_solver.solve()
    #print sgd_solver.theta
    
    esum = ipm_solver.calc_loss()
    if comm.Get_rank() == 0:
        print 'esum is', esum
    
    ipm_solver.write_ipm_result()
